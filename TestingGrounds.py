# Testing Grounds!
"""
Use this space to test out features!
"""
from person import Person
from Hero import Hero
from party import Party
from battle import *
from Equipable_Items import *

if __name__ == '__main__':
    print('===  From Test File  ===')
    h = Party()
    h.add_item(Weapon.generate_random())
    h.add_item(Armor.generate_random())
    h.add_item(Armor.generate_random())
    h.show_gear(h.inventory)


def show_stats_2():
    name = f'{self.quality} {self.type}'
    slot = f'{self.equipable_slot.title():>9}'
    line2_left = f'Dur: {self.durability:>2}/{self.max_durability:<2} '
    line2_right = f'Defense: {self.defense}'
    return f'{name:<17}{slot:>13}\n{line2_left:<15}{line2_right:>15}\n'


def show_stats(self):
    name = f'{self.quality} {self.type}'
    slot = f'{self.equipable_slot:>9}'
    dmg = "" if self.att_dmg_max == "NA" else f'{self.att_dmg_min:>3}-{self.att_dmg_max:<3}'
    line2_left = "" if self.durability == "NA" else f'Dur: {self.durability:>2}/{self.max_durability:<2}'
    line2_right = f'Damage: {dmg}' if dmg else ""
    return f'{name:<15}{slot:>15}\n{line2_left:<15}{line2_right:>15}'


hat = item("Dirty", "Hat", "Head", "NA", "NA", "13", "100")
necklace = item("Gold", "Necklace", "Neck", "NA", "NA", "NA", "NA")
sword_of_a_thousand_truths = item("Epic", "Sword", "Main Hand", "100", \
                                  "100", "3000", "3000")

card1 = hat.show_stats()
card2 = necklace.show_stats()
card3 = sword_of_a_thousand_truths.show_stats()
print("┌" + "─" * 32 + "┬" + "─" * 32 + "┬" + "─" * 32 + "┐")
print("\n".join(f'│ {x} │ {y} │ {z} │' for x, y, z in zip(card1.splitlines(),
                                                          card2.splitlines(),
                                                          card3.splitlines())))
print("└" + "─" * 32 + "┴" + "─" * 32 + "┴" + "─" * 32 + "┘")

"""
┌───────────────────────────────┬────────────────────────────────┬───────────────────────────────┐ # len(98)
│Dirty Hat                 Head │ Gold Necklace             Neck │ Epic Sword           Main Hand│
│Dur: 13/100    Damage:  NA-NA  │ Dur: NA/NA     Damage:  NA-NA  │ Dur: 3000/3000 Damage: 100-100│
└───────────────────────────────┴────────────────────────────────┴───────────────────────────────┘
"""
