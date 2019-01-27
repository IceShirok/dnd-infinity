
import json

from ddddd.entity import base
from ddddd import app
from ddddd.entity.character import spells

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def main():
    """
    Testing playground for D&D Infinity.
    """
    dorian = app.create_dorian()
    logger.debug(json.dumps(dorian.generate_character_sheet(), indent=4))
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
        mod = base.prettify_modifier(base.modifier(score))
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
        return '<div style="margin: 5px"><p>{} {}: {}</p></div>'.format(tick, ability, base.prettify_modifier(modifier))
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
        return '<div style="margin: 5px"><p>{} {}: {} ({})</p></div>'.format(tick, skill, base.prettify_modifier(modifier), ability)
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


def generate_attacks_html(player_character):
    html_page = ''
    html_page += '<div>'
    html_page += '<h2>Attacks & Spellcasting</h2>'
    html_page += '<h3>Attacks</h3>'
    html_page += '<table>'
    html_page += '<tr><th>Name</th><th>Attack Bonus</th><th>Damage</th></tr>'
    for weapon in player_character.worn_items.weapons:
        html_page += '<tr><td>{}</td><td>{}</td><td>{}</td></tr>'.format(weapon.name, 0, weapon.damage)
    html_page += '</table>'

    html_page += '<h3>Spellcasting</h3>'
    for spell_type in spells.ORD_TO_NUM:
        if spell_type in player_character.spellcasting.spell_slots:
            num_spell_slots = player_character.spellcasting.spell_slots[spell_type]
            html_page += '<h4>{} ({} spell slots)</h4>'.format(spell_type, num_spell_slots)
            spellz = list(filter(lambda x: x.level == spells.ORD_TO_NUM[spell_type], player_character.spellcasting.list_spells_known))
            for spell in spellz:
                html_page += '<p>{}</p>'.format(spell.name)

    html_page += '</div>'
    return html_page


def generate_equipment_html(player_character):
    html_page = ''
    html_page += '<div>'
    html_page += '<h2>Equipment</h2>'
    html_page += 'Carrying capacity: {} / {}'.format(player_character.carrying_weight, player_character.carrying_capacity)
    if player_character.worn_items.armor:
        html_page += '<p>{} (equipped, armor)</p>'.format(player_character.worn_items.armor.name)
    for weapon in player_character.worn_items.weapons:
        html_page += '<p>{} (equipped, weapon)</p>'.format(weapon.name)
    for item in player_character.backpack.items:
        quantity = ' ({})'.format(item.quantity) if item.quantity > 1 else ''
        html_page += '<p>{}{}</p>'.format(item.name, quantity)
    html_page += '</div>'
    return html_page


def generate_proficiencies(player_character):
    html_page = ''
    html_page += '<div>'
    html_page += '<h2>Proficiencies</h2>'
    for p in player_character.proficiencies:
        a_list = ', '.join(player_character.proficiencies[p])
        html_page += '<p><strong>{}</strong>: {}</p>'.format(p, a_list)
    html_page += '<p><strong>Languages</strong>: {}</p>'.format(', '.join(player_character.languages))
    html_page += '</div>'
    return html_page


def generate_features_html(player_character):
    html_page = ''
    html_page += '<div>'
    html_page += '<h2>Traits & Features</h2>'
    subfeatures = player_character.features
    for fk in subfeatures:
        html_page += '<h3>{}</h3>'.format(fk)
        subfeature = subfeatures[fk]
        for f in subfeature:
            html_page += '<h4>{}</h4><p>{}</p>'.format(subfeature[f]['name'], subfeature[f]['description'])
    html_page += '</div>'
    return html_page


def write_html_page(player_character):
    html_page = '<html>'
    html_page += '<head>'
    html_page += '<title>DnD Character Sheet Test</title>'
    html_page += '<link rel="stylesheet" href="styles.css" />'
    html_page += '</head>'
    html_page += '<body>'

    html_page += '<h1>Character Sheet</h1>'

    html_page += '<div id="container">' # start container
    
    html_page += '<div id="banner">'
    html_page += generate_banner_html(player_character)
    html_page += '</div>'

    html_page += '<div class="column">'
    html_page += generate_ability_scores_html(player_character)
    html_page += '</div>'

    html_page += '<div class="column">'
    html_page += generate_saving_throws_html(player_character)
    html_page += generate_skills_html(player_character)
    html_page += '</div>'

    html_page += '<div class="column">'
    html_page += generate_basic_combat_html(player_character)
    html_page += generate_health_html(player_character)
    html_page += generate_attacks_html(player_character)
    html_page += generate_equipment_html(player_character)
    html_page += '</div>'
    
    html_page += '<div class="column">'
    html_page += generate_proficiencies(player_character)
    html_page += generate_features_html(player_character)
    html_page += '</div>'
    
    html_page += '</div>' # end container

    html_page += '</body>'
    html_page += '</html>'

    f = open("index.html", "w")
    f.write(html_page)
    f.close()


if __name__ == '__main__':
    main()
