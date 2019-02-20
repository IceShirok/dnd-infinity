from pylatex import Document, Section, Subsection, Command, LineBreak, LongTable, Itemize, LargeText, NewPage
from pylatex.utils import italic, NoEscape, bold

from ddddd.entity import base
from ddddd.pc_playground import get_available_characters


def generate_file_friendly_name(name):
    """Translates a filename to a more terminal-friendly filename."""
    return name.lower().replace(' ', '_')


def generate_character_sheet(pc):
    doc = Document(generate_file_friendly_name(pc.name))

    doc.preamble.append(Command('title', pc.name))
    doc.preamble.append(Command('author', 'IceShirok'))
    doc.append(NoEscape(r'\maketitle'))

    with doc.create(Section('Basics', numbering=False)):
        with doc.create(LongTable("l l")) as data_table:
            data_table.add_row(['Class and Level', '{} {}'.format(pc.vocation_name, pc.level)])
            data_table.add_row(['Background', '{}'.format(pc.background_name)])
            data_table.add_row(['Race', '{} ({})'.format(pc.base_race_name, pc.race_name)])

    with doc.create(Section('Basic Combat Stuff', numbering=False)):
        with doc.create(LongTable("l l")) as data_table:
            armor_class_source = pc.worn_items.armor.name if pc.worn_items.armor else 'dodgy stuff'
            data_table.add_row(['Armor Class', '{} ({})'.format(pc.armor_class, armor_class_source)])
            data_table.add_row(['Initiative', '{}'.format(pc.initiative)])
            data_table.add_row(['Speed', '{} ft'.format(pc.speed)])

    with doc.create(Section('Ability Scores', numbering=False)):
        doc.append(bold('Proficiency Bonus'))
        doc.append(' {}'.format(base.prettify_modifier(pc.proficiency_bonus)))
        doc.append(LineBreak())

        with doc.create(LongTable("l l l")) as data_table:
            data_table.add_hline()
            data_table.add_row(['Ability', 'Score', 'Modifier'])
            data_table.add_hline()
            data_table.end_table_header()
            for ability in pc.ability_scores.keys():
                weapon_row = [
                    ability,
                    pc.ability_scores[ability].score,
                    base.prettify_modifier(pc.ability_scores[ability].modifier),
                ]
                data_table.add_row(weapon_row)

        for ability in pc.ability_scores.keys():
            with doc.create(Subsection('Ability Proficiencies: {}'.format(ability), numbering=False)):
                with doc.create(LongTable("l l l")) as data_table:
                    save_proficiency = 'proficient' if pc.saving_throws[ability]['is_proficient'] else '-'
                    saving_throw_row = [
                        'Saving Throw',
                        base.prettify_modifier(pc.saving_throws[ability]['modifier']),
                        save_proficiency,
                    ]
                    data_table.add_row(saving_throw_row)
                    if ability in pc.skills_by_ability:
                        for skill in pc.skills_by_ability[ability]:
                            skill_details = pc.skills_by_ability[ability][skill]
                            modifier = skill_details['modifier']
                            skill_proficiency = '-'
                            if skill_details['is_proficient']:
                                skill_proficiency = 'skilled'
                            if skill_details['expertise']:
                                skill_proficiency = 'expert'
                            skill_row = [
                                skill,
                                base.prettify_modifier(modifier),
                                skill_proficiency,
                            ]
                            data_table.add_row(skill_row)

    with doc.create(Section('Health Stuff', numbering=False)):
        with doc.create(LongTable("l l")) as data_table:
            data_table.add_row(['Hit Points', '{} / {}'.format(pc.max_hit_points, pc.max_hit_points)])
            data_table.add_row(['Temporary Hit Points', '{}'.format(0)])
            data_table.add_row(['Total Hit Dice', '{}'.format(pc.total_hit_dice_prettified)])
            data_table.add_row(['Death Saves', 'TBD'])

    with doc.create(Section('Attacks and Spellcasting', numbering=False)):
        with doc.create(Subsection('Attacks', numbering=False)):
            with doc.create(LongTable("l l l")) as data_table:
                data_table.add_hline()
                data_table.add_row(['Name', 'Attack Bonus', 'Damage'])
                data_table.add_hline()
                data_table.end_table_header()

                for weapon in pc.worn_items.weapons:
                    weapon_details = pc.calculate_weapon_bonuses()[weapon.name]
                    attack_bonus = '{} ({})'.format(base.prettify_modifier(weapon_details['attack_bonus']),
                                                    weapon_details['attack_type'])
                    weapon_row = [
                        weapon.name,
                        attack_bonus,
                        weapon_details['damage'],
                    ]
                    data_table.add_row(weapon_row)

                if pc.spellcasting and pc.cantrips:
                    for cantrip_name in pc.calculate_damage_cantrips():
                        cantrip_details = pc.calculate_damage_cantrips()[cantrip_name]

                        cantrip_row = [
                            cantrip_name,
                            cantrip_details['attack_bonus'],
                            cantrip_details['damage'],
                        ]
                        data_table.add_row(cantrip_row)

    with doc.create(Section('Proficiencies', numbering=False)):
        with doc.create(Subsection('Languages', numbering=False)):
            with doc.create(Itemize()) as itemize:
                for p in pc.languages:
                    itemize.add_item(p)
        for prof in pc.proficiencies:
            with doc.create(Subsection(prof, numbering=False)):
                with doc.create(Itemize()) as itemize:
                    for p in pc.proficiencies[prof]:
                        itemize.add_item(p)

    with doc.create(Section('Traits and Features', numbering=False)):
        def add_feature_subsection(title, features, doc):
            with doc.create(Subsection(title, numbering=False)):
                with doc.create(Itemize()) as itemize:
                    for feature in features:
                        itemize.add_item(feature.name)
                        itemize.add_item(feature.description)

        add_feature_subsection('Racial Traits', pc.racial_traits, doc)
        add_feature_subsection('Background Features', pc.background_feature, doc)
        if pc.feats:
            add_feature_subsection('Feats', pc.feats, doc)
        add_feature_subsection('Class Features', pc.vocation_features, doc)

    add_spellcasting_page(pc, doc)
    add_equipment_page(pc, doc)

    doc.generate_pdf(clean_tex=False)
    doc.generate_tex()


def generate_spell_card(spell, doc):
    doc.append(LargeText(spell.name))
    with doc.create(LongTable("l l")) as data_table:
        data_table.add_row(['Name', spell.name])
        data_table.add_row(['Type', '{}-level {}'.format(spell.level, spell.magic_school)])
        data_table.add_row(['Casting time', spell.casting_time])
        data_table.add_row(['Range', spell.spell_range])
        data_table.add_row(['Components', ', '.join(spell.components)])
        data_table.add_row(['Duration', spell.duration])
        data_table.add_row(['Description', spell.description])


def add_spellcasting_page(pc, doc):
    doc.append(NewPage())

    with doc.create(Section('Spellcasting', numbering=False)):
        with doc.create(LongTable("l l")) as data_table:
            data_table.add_row(['Spellcasting Ability', pc.spellcasting.spellcasting_ability])
            data_table.add_row(['Spell Save DC', pc.spell_save_dc])
            data_table.add_row(['Spell Attack Bonus', base.prettify_modifier(pc.spell_attack_bonus)])

        if pc.spellcasting and pc.cantrips:
            with doc.create(Subsection('Cantrips', numbering=False)):
                for cantrip in pc.cantrips:
                    generate_spell_card(cantrip, doc)

        for spell_type in pc.casting_spells.keys():
            with doc.create(Subsection(spell_type, numbering=False)):
                for spell in pc.casting_spells[spell_type]:
                    generate_spell_card(spell, doc)


def add_equipment_page(pc, doc):
    doc.append(NewPage())

    with doc.create(Section('Equipment', numbering=False)):
        doc.append(bold('Carrying Capacity'))
        doc.append(' {} / {}'.format(pc.carrying_weight, pc.carrying_capacity))
        doc.append(LineBreak())

        with doc.create(Subsection('Equipped Items', numbering=False)):
            doc.append(bold('Total Worth:'))
            doc.append(' {}GP'.format(pc.total_equipment_worth))
            doc.append(LineBreak())

            if pc.worn_items.armor:
                doc.append(bold('Armor:'))
                doc.append(' {} (armor)'.format(pc.worn_items.armor.name))
                doc.append(LineBreak())

            with doc.create(Itemize()) as itemize:
                for weapon in pc.worn_items.weapons:
                    itemize.add_item('{} (weapon)'.format(weapon.name))

        with doc.create(Subsection('Backpack', numbering=False)):
            doc.append(bold('Total Worth:'))
            doc.append(' {}GP'.format(pc.total_backpack_worth))
            doc.append(LineBreak())

            with doc.create(Itemize()) as itemize:
                for item in pc.backpack.items:
                    if item.quantity > 1:
                        itemize.add_item('{} ({})'.format(item.name, item.quantity))
                    else:
                        itemize.add_item(item.name)


def main():
    pc = get_available_characters()['tamiphi']['create'](3)
    generate_character_sheet(pc)


if __name__ == '__main__':
    main()
