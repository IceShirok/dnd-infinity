
import json
import sys

import race, cclass, background, pc
import equipment

"""
Testing playground for D&D Infinity.
"""
def main():
    write_html_page()
    """
    if len(sys.argv) < 2:
        print('put in argument pls')
        print('"pc" for testing pc')
        print('"stuff" for testing equipment')
    elif sys.argv[1] == 'pc':
        test_pc()
    elif sys.argv[1] == 'stuff':
        test_stuff()
    else:
        print('not sure what you put in')
        print('try something else')
    print('bye')
    """

def write_html_page():
    dorian = create_dorian()
    dorian_json = dorian.__json__()
    print(json.dumps(dorian.generate_character_sheet(), indent=4))

    html_page = '<html>'
    html_page += '<head><title>DnD Character Sheet Test</title></head>'
    html_page += '<body>'

    html_page += '<h1>Character Sheet</h1>'
    
    html_page += '<div>'
    html_page += '<p>Name: {}</p>'.format(dorian.name)
    html_page += '<p>Class & Level: {} {}</p>'.format(dorian.class_name, dorian.level)
    html_page += '<p>Background: {}</p>'.format(dorian.background_name)
    html_page += '<p>Race: {}</p>'.format(dorian.race_name)
    html_page += '</div>'
    
    html_page += '<div>Proficiency bonus: {}</div>'.format(dorian.proficiency_bonus)
    
    html_page += '<div>'
    html_page += '<h2>Ability Scores</h2>'
    def generate_ability_score_html(ability, score):
        mod = pc.prettify_modifier(pc._modifier(score))
        return '<div style="display: inline-block; margin: 5px"><p>{}</p><h3>{}</h3><p>{}</p></div>'.format(ability, score, mod)
    for ability in ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA']:
        html_page += generate_ability_score_html(ability, dorian.base.ability_scores[ability])
    html_page += '</div>'
    
    html_page += '<div>'
    html_page += '<h2>Saving Throws</h2>'
    def generate_saving_throw_html(ability, modifier, is_proficient):
        tick = 'v' if is_proficient else '-'
        return '<div style="margin: 5px"><p>{} {}: {}</p></div>'.format(tick, ability, pc.prettify_modifier(modifier))
    for save in dorian.saving_throws:
        s_details = dorian.saving_throws[save]
        html_page += generate_saving_throw_html(save, s_details['modifier'], s_details['is_proficient'])
    html_page += '</div>'

    
    html_page += '<div>'
    html_page += '<h2>Skills</h2>'
    def generate_skill_html(skill, is_proficient, modifier, ability):
        tick = 'v' if is_proficient else '-'
        return '<div style="margin: 5px"><p>{} {}: {} ({})</p></div>'.format(tick, skill, pc.prettify_modifier(modifier), ability)
    for skill in dorian.skill_proficiencies:
        s_details = dorian.skill_proficiencies[skill]
        html_page += generate_skill_html(skill, s_details['is_proficient'], s_details['modifier'], s_details['ability'])
    html_page += '</div>'

    html_page += '<div>'
    html_page += '<h2>Health Stuff</h2>'
    html_page += '<p>Armor Class: {}</p>'.format(dorian.armor_class)
    html_page += '<p>Initiative: {}</p>'.format(dorian.initiative)
    html_page += '<p>Speed: {}</p>'.format(dorian.speed)
    html_page += '<p>Hit Points: {} / {}</p>'.format(dorian.max_hit_points, dorian.max_hit_points)
    html_page += '<p>Temporary Hit Points: {}</p>'.format(0)
    def prettify_hit_dice(hit_dice):
        p = []
        for die in hit_dice:
            p.append('{}{}'.format(hit_dice[die], die))
        return ' + '.join(p)
    html_page += '<p>Total Hit Dice: {}</p>'.format(prettify_hit_dice(dorian.total_hit_dice))
    html_page += '<p>Death Saves: {} Success / {} Failures</p>'.format(0, 0)
    html_page += '</div>'

    html_page += '</body>'
    html_page += '</html>'
    f = open("index.html", "w")
    f.write(html_page)
    f.close()
    

def create_dorian():
    dorian_base = pc.PlayerBase("Dorian Sapbleden", 16, 10, 14, 12, 14, 8, level=2)
    dorian_race = race.HillDwarf(traits={'tool_proficiency': {'tools': ['brewers_kit']}})
    dorian_classes = [
            cclass.RangerFactory().generate_by_level(1, skills=['athletics', 'animal_handling', 'survival'], favored_enemy='plants', languages='elvish', favored_terrain='forest'),
            cclass.RangerFactory().generate_by_level(2, fighting_style=['two_weapon_fighting'])
            ]
    dorian_background = background.Criminal()
    dorian_pc = pc.PlayerCharacter(dorian_base, dorian_race, dorian_classes, dorian_background)
    return dorian_pc

def test_pc():
    dorian_pc = create_dorian()
    print(dorian_pc.__str__())

    print('-----')

    ttt_base = pc.PlayerBase("Tamiphi Tockentell", 10, 11, 16, 18, 20, 7, level=8)
    gnome = race.RockGnome({})
    print(ttt_base)
    print(gnome)

    print('-----')

    lok_base = pc.PlayerBase("Lok", 15, 18, 10, 12, 16, 9, level=4)
    human = race.Human(languages=['draconic'])
    print(lok_base)
    print(human)

    print('-----')

    print(json.dumps(dorian_pc.generate_character_sheet(), indent=4))

def test_stuff():
    backpack = equipment.Backpack(gold_pieces=15)
    print(backpack)
    backpack.add_item(equipment.Weapon('dagger', '1d4 piercing', 200, 1, ['finesse', 'light', 'thrown (range 20/60)'])
)
    backpack.add_item(equipment.Item('crowbar'))
    backpack.add_item(equipment.Item('clothes', description='A set of dark common clothes including a hood.'))
    print(backpack)

if __name__ == '__main__':
    main()

