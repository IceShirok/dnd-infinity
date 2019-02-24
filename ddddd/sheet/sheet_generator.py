import pylatex
from pylatex import Document, Section, Subsection, Command, LineBreak, LongTable, Itemize, LargeText, NewPage, HugeText
from pylatex.utils import NoEscape, bold

from ddddd.entity.character import base
from ddddd.pc_playground import get_available_characters


def generate_file_friendly_name(name):
    """Translates a filename to a more terminal-friendly filename."""
    return name.lower().replace(' ', '_')


def decorate_pc_name(name):
    name_split = name.split(' ')
    name_split = list(map(lambda n: r'$\mathcal{'+n[0]+r'}\mathfrak{'+n[1:]+r'}$', name_split))
    return r'\noindent{\huge{'+' '.join(name_split)+r'}}\\'


def make_better_english(s):
    s_split = s.replace('_', ' ').split(' ')
    return ' '.join(map(lambda x: x.capitalize(), s_split))


def generate_character_sheet(pc):
    filename = '{}.tex'.format(generate_file_friendly_name(pc.name))
    with open(filename, 'w') as f:
        def write_(line):
            f.write('{}\n'.format(line))
        write_(r'\documentclass[twocolumn]{article}')
        # packages start
        write_(r'\usepackage{multicol}')
        write_(r'\usepackage{covington}')
        write_(r'\usepackage[letterpaper,margin=.75in]{geometry}')
        write_(r'\usepackage{pgfpages}')
        write_(r'\usepackage{amsfonts,amsmath,amssymb}')
        write_(r'\usepackage{stmaryrd}')
        write_(r'\usepackage{setspace}')
        write_(r'\usepackage{enumitem}')
        write_(r'\usepackage{wasysym}')
        write_(r'\usepackage{pifont}')
        write_(r'\usepackage{marvosym}')
        write_(r'\usepackage{qtree}')
        write_(r'\usepackage{MnSymbol,wasysym}')
        write_(r'\usepackage{fourier-orns}')
        write_(r'\usepackage{array}')
        # packages end

        write_(r'\begin{document}')

        # Banner
        write_(r'\pagenumbering{gobble}')
        write_(decorate_pc_name(pc.name))
        race = '{} ({})'.format(pc.base_race_name, pc.race_name)
        vocation = '{} {}'.format(pc.vocation_name, pc.level)
        background = pc.background_name
        write_(r'\noindent {} $\vert$ {} $\vert$ {}\\'.format(race, vocation, background))
        write_(r'\vspace{8pt}')

        # Ability scores
        write_(r'\noindent\begin{tabular}{|c|c|c|c|c|c|}')
        write_(r'\hline')
        ability_names = list(map(lambda a: r'\textbf{'+a+r'}', pc.ability_scores.keys()))
        ability_scores = list(map(lambda a: str(a.score), pc.ability_scores.values()))
        ability_mods = list(map(lambda a: base.prettify_modifier(a.modifier), pc.ability_scores.values()))
        for ability_row in [ability_names, ability_scores, ability_mods]:
            write_(r'{}\\'.format(r'&'.join(ability_row)))
            write_(r'\hline')
        write_(r'\end{tabular}\\[2pt]')
        write_(r'\vspace{5pt}')

        # Ability proficiencies
        write_(r'\noindent{\Large{\textit{Skill Proficiencies}}}\\')
        write_(r'\noindent\begin{tabular}{|m{3.1in}|}')
        write_(r'\hline')
        for ability in pc.ability_scores:
            write_(r'\textbf{'+ability+r'} \ding{114}\\')
            saving_throw = pc.saving_throws[ability]
            save_sym = r'$\square$'
            if saving_throw.is_proficient:
                save_sym = r'$\checkmark$'
            write_(r'{} {} $\vert$ {}\\'.format(save_sym, 'Saving Throw', base.prettify_modifier(saving_throw.modifier)))
            if ability in pc.skills_by_ability:
                skills = pc.skills_by_ability[ability]
                for s_name, skill in skills.items():
                    skill_sym = r'$\square$'
                    if skill.expertise:
                        skill_sym = r'$\bigstar$'
                    elif skill.is_proficient:
                        skill_sym = r'$\checkmark$'
                    write_(r'{} {} $\vert$ {}\\'.format(skill_sym, s_name, base.prettify_modifier(skill.modifier)))
        write_(r'\hline')
        write_(r'\end{tabular}')
        write_(r'\vspace{8pt}')

        # Basic combat stuff
        write_(r'\noindent\begin{tabular}{|c|c|c|}')
        write_(r'\hline')
        write_(r'Armor Class&Initiative&Speed\\')
        write_(r'{}&{}&{}\\'.format(pc.armor_class, base.prettify_modifier(pc.initiative), pc.speed))
        write_(r'\hline')
        write_(r'\end{tabular}\\[2pt]')
        write_(r'\vspace{5pt}')

        # Health stuff
        write_(r'\noindent{\Large{\textit{Health}}}\\')
        write_(r'\noindent\begin{tabular}{|m{3.1in}|}')
        write_(r'\hline')
        # Hit dice
        hit_dice = pc.total_hit_dice_prettified
        ding = r'\ding{114}'
        dings = ' '.join([ding] * pc.level)
        write_(r'\noindent Hit dice used ('+hit_dice+r'): '+dings+r'\\[5pt]')
        write_(r'\noindent Current HP: \rule{.4in}{.2pt} / '+str(pc.max_hit_points)+r'\\[5pt]')
        write_(r'\noindent Temporary HP: \rule{.4in}{.2pt}\\[5pt]')
        write_(r'\noindent Death Saves: $\checkmark$\ding{114} $\checkmark$\ding{114} $\checkmark$\ding{114} \ \ \ \ding{55}\ding{114} \ding{55}\ding{114} \ding{55}\ding{114}\\[5pt]')
        write_(r'\hline')
        write_(r'\end{tabular}')
        write_(r'\vspace{12pt}')

        # Weapons
        write_(r'\noindent{\Large{\textit{Weapons}}}\\')
        write_(r'\noindent\begin{tabular}{|m{3.1in}|}')
        write_(r'\hline')
        for weapon in pc.worn_items.weapons:
            weapon_details = pc.calculate_weapon_bonuses()[weapon.name]
            attack_bonus = '{} ({})'.format(base.prettify_modifier(weapon_details['attack_bonus']),
                                            weapon_details['attack_type'])
            write_(r'\textbf{'+weapon.name+r'} \ding{114}\\')
            write_(r'{} $\vert$ {}\\'.format(attack_bonus, weapon_details['damage']))
        for _ in range(0, 4):
            write_(r'\rule{3in}{.2pt}\\')
        write_(r'\hline')
        write_(r'\end{tabular}')
        write_(r'\vspace{8pt}')

        write_(r'\vfill\null')
        write_(r'\columnbreak')

        # Proficiencies
        write_(r'\noindent{\Large{\textit{Proficiencies}}}\\')
        write_(r'\noindent\begin{tabular}{|m{3.1in}|}')
        write_(r'\hline')
        proficiencies = pc.proficiencies
        proficiencies['Languages'] = pc.languages
        for prof, p_list in proficiencies.items():
            write_(r'\textbf{'+prof+r'}\\')
            p = list(map(lambda l: make_better_english(l), p_list))
            write_(r'{}\\'.format(r', '.join(p)))
        write_(r'\hline')
        write_(r'\end{tabular}')
        write_(r'\vspace{12pt}')

        # Traits and features
        write_(r'\noindent{\Large{\textit{Traits \& Features}}}\\')
        write_(r'\noindent\begin{tabular}{|m{3.1in}|}')
        write_(r'\hline')
        for feature_type, f_list in pc.features.items():
            write_(r'\Large{'+feature_type+r'}\\')
            for feature in f_list:
                write_(r'\textbf{'+feature.name+r'}\\')
                write_(r'{}\\'.format(feature.description))
            # p = list(map(lambda l: make_better_english(l), p_list))
            # write_(r'{}\\'.format(r', '.join(p)))
        write_(r'\hline')
        write_(r'\end{tabular}')
        write_(r'\vspace{12pt}')

        write_(r'\end{document}')

        f.close()

    import os
    os.system("pdflatex {}".format(filename))

def generate_character_sheet_v1(pc):
    doc = Document(default_filepath=generate_file_friendly_name(pc.name),
                   documentclass='article',
                   document_options='twocolumn')

    doc.append(HugeText(pc.name))
    doc.append('\n')

    doc.append('{} ({})'.format(pc.base_race_name, pc.race_name))
    doc.append(' | ')
    doc.append('{} {}'.format(pc.vocation_name, pc.level))
    doc.append(' | ')
    doc.append('{}'.format(pc.background_name))
    # doc.preamble.append(Command('title', pc.name))
    # doc.preamble.append(Command('author', 'IceShirok'))
    # doc.append(NoEscape(r'\maketitle'))

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
                    save_proficiency = 'proficient' if pc.saving_throws[ability].is_proficient else '-'
                    saving_throw_row = [
                        'Saving Throw',
                        base.prettify_modifier(pc.saving_throws[ability].modifier),
                        save_proficiency,
                    ]
                    data_table.add_row(saving_throw_row)
                    if ability in pc.skills_by_ability:
                        for skill in pc.skills_by_ability[ability]:
                            skill_details = pc.skills_by_ability[ability][skill]
                            modifier = skill_details.modifier
                            skill_proficiency = '-'
                            if skill_details.is_proficient:
                                skill_proficiency = 'skilled'
                            if skill_details.expertise:
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

    if pc.spellcasting:
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
    pc = get_available_characters()['fethri']['create'](3)
    generate_character_sheet(pc)


if __name__ == '__main__':
    main()
