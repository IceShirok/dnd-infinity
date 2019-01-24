
import ability_scores

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
    ability_scores.STR: [ATHLETICS],
    ability_scores.DEX: [ACROBATICS, SLEIGHT_OF_HAND, STEALTH],
    ability_scores.INT: [ARCANA, HISTORY, INVESTIGATION, NATURE, RELIGION],
    ability_scores.WIS: [ANIMAL_HANDLING, INSIGHT, MEDICINE, PERCEPTION, SURVIVAL],
    ability_scores.CHA: [DECEPTION, INTIMIDATION, PERFORMANCE, PERSUASION],
}