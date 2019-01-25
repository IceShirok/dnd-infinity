
from ddddd.entity import ability_score

ATHLETICS = 'Athletics'

ACROBATICS = 'Acrobatics'
SLEIGHT_OF_HAND = 'Sleight of Hand'
STEALTH = 'Stealth'

ARCANA = 'Arcana'
HISTORY = 'History'
INVESTIGATION = 'Investigation'
NATURE = 'Nature'
RELIGION = 'Religion'

ANIMAL_HANDLING = 'Animal Handling'
INSIGHT = 'Insight'
MEDICINE = 'Medicine'
PERCEPTION = 'Perception'
SURVIVAL = 'Survival'

DECEPTION = 'Deception'
INTIMIDATION = 'Intimidation'
PERFORMANCE = 'Performance'
PERSUASION = 'Persuasion'

SKILL_PROFICIENCIES_BY_ABILITY_SCORE = {
    ability_score.STR: [ATHLETICS],
    ability_score.DEX: [ACROBATICS, SLEIGHT_OF_HAND, STEALTH],
    ability_score.INT: [ARCANA, HISTORY, INVESTIGATION, NATURE, RELIGION],
    ability_score.WIS: [ANIMAL_HANDLING, INSIGHT, MEDICINE, PERCEPTION, SURVIVAL],
    ability_score.CHA: [DECEPTION, INTIMIDATION, PERFORMANCE, PERSUASION],
}
