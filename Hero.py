import person


class Hero(person.Person):
    def __init__(self, name):
        super().__init__(name, profession)
        self.type = 'Hero'


    @classmethod
    def generate(cls,name='Mr. Lazy',profession='Warrior'):
        return cls(name, profession)

    def __str__(self):
        return f'{super().name}'


w = Hero.generate()
print(w)
