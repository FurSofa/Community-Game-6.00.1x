import random
from attack_setups import weapon_setups


def battle_menu(attacker, enemy_party):
    action = attacker.choose_battle_action(enemy_party).lower()

    if action == 'attack':
        # TODO: make this independent of setup file! (get the setup from the weapon)
        attack_options = [item.attack_name for item in
                          [attacker.equip_slots['Main Hand'], attacker.equip_slots['Off Hand']] if item]

        setup_key = attacker.choose_attack(attack_options)
        setup = weapon_setups[setup_key]
        dmg_done = execute_attack(attacker, enemy_party, **setup)

    elif action == 'show hero stats':
        attacker.party.display_single_member_item_card(attacker)
        battle_menu(attacker, enemy_party)

    elif action == 'heal':
        attacker.heal(attacker.calculate_dmg())


def execute_attack(attacker, target_party, target_num=1, splash_dmg=0,
                   primary=True, primary_percent=100, rnd_target=True,
                   dmg_type='pysical', can_crit=True, is_true_dmg=False,
                   is_heal=False, vamp=0, forced_primary_target=None):
    '''

    :param attacker: npc or subclass
    :param target_party: party
    :param target_num: int: number of targets including primary / 'all' for full target party
    :param splash_dmg: dmg to non primary targets
    :param primary: bool: is there a primary target hit for primary percent
    :param primary_percent: percent of full dmg the primary target is hit for
    :param rnd_target: bool: chooses non primary targets randomly
    :param dmg_type: 'physical' or 'magic'. for dmg generation (and reduction)
    :param can_crit: bool:
    :param is_true_dmg: bool: will ignore defense
    :param is_heal: bool: will add hp, not reduce it. always ignores defense
    :param vamp: int: percentage of dmg dealt affecting attacker hp. can be negative
    :param forced_primary_target:
    :return: int: overall dmg done
    '''


    if target_num == 'all' or target_num > len(target_party.members):
        target_num = len(target_party.members)

    members_list = target_party.members[:]
    dmg_received = 0

    while target_num > 0:
        if primary:
            if forced_primary_target:
                target = forced_primary_target
            else:
                target = attacker.choose_target(members_list)
            dmg_mod = primary_percent
            primary = False
        else:
            dmg_mod = splash_dmg
            if rnd_target:
                target = random.choice(members_list)
            elif target_num < len(members_list):
                target = attacker.choose_target(members_list)
            else:
                target = members_list[0]

        # generate dmg
        is_crit = False
        if dmg_type == 'magic':
            dmg = attacker.int
        else:  # if dmg_type == 'physical':
            dmg = random.randint(attacker.att_dmg_min, attacker.att_dmg_max)
        if can_crit:
            if random.randrange(100) < attacker.crit_chance:
                is_crit = True
                dmg = (dmg * attacker.crit_multiplier) // 100
                print(attacker.name, 'hits a crit!')


        #modify dmg by attack
        dmg_dealt = dmg * dmg_mod // 100

        print('dmg_dealt', dmg_dealt)
        # target take dmg
        if is_true_dmg or is_heal:
            print('is true dmg')
            dmg_done = dmg_dealt
            if is_heal:
                print('is heal')
                dmg_done = -dmg_done
        else:
            if dmg_type == 'magic':
                # TODO: implement magic resi
                dmg_multi = dmg_dealt / (dmg_dealt + (target.int / 4))
            else:
                dmg_multi = dmg_dealt / (dmg_dealt + target.defense)
            dmg_done = round(dmg_dealt * dmg_multi)

        target.hp -= dmg_done

        if not vamp == 0:

            vamp_is_heal = (vamp > 0)
            print('vamp is heal', vamp_is_heal)
            execute_attack(attacker, attacker.party, 1, forced_primary_target=attacker,
                           primary_percent=abs(vamp), is_heal=vamp_is_heal, dmg_type=dmg_type, is_true_dmg=True)

        print(attacker.name, 'hits', target.name, 'for', dmg_dealt, dmg_type, 'dmg and does', dmg_done, 'dmg')

        dmg_received += dmg_done
        members_list.remove(target)
        target_num -= 1
    return dmg_received


# def attack(attacker,)

# attack = {
#     'dmg_type': ['true', 'physical', 'magic'],
#     'dmg': 'amount or range',
#     'is_crit': 'bool',  # or percentage and calc it through that
#     'crit_dmg': 'multiplicator if is_crit',
#     'target': 'person_obj',
#     'target_defense': ['physical', 'magic'],
#     'with_primary': 'bool',
#     'primary_dmg_%': 'int',
#     'num_targets': 'int',
#     'splash_dmg_%': 'int',
# }

#
# def combat(hero_party, enemy_party, person='remove when really coding'):
#     """
#     A start to gathering functions and calculations for combat consolidation
#
#     :param hero_party: first party
#     :param enemy_party: second party
#     :param person: Not needed as a param
#     :return:
#     """
#
#     def alternating_turns(hero_party, enemy_party):
#         # Magic
#         pass
#
#     def choose_target(person, opposing_party):
#         """
#         generates a list of the targets
#         :param person:
#         :param opposing_party:
#         :return: list of targets  # this is so we can use count() later
#         """
#         # put logic for AI here
#         # put hero choice here
#         return []
#
#     def is_crit(pesron) -> bool:
#         _chance = person.crit
#         if _chance < random.randint(1,100):
#             return True
#         else:
#             return False
#
#     def calculate_damage(person, crit=is_crit(person)):
#         damage = person.damage
#         damage_type = person.equip_slots['Main Hand'].weapon_setups[key]
#         crit_multi = person.crit_multiplier
#         if crit:
#             damage = damage * crit_multi // 100
#
#         # if damage_type == 'Magic':
#         #     damage *= (person.int *80//100)
#         # elif damage_type == 'Physical':
#         #     damage *= (person.str * 80 // 100)
#         return damage
#
#
#     def attack_type_logic(not_sure_yet):
#         attack_type = ['single']
#         if attack_type == 'heal':
#             target = select_from_list(person.party)
#         elif attack_type == 'single':
#             choose_target(person='', opposing_party='')
#             # Ect
#         pass
#
#     def unpack_item_stats():
#         pass
#
#     def deal_damage(person, damage=100, damage_type='physical', targets=['list of targets']):
#
#         for target in targets:
#             defense = target.defense[damage_type]
#             dmg_multi = damage / (damage + defense)
#             actual_dmg = round(damage * dmg_multi)
#             target.hp -= actual_dmg
#             print(f'{person.name} deals {actual_dmg} to {target}!')
#
#
#     def heal(pesron,ammount):
#         amount = person.damage()
#         amount, is_crit = amount
#         self.hp += amount
#         if self.hp > self.max_hp:
#             healed_amount = self.max_hp - self.hp
#             self.hp = self.max_hp
#             print(f'{self.name} is fully Healed! HP: {self.hp}/{self.max_hp}')
#         else:
#             healed_amount = amount
#             print(f'{self.name} healed for {amount} hp! HP: {self.hp}/{self.max_hp}')
#         return healed_amount
#
#
#         pass
