import math

"""
Common functions
"""


def modifier(score):
    # Calculates the ability modifier
    return math.floor((score-10)/2)


def prettify_modifier(mod):
    # Function used to add a + to positive score, - to negative score,
    # or do nothing to a 0. Used for visual purposes.
    if mod > 0:
        return '+{}'.format(mod)
    else:
        return str(mod)


# ABILITY SCORES

STR = 'STR'
DEX = 'DEX'
CON = 'CON'
INT = 'INT'
WIS = 'WIS'
CHA = 'CHA'
