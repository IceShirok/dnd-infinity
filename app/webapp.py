
import json
import sys

import race, cclass, background, pc
import equipment
import app


"""
Testing playground for D&D Infinity.
"""
def main():
    dorian = app.create_dorian()
    dorian_json = dorian.__json__()
    print(json.dumps(dorian.generate_character_sheet(), indent=4))
    write_html_page(dorian)

def generate_banner_html(player_character):
    html_page = ''
    html_page += '<div>'
    html_page += '<h2>{}</h2>'.format(player_character.name)
    html_page += '<p>Class & Level: {} {}</p>'.format(player_character.class_name, player_character.level)
    html_page += '<p>Background: {}</p>'.format(player_character.background_name)
    html_page += '<p>Race: {}</p>'.format(player_character.race_name)
    html_page += '</div>'
    return html_page

def generate_ability_scores_html(player_character):
    html_page = ''
    html_page += '<div>'
    html_page += '<h2>Ability Scores</h2>'
    html_page += '<div>Proficiency bonus: {}</div>'.format(player_character.proficiency_bonus)
    def generate_ability_score_html(ability, score):
        mod = pc.prettify_modifier(pc._modifier(score))
        return '<div style="margin: 5px"><p>{}</p><h3>{}</h3><p>{}</p></div>'.format(ability, score, mod)
    for ability in ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA']:
        html_page += generate_ability_score_html(ability, player_character.base.ability_scores[ability])
    html_page += '</div>'
    return html_page

def generate_saving_throws_html(player_character):
    html_page = ''
    html_page += '<div>'
    html_page += '<h2>Saving Throws</h2>'
    def generate_saving_throw_html(ability, modifier, is_proficient):
        tick = 'v' if is_proficient else '-'
        return '<div style="margin: 5px"><p>{} {}: {}</p></div>'.format(tick, ability, pc.prettify_modifier(modifier))
    for save in player_character.saving_throws:
        s_details = player_character.saving_throws[save]
        html_page += generate_saving_throw_html(save, s_details['modifier'], s_details['is_proficient'])
    html_page += '</div>'
    return html_page

def generate_skills_html(player_character):
    html_page = ''
    html_page += '<div>'
    html_page += '<h2>Skills</h2>'
    def generate_skill_html(skill, is_proficient, modifier, ability):
        tick = 'v' if is_proficient else '-'
        return '<div style="margin: 5px"><p>{} {}: {} ({})</p></div>'.format(tick, skill, pc.prettify_modifier(modifier), ability)
    for skill in player_character.skill_proficiencies:
        s_details = player_character.skill_proficiencies[skill]
        html_page += generate_skill_html(skill, s_details['is_proficient'], s_details['modifier'], s_details['ability'])
    html_page += '</div>'
    return html_page

def generate_basic_combat_html(player_character):
    html_page = ''
    html_page += '<div>'
    html_page += '<h2>Basic Combat Stuff</h2>'
    html_page += '<p>Armor Class: {}</p>'.format(player_character.armor_class)
    html_page += '<p>Initiative: {}</p>'.format(player_character.initiative)
    html_page += '<p>Speed: {}</p>'.format(player_character.speed)
    html_page += '</div>'
    return html_page

def generate_health_html(player_character):
    html_page = ''
    html_page += '<div>'
    html_page += '<h2>Health Stuff</h2>'
    html_page += '<p>Hit Points: {} / {}</p>'.format(player_character.max_hit_points, player_character.max_hit_points)
    html_page += '<p>Temporary Hit Points: {}</p>'.format(0)
    def prettify_hit_dice(hit_dice):
        p = []
        for die in hit_dice:
            p.append('{}{}'.format(hit_dice[die], die))
        return ' + '.join(p)
    html_page += '<p>Total Hit Dice: {}</p>'.format(prettify_hit_dice(player_character.total_hit_dice))
    html_page += '<p>Death Saves: {} Success / {} Failures</p>'.format(0, 0)
    html_page += '</div>'
    return html_page

def generate_features_html(player_character):
    return '<p>Traits & Features TBD</p>'

def write_html_page(player_character):
    html_page = '<html>'
    html_page += '<head><title>DnD Character Sheet Test</title></head>'
    html_page += '<body>'

    html_page += '<h1>Character Sheet</h1>'
    
    html_page += '<div>'
    html_page += generate_banner_html(player_character)
    html_page += '</div>'

    html_page += '<div style="display: inline-block; margin: 5px; vertical-align: top;">'
    html_page += generate_ability_scores_html(player_character)
    html_page += '</div>'

    html_page += '<div style="display: inline-block; margin: 5px; vertical-align: top;">'
    html_page += generate_saving_throws_html(player_character)
    html_page += generate_skills_html(player_character)
    html_page += '</div>'

    html_page += '<div style="display: inline-block; margin: 5px; vertical-align: top;">'
    html_page += generate_basic_combat_html(player_character)
    html_page += generate_health_html(player_character)
    html_page += '</div>'
    
    html_page += '<div style="display: inline-block; margin: 5px; vertical-align: top;">'
    html_page += generate_features_html(player_character)
    html_page += '</div>'

    html_page += '</body>'
    html_page += '</html>'

    f = open("index.html", "w")
    f.write(html_page)
    f.close()


if __name__ == '__main__':
    main()
