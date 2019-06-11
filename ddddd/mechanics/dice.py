
import random


def roll_die(max_val):
    return random.randint(1, max_val)


def roll_d6():
    return roll_die(6)


def roll_d20():
    return roll_die(20)


def roll_ability_score():
    values = []
    for _ in range(0, 4):
        values.append(roll_d6())
    min_value = min(values)
    return sum(values) - min_value
