
import math


def _modifier(score):
    return math.floor((score-10)/2)

def _modifier_p(score):
    mod = _modifier(score)
    if mod > 0:
        return '+{}'.format(mod)
    else:
        return str(mod)

class CharacterSheetGenerator(object):
    def __init__(self):
        pass

    def generate_character_sheet(sheet, character):

        # some raw stuff
        p_bonus = character.base.proficiency_bonus

        # calculate ability scores
        ability_scores_raw = [
            ('STR', character.base._str),
            ('DEX', character.base._dex),
            ('CON', character.base._con),
            ('INT', character.base._int),
            ('WIS', character.base._wis),
            ('CHA', character.base._cha),
        ]
        ability_scores_p = {}
        for a in ability_scores_raw:
            ability_scores_p[a[0]] = {
                'score': a[1],
                'modifier': _modifier(a[1]),
            }

        # more combat-related scores
        armor_class = 10 + ability_scores_p['DEX']['modifier']
        initiative = ability_scores_p['DEX']['modifier']
        speed = character.race.speed

        # hit points
        hit_points = 0
        for c in character.classes:
            if hit_points <= 0:
                hit_points = c.hit_die + ability_scores_p['CON']['modifier']
            else:
                hit_points += math.ceil(c.hit_die/2) + ability_scores_p['CON']['modifier']
        hit_dice = '{}d{}'.format(len(character.classes), character.classes[0].hit_die)

        # saving throws
        saving_throws = character.classes[0].saving_throws
        saving_throws_p = {}
        for a in ability_scores_p.keys():
            saving_throws_p[a] = ability_scores_p[a]['modifier']
            if a in saving_throws:
               saving_throws_p[a] += p_bonus 

        # skill proficiencies
        skillz = {
            'STR': ['athletics'],
            'DEX': ['acrobatics', 'sleight_of_hand', 'stealth'],
            'CON': [],
            'INT': ['arcana', 'history', 'investigation', 'nature', 'religion'],
            'WIS': ['animal_handling', 'insight', 'medicine', 'perception', 'survival'],
            'CHA': ['deception', 'intimidation', 'performance', 'persuasion'],
        }
        mad_skills = character.classes[0].skills
        sweet_skills = {}
        for ability in skillz.keys():
            for skill in skillz[ability]:
                sweet_skills[skill] = {
                    'ability': ability,
                }
                if skill in mad_skills:
                    sweet_skills[skill]['modifier'] = ability_scores_p[ability]['modifier'] + p_bonus
                else:
                    sweet_skills[skill]['modifier'] = ability_scores_p[ability]['modifier']

        # the final struct
        j = {
            'name': character.base.name,
            'basic': {
                'race': character.race.name,
                'class': character.classes[0].name,
                'level': character.base.level,
                'background': character.background.name,
            },
            'ability_scores': ability_scores_p,
            'saving_throws': saving_throws_p,
            'skills': sweet_skills,
            'combat': {
                'armor_class': armor_class,
                'initiative': initiative,
                'speed': speed,
            },
            'hit_points': {
                'max_hp': hit_points,
                'total_hit_dice': hit_dice,
            }
        }
        return j

