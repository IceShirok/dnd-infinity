from pylatex import Document, Section, Subsection, Command, LineBreak, LongTable
from pylatex.utils import italic, NoEscape, bold

from ddddd.entity import base
from ddddd.pc_playground import get_available_characters


def generate_file_friendly_name(name):
    return name.lower().replace(' ', '_')


def generate_character_sheet(pc):
    doc = Document(generate_file_friendly_name(pc.name))

    doc.preamble.append(Command('title', pc.name))
    doc.preamble.append(Command('author', 'IceShirok'))
    doc.append(NoEscape(r'\maketitle'))

    with doc.create(Section('Basics', numbering=False)):
        doc.append(bold('Class & Level'))
        doc.append(' {} {}'.format(pc.vocation_name, pc.level))
        doc.append(LineBreak())

        doc.append(bold('Background'))
        doc.append(' {}'.format(pc.background_name))
        doc.append(LineBreak())

        doc.append(bold('Race'))
        doc.append(' {} ({})'.format(pc.base_race_name, pc.race_name))
        doc.append(LineBreak())

    with doc.create(Section('Basic Combat Stuff', numbering=False)):
        doc.append(bold('Armor Class'))
        armor_class_source = pc.worn_items.armor.name if pc.worn_items.armor else 'dodgy stuff'
        doc.append(' {} ({})'.format(pc.armor_class, armor_class_source))
        doc.append(LineBreak())

        doc.append(bold('Initiative'))
        doc.append(' {}'.format(pc.initiative))
        doc.append(LineBreak())

        doc.append(bold('Speed'))
        doc.append(' {} ft'.format(pc.speed))
        doc.append(LineBreak())

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
                ability_row = [
                    ability,
                    pc.ability_scores[ability].score,
                    base.prettify_modifier(pc.ability_scores[ability].modifier),
                ]
                data_table.add_row(ability_row)

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

    doc.generate_pdf(clean_tex=False)
    doc.generate_tex()


def main():
    fethri = get_available_characters()['fethri']['create']()
    generate_character_sheet(fethri)


if __name__ == '__main__':
    main()
