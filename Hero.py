import person


class Hero(Person):
    def __init__(self, name):
        super().__init__(name, profession)
        self.type = 'Hero'

        # defense stats
        self.base_max_health = 20
        self.current_max_health = self.base_max_health
        self.health = self.current_max_health
        self.base_defense = 0
        self.current_defense = self.base_defense

        # damage relevant stats
        self.base_attack_dmg = 5
        self.current_attack_dmg = self.base_attack_dmg
        self.base_crit_chance = 10
        self.base_crit_modifier = 150

    @classmethod
    def generate(cls):
        return cls(name, profession)
