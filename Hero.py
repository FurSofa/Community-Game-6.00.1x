import person


class Hero(person.Person):
    def __init__(self, name, profession):
        super().__init__(name, profession)
        self.type = 'Hero'

    @classmethod
    def generate(cls, name='Mr. Lazy', profession='Warrior'):
        return cls(name, profession)

    def __str__(self):
        return super().__str__()


p = person.Person.generate('norbnorb', 'Mage')
p.profession_stat_augment()
print(p)

w = Hero.generate('norbnorb', 'Warrior')
w.profession_stat_augment()
print(w)
