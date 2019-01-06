
import math


def _modifier(score):
    # Calculates the ability modifier
    return math.floor((score-10)/2)

def _modifier_p(score):
    # Calculates and returns a prettified ability modifier score
    mod = _modifier(score)
    if mod > 0:
        return '+{}'.format(mod)
    else:
        return str(mod)

def calculate_ability_scores(base, race):
    # Calculate the scores and modifiers for each ability score
    ability_scores_raw = base.ability_scores

    for a in race.asi.keys():
        ability_scores_raw[a] += race.asi[a]

    ability_scores_p = {}
    for a in ability_scores_raw.keys():
        score = ability_scores_raw[a]
        ability_scores_p[a] = {
            'score': score,
            'modifier': _modifier(score),
        }

    return ability_scores_p

def calculate_armor_class(ability_scores):
    return (10 + ability_scores['DEX']['modifier'])

def calculate_initiative(ability_scores):
    return (ability_scores['DEX']['modifier'])

def calculate_hit_points(ability_scores, classes):
    hit_points = 0
    for c in classes:
        if hit_points <= 0:
            hit_points = c.hit_die + ability_scores['CON']['modifier']
        else:
            hit_points += math.ceil(c.hit_die/2) + ability_scores['CON']['modifier']
    return hit_points

def calculate_hit_dice(classes):
    # A bit more complex because of multiclassing feature
    hit_dice = {}
    for c in classes:
        hit_die = 'd{}'.format(c.hit_die)
        if hit_die not in hit_dice:
            hit_dice[hit_die] = 1
        else:
            hit_dice[hit_die] += 1
    return hit_dice

def calculate_saving_throws(ability_scores, first_class, p_bonus):
    saving_throws = first_class.saving_throws
    saving_throws_p = {}
    for a in ability_scores.keys():
        saving_throws_p[a] = ability_scores[a]['modifier']
        if a in saving_throws:
           saving_throws_p[a] += p_bonus 
    return saving_throws_p

SKILL_PROFICIENCIES = {
    'STR': ['athletics'],
    'DEX': ['acrobatics', 'sleight_of_hand', 'stealth'],
    'CON': [],
    'INT': ['arcana', 'history', 'investigation', 'nature', 'religion'],
    'WIS': ['animal_handling', 'insight', 'medicine', 'perception', 'survival'],
    'CHA': ['deception', 'intimidation', 'performance', 'persuasion'],
}

# TODO may be placed in another class entirely
def calculate_skill_proficiencies(ability_scores, first_class, p_bonus):
    skill_proficiencies = first_class.skills
    skill_proficiencies_p = {}
    for ability in SKILL_PROFICIENCIES.keys():
        for skill in SKILL_PROFICIENCIES[ability]:
            skill_proficiencies_p[skill] = {
                'ability': ability,
            }
            skill_proficiencies_p[skill]['modifier'] = ability_scores[ability]['modifier']
            if skill in skill_proficiencies:
                skill_proficiencies_p[skill]['modifier'] += p_bonus
    return skill_proficiencies_p


"""
A service that generates a character sheet-friendly JSON.
The service's purpose is to aggregate and merge all the different
features from different parts of the PC so that it would be
suitable to use as a character sheet.
"""
class CharacterSheetGenerator(object):
    def __init__(self):
        pass

    def generate_character_sheet(sheet, character):

        # some raw stuff
        p_bonus = character.base.proficiency_bonus
        class_p = character.classes[0].name

        # calculate ability scores
        ability_scores_p = calculate_ability_scores(character.base, character.race)

        # more combat-related scores
        armor_class = calculate_armor_class(ability_scores_p)
        initiative = calculate_initiative(ability_scores_p)
        speed = character.race.speed

        # hit points
        hit_points = calculate_hit_points(ability_scores_p, character.classes)
        hit_dice = calculate_hit_dice(character.classes)

        # saving throws
        saving_throws_p = calculate_saving_throws(ability_scores_p, character.classes[0], p_bonus)

        # skill proficiencies
        skill_proficiencies_p = calculate_skill_proficiencies(ability_scores_p, character.classes[0], p_bonus)

        # add in traits and features
        skill_features = {}
        for c in character.classes:
            skill_features = { **skill_features, **c.features }

        traits = {
            'size': character.race.size,
            'racial_traits': character.race.traits,
            'languages': character.race.languages + character.background.languages,
            'class_features': skill_features,
            'class_proficiencies': character.classes[0].proficiencies,
            'background_feature': character.background.feature,
            'background_proficiencies': character.background.proficiencies,
        }

        # spellcasting, if it exists
        spellcasting_p = {}
        for c in character.classes:
            if c.spellcasting:
                spellcasting_p = c.spellcasting.__json__()

        # the final struct
        j = {
            'name': character.base.name,
            'basic': {
                'race': character.race.name,
                'class': class_p,
                'level': character.base.level,
                'background': character.background.name,
            },
            'proficiency_bonus': p_bonus,
            'ability_scores': ability_scores_p,
            'saving_throws': saving_throws_p,
            'skills': skill_proficiencies_p,
            'combat': {
                'armor_class': armor_class,
                'initiative': initiative,
                'speed': speed,
            },
            'hit_points': {
                'max_hp': hit_points,
                'total_hit_dice': hit_dice,
            },
            'traits_and_features': traits,
            'spellcasting': spellcasting_p,
        }
        return j

