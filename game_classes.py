class Party:
    def __init__(self):
        self.members = []
        self.dead_members = []

    @property
    def has_units_left(self) -> bool:
        return len(self.members) > 0

    def remove_dead(self):
        delete_index = []
        for i, member in enumerate(self.members):
            if not member.is_alive:
                delete_index.append(i)
                print(member, 'is dead!')
        for i in reversed(delete_index):
            self.dead_members.append(self.members.pop(i))
        return len(delete_index)

    def add_member(self, member):
        member.party = self
        self.members.append(member)


def battle(party1, party2):
    rounds = 0
    print('A Battle has started!')
    print('Party 1:', party1.members)
    print('Party 2:', party2.members)
    while party1.has_units_left and party2.has_units_left:
        rounds += 1
        print('')
        print('Round:', rounds)
        print('Party 1:', party1.members)
        print('Party 2:', party2.members)
        if party1.has_units_left:
            for member in party1.members:
                print(member, 'has to choose an action.')
                member.choose_action(party2)
                party2.remove_dead()
                if not party2.has_units_left:
                    break
                input('just press enter')
        if party2.has_units_left:
            for member in party2.members:
                member.choose_action(party1)
                party1.remove_dead()
                if not party1.has_units_left:
                    break
                input('just press enter')
    if party1.has_units_left:
        print('Party 1 has won the battle!')
    else:
        print('Party 2 has won the battle!')
