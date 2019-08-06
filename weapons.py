import random
import Equipable_Items

# TODO: Add weapon variations based on the 'Weapon' class from Base_Item_classes

# class Sword(Weapon):
#     def __init__(self, dmg, defense):
#         super().__init__(dmg, defense)
#         self.attack_dmg = dmg
#         self.defense = defense
#         self.crit_chance = 5
#         self.crit_dmg = 25
#         self.name = 'Sword'
#
#
# class Axe(Weapon):
#     def __init__(self, dmg, defense):
#         super().__init__(dmg, defense)
#         self.attack_dmg = dmg
#         self.defense = defense
#         self.name = 'Axe'
#
#     def deal_dmg(self, target):
#         dmg_dealt = self.holder.calculate_dmg()
#         dmg_received = target.take_dmg(dmg_dealt)
#         print(self.holder, 'deals', dmg_received, 'dmg to', target)
#         if len(target.party.members) > 1:
#             members_list = target.party.members
#             members_list.remove(target)
#             target2 = random.choice(members_list)
#             dmg_received2 = target2.take_dmg(self.holder.calculate_dmg()//2)
#             print('and', dmg_received2, 'dmg to', target2)
#             dmg_received += dmg_received2
#         return dmg_received
