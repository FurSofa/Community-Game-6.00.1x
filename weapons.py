import random

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

from helper_functions import *

# def deal_multi_dmg(self, target, target_num='all', splash_dmg=25, primary=True, rnd_target=True):
#     if target_num == 'all':
#         target_num = len(target.party.members)
#     members_list = target.party.members[:]
#     dmg_received = 0
#
#     if primary:
#         dmg_dealt = self.calculate_dmg()
#         dmg_received = target.take_dmg(dmg_dealt)
#         print(self.holder, 'deals', dmg_received, 'dmg to', target)
#         members_list.remove(target)
#         target_num -= 1
#
#     while target_num > 0:
#         if rnd_target:
#             target = random.choice(members_list)
#         elif target_num < len(members_list):
#             target = select_from_list(members_list, q='Select next target')
#         else:
#             target = members_list[0]
#         dmg_received2 = target.take_dmg(self.calculate_dmg()*splash_dmg//100)
#         print('and', dmg_received2, 'dmg to', target)
#         dmg_received += dmg_received2
#         members_list.remove(target)
#         target_num -= 1
#     return dmg_received


# def deal_multi_dmg(self, target, target_num='all', splash_dmg=25, primary=True, rnd=True):
#     if target_num == 'all':
#         target_num = len(target.party.members)
#     members_list = target.party.members[:]
#     dmg_received = 0


