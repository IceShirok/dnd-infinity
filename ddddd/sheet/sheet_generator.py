
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
            write_(r'\textbf{'+ability+r'}\\')
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
        for _ in range(0, 3):
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


def main():
    pc = get_available_characters()['fethri']['create'](3)
    generate_character_sheet(pc)


if __name__ == '__main__':
    main()
