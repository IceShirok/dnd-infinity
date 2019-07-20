
class EntityWithInitiative(object):
    def initiative(self):
        raise NotImplementedError


class SimpleEntity(EntityWithInitiative):
    def __init__(self, name, initiative_mod):
        self.name = name
        self.initiative_mod = initiative_mod

    def initiative(self):
        return self.initiative_mod


class InitiativeEntity(object):
    def __init__(self, entity, initiative):
        self.entity = entity
        self.initiative = initiative

    def __eq__(self, other):
        if not isinstance(other, InitiativeEntity):
            return NotImplemented
        return self.entity == other.entity

    def __str__(self):
        return '{} - {}'.format(self.entity, self.initiative)


class InitiativeTracker(object):
    def __init__(self):
        self.entities = list()
        self.round = 1

        self.turn_pointer = None

    def sort(self):
        def sort_by_initiative(ie):
            return ie.initiative
        self.entities.sort(key=sort_by_initiative, reverse=True)

    def add_entity(self, entity, initiative=None):
        if not initiative:
            initiative = 20
        self.entities.append(InitiativeEntity(entity, initiative))
        self.sort()

    def reset_combat(self):
        self.round = 1
        self.turn_pointer = 0

    def next_turn(self):
        if self.turn_pointer + 1 >= len(self.entities):
            self.round += 1
            self.turn_pointer = 0
        else:
            self.turn_pointer += 1

    def get_current_entity(self):
        return self.entities[self.turn_pointer]

    def get_intiative_order(self):
        return self.entities


def initiative_tracker():
    init_tracker = InitiativeTracker()
    entities_raw = [
        ('Brother Hadad', 7),
        ('Cheese', 14),
        ('Solomon King', 13),
        ('Lawrence', 21),
        ('Fethri Winterwhisper', 17),
        ('Cake Monster', 5),
    ]
    for entity, initiative in entities_raw:
        init_tracker.add_entity(entity, initiative)

    def print_init_tracker():
        entities = init_tracker.get_intiative_order()
        print('ROUND {}'.format(init_tracker.round))
        for e in entities:
            if init_tracker.get_current_entity() == e:
                print('---> {}'.format(e))
            else:
                print('     {}'.format(e))

    init_tracker.reset_combat()
    while True:
        print_init_tracker()
        user_input = input('What would you like to do? (exit, etc) > ')
        if user_input == 'exit':
            break
        else:
            init_tracker.next_turn()
        print('-----')
    print('goodbye')


if __name__ == '__main__':
    initiative_tracker()
