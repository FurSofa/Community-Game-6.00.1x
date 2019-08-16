import random
from helper_functions import select_from_list


def deal_multi_dmg(attacker, target_party, target_num='all', splash_dmg=25,
                   primary=True, primary_percent=100, rnd_target=True,
                   dmg_type='pysical'):
    if target_num == 'all' or target_num > len(target_party.members):
        target_num = len(target_party.members)

    members_list = target_party.members[:]
    dmg_received = 0

    # if primary:
    #     print('target choice:')
    #     target = attacker.choose_target(members_list)
    #     print(target.name)
    #     dmg_dealt, is_crit = attacker.calculate_dmg(dmg_type)
    #     dmg_dealt = dmg_dealt * primary_percent // 100
    #     dmg_received += target.take_dmg(dmg_dealt, dmg_type)
    #
    #     print(attacker.display(), 'deals', dmg_received, 'dmg to', target.display())
    #
    #     members_list.remove(target)
    #     target_num -= 1

    while target_num > 0:
        if primary:
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
        dmg_dealt, is_crit = attacker.calculate_dmg(dmg_type)
        if is_crit:
            print('CRIT CRIT CRIT YAY!')
            dmg_dealt = dmg_dealt * dmg_mod // 100
            dmg_received_single = target.take_dmg(dmg_dealt, dmg_type)
        print(attacker.name, 'hits', target.name, 'for', dmg_dealt, dmg_type, 'dmg and does', dmg_received_single,
              'dmg')
        dmg_received += dmg_received_single
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


def combat(hero_party, enemy_party, person='remove when really coding'):
    """
    A start to gathering functions and calculations for combat consolidation

    :param hero_party: first party
    :param enemy_party: second party
    :param person: Not needed as a param
    :return:
    """

    def alternating_turns(hero_party, enemy_party):
        # Magic
        pass

    def choose_target(person, opposing_party):
        """
        generates a list of the targets
        :param person:
        :param opposing_party:
        :return: list of targets  # this is so we can use count() later
        """
        # put logic for AI here
        # put hero choice here
        return []

    def is_crit(pesron) -> bool:
        _chance = person.crit
        if _chance < random.randint(1,100):
            return True
        else:
            return False

    def calculate_damage(person, crit=is_crit(person)):
        damage = person.damage
        damage_type = person.equip_slots['Main Hand'].weapon_setups[key]
        crit_multi = person.crit_muliplier
        if crit:
            damage = damage * crit_multi // 100

        # if damage_type == 'Magic':
        #     damage *= (person.int *80//100)
        # elif damage_type == 'Physical':
        #     damage *= (person.str * 80 // 100)
        return damage


    def attack_type_logic(not_sure_yet):
        attack_type = ['single']
        if attack_type == 'heal':
            target = select_from_list(person.party)
        elif attack_type == 'single':
            choose_target(person='', opposing_party='')
            # Ect
        pass

    def unpack_item_stats():
        pass

    def deal_damage(person, damage=100, damage_type='physical', targets=['list of targets']):

        for target in targets:
            defense = target.defense[damage_type]
            dmg_multi = damage / (damage + defense)
            actual_dmg = round(damage * dmg_multi)
            target.hp -= actual_dmg
            print(f'{person.name} deals {actual_dmg} to {target}!')


    def heal(pesron,ammount):
        amount = person.damage()
        amount, is_crit = amount
        self.hp += amount
        if self.hp > self.max_hp:
            healed_amount = self.max_hp - self.hp
            self.hp = self.max_hp
            print(f'{self.name} is fully Healed! HP: {self.hp}/{self.max_hp}')
        else:
            healed_amount = amount
            print(f'{self.name} healed for {amount} hp! HP: {self.hp}/{self.max_hp}')
        return healed_amount


        pass
