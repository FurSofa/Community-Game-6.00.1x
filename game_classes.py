class Party:
    def __init__(self):
        self.members = []
        self.dead_members = []
        # inventory
        self.inventory = []
        self.equipment = []  # used for armor and weapons
        self.gold = 0

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

    #  inventory and trading
    def change_gold(self, gold_amount):
        #  check if person has enough gold might be better in merchant class
        if self.gold + gold_amount < 0:
            print('Not enough gold!')
            return 'Error'
        self.gold += gold_amount
        return gold_amount


class Battle:
    def __init__(self):
        pass

    def single_unit_turn(self, unit, enemy_party):
        print(unit, 'has to choose an action.')
        unit.choose_battle_action(enemy_party)
        enemy_party.remove_dead()
        return not enemy_party.has_units_left

    def whole_party_turn_battle(self, party_1, party_2):
        rounds = 0
        print('A Battle has started!')
        while party_1.has_units_left and party_2.has_units_left:
            rounds += 1
            print('')
            print('Round:', rounds)
            print('Party 1:', party_1.members)
            print('Party 2:', party_2.members)
            if party_1.has_units_left:
                for member in party_1.members:
                    no_enemies_left = self.single_unit_turn(member, party_2)
                    if no_enemies_left:
                        break
                    input('just press enter')
            if party_2.has_units_left:
                for member in party_2.members:
                    no_enemies_left = self.single_unit_turn(member, party_1)
                    if no_enemies_left:
                        break
                    input('just press enter')
        if party_1.has_units_left:
            print('Party 1 has won the battle!')
        else:
            print('Party 2 has won the battle!')
        return party_1.has_units_left

    def alternating_turn_battle(self, party_1, party_2):
        rounds = 0
        print('A Battle has started!')
        while party_1.has_units_left and party_2.has_units_left:
            rounds += 1
            print('')
            print('Round:', rounds)
            print('Party 1:', party_1.members)
            print('Party 2:', party_2.members)
            for i in range(max(len(party_1.members), len(party_2.members))):
                if i < len(party_1.members):
                    no_enemies_left = self.single_unit_turn(party_1.members[i], party_2)
                    if no_enemies_left:
                        break
                    input('just press enter')
                if i < len(party_2.members):
                    no_enemies_left = self.single_unit_turn(party_2.members[i], party_1)
                    if no_enemies_left:
                        break
                    input('just press enter')
        if party_1.has_units_left:
            print('Party 1 has won the battle!')
        else:
            print('Party 2 has won the battle!')
        return party_1.has_units_left
