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

    @property
    def members_names(self):
        return ', '.join(member.name for member in self.members)

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