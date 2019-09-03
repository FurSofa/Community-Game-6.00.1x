import random
import pandas as pd
import numpy as np
import copy
import json


def increase_after_steps(start=0, step=10, increment=1, length=100, factor=1):
    range_2 = length * increment // step
    return [y+start for x in [[i * factor for e in range(step)] for i in range(0,range_2,increment)] for y in x]


class DGame:
    def __init__(self, difficulty):
        self.difficulty = difficulty


dummy_game = DGame('Easy')


class Party:
    def __init__(self, char, game=dummy_game):
        self.hero = None
        self.members = []
        self.dead_members = []
        # inventory
        self.inventory = []
        self.equipment = []  # used for armor and weapons
        self.gold = 0

        self.game = game
        self.members.append(char)

    def __str__(self):
        return 'h: ' + str(self.hero()) + ' ' + str(self.members)

    @classmethod
    def generate(cls, char ,game=dummy_game):
        game = DGame('Easy')
        return cls(char, game)

    @classmethod
    def __del__(cls):
        del cls

    @property
    def has_units_left(self) -> bool:
        """
        checks if active members are left
        :return: True if any party member is alive
        """
        return len(self.members) > 0

    def remove_dead(self):
        """
        removes dead players from active members and places them in dead members
        :return: number of members found dead
        """
        delete_index = []
        for i, member in enumerate(self.members):
            if not member.is_alive:
                delete_index.append(i)
                # print(member.name, 'is dead!')
        for i in reversed(delete_index):
            self.dead_members.append(self.members.pop(i))
        return len(delete_index)

    def add_member(self, member):
        """
        adds a member to the party
        :param member: NPC or Hero class object
        :return:
        """
        print(f'{member.name}, the {member.profession} joins the party!')
        member.party = self
        self.members.append(member)
        if member.hero:
            self.hero = member


class NPC:
    def __init__(self, name, lvl, vit, dex, str, int, speed, hp, p_dmg,
                 crit_chan, crit_dmg, m_dmg, b_dmg, crit_hit, avg_dmg,
                 armor, dodge, attack_setup):
        self.lvl = lvl
        self.vit = vit
        self.dex = dex
        self.str = str
        self.int = int
        self.speed = speed
        self.hp = hp
        self.p_dmg = p_dmg
        self.crit_chance = crit_chan
        self.crit_dmg = crit_dmg
        self.m_dmg = m_dmg
        self.b_dmg = b_dmg
        self.crit_hit = crit_hit
        self.avg_dmg = avg_dmg

        self.armor = armor
        self.dodge = dodge
        self.name = name

        self.max_hp = self.hp
        self.c = 0
        self.ct = 100
        self.party = Party.generate(self)
        self.attack_setup = attack_setup
        self.crit_multiplier = self.crit_dmg
        self.level = self.lvl

    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    def __repr__(self):
        return str(f'{self.name}')  # , {self.level}')

    def __str__(self):
        return str(f'{self.name}')  # , {self.level}')

    def set_hp(self, amount):
        """
        set the hp safely
        :param amount: int: to change / can be positive or negative
        :return: amount
        """
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        if self.hp < 0:
            self.hp = 0
        return amount

    def choose_target(self, target_party):
        """
        picks random target from target_party.members
        :param target_party: party instance
        :return: person from party
        """
        if len(target_party) > 1:
            if self.party.has_hero() or self.party.game.difficulty == 'Medium':
                choice = random.randrange(len(target_party))
                target = target_party[choice]
            else:
                if self.party.game.difficulty == 'Hard':
                    target = min(target_party, key=lambda member: member.hp)
                elif self.party.game.difficulty == 'Easy':
                    target = max(target_party, key=lambda member: member.hp)
        else:
            target = target_party[0]
        return target

    def choose_attack(self, attack_options):
        choice = random.choice(attack_options)
        return choice

    def choose_battle_action(self, enemy_party):
        """
        ENDPOINT for battle
        npc will always choose basic attack
        :param enemy_party:
        :return: -
        """
        return 'attack'


def mk_unit_d3(df):
    attack_setup = full_setup_d3
    unit = NPC(df['u_name'], df['lvl'], df['vit'], df['dex'], df['str'], df['int'], df['speed'], df['hp'], df['p_dmg'], df['crit_chan'], df['crit_dmg'], df['m_dmg'], df['b_dmg'], df['crit_hit'], df['avg_dmg'], df['armor'], df['dodge'], attack_setup)
    return unit


def mk_unit_lol(df):
    attack_setup = full_setup_lol
    unit = NPC(df['u_name'], df['lvl'], df['vit'], df['dex'], df['str'], df['int'], df['speed'], df['hp'], df['p_dmg'], df['crit_chan'], df['crit_dmg'], df['m_dmg'], df['b_dmg'], df['crit_hit'], df['avg_dmg'], df['armor'], df['dodge'], attack_setup)
    return unit


def add_units(fight_df, cl_df_list):

    for cls_df in cl_df_list:
        name_str = cls_df.name

        fight_df['unit_' + str(name_str) + '_d3'] = cls_df.apply(mk_unit_d3, axis=1)
        fight_df['unit_' + str(name_str) + '_lol'] = cls_df.apply(mk_unit_lol, axis=1)
    return fight_df


def calc_fights(fight_df):
    fight_units = fight_df.copy()
    fight_units['dex_v_str_d3'] = fight_units[['unit_dex_cl_d3', 'unit_str_cl_d3']].apply(fight, axis=1)
    fight_units['int_v_str_d3'] = fight_units[['unit_int_cl_d3', 'unit_str_cl_d3']].apply(fight, axis=1)
    fight_units['int_v_dex_d3'] = fight_units[['unit_int_cl_d3', 'unit_dex_cl_d3']].apply(fight, axis=1)

    fight_units['dex_v_str_lol'] = fight_units[['unit_dex_cl_lol', 'unit_str_cl_lol']].apply(fight, axis=1)
    fight_units['int_v_str_lol'] = fight_units[['unit_int_cl_lol', 'unit_str_cl_lol']].apply(fight, axis=1)
    fight_units['int_v_dex_lol'] = fight_units[['unit_int_cl_lol', 'unit_dex_cl_lol']].apply(fight, axis=1)
    return fight_units


def clock_battle_test(party1, party2):
    p1_won = clock_tick_battle(party1, party2)
    if p1_won:
        winner = party1.members[0]
    else:
        winner = party2.members[0]
    return winner


def run_clock_battle(unit1, unit2):
    p1 = unit1.party
    p2 = unit2.party
    return clock_battle_test(p1, p2)


def fight(row):
    u1 = copy.deepcopy(row[0])
    u2 = copy.deepcopy(row[1])
    return run_clock_battle(u1, u2)


def single_unit_turn(unit, enemy_party):
    action = run_attack(unit, enemy_party, **unit.attack_setup)
    enemy_party.remove_dead()
    return 'attack'


def check_crit(attacker, can_crit):
    return (random.randrange(100) < attacker.crit_chance) if can_crit else False


def check_dodge(target, can_dodge):
    return (random.randrange(100) < target.dodge) if can_dodge else False


def generate_dmg(attacker, target, dmg_base='str_based', is_crit=False,
                 wpn_dmg_perc=100, c_hp_perc_dmg=0, max_hp_perc_dmg=0):

    c_hp_dmg = target.hp / 100 * c_hp_perc_dmg
    max_hp_dmg = target.max_hp / 100 * max_hp_perc_dmg
    # if dmg_base == 'int_based':
    #     wpn_dmg = attacker.m_dmg
    # else:  # if dmg_base == 'str_based':
    #     wpn_dmg = random.randint(attacker.att_dmg_min, attacker.att_dmg_max)
    wpn_dmg = attacker.b_dmg
    wpn_dmg = wpn_dmg / 100 * wpn_dmg_perc

    dmg = sum([c_hp_dmg, max_hp_dmg, wpn_dmg])
    if is_crit:
        dmg = (dmg * attacker.crit_multiplier) // 100
    return round(dmg)


def defense_calc(attacker, dmg, target, elemental, reduction_calc):
    # TODO: generalise resistances
    # if not elemental == 'physical':
    #     dmg_multi = dmg / (dmg + target.__dict__[elemental + '_res'])
    # else:
    #     dmg_multi = dmg / (dmg + target.defense)
    # dmg_done = round(dmg * dmg_multi)
    # if elemental == 'physical':  # untill we have the new npc
    defense = target.armor
    # else:
        # defense = target.__dict__[elemental + '_res']

    if reduction_calc == 'classic':
        if defense > dmg:
            dmg_done = 0
        else:
            dmg_done = dmg - defense
    elif reduction_calc == 'd3':
        dmg_reduction = (target.armor / (target.armor + attacker.level * 5)) * 100
        dmg_done = dmg / 100 * (100 - dmg_reduction)

    elif reduction_calc == 'lol':
        if target.armor < 0:
            dmg_multi = 2 - (100 / (100 - target.armor))
        else:
            dmg_multi = 100 / (100 + target.armor)
        dmg_done = dmg_multi * dmg
    else:
        raise ValueError('No reduction_calc set! use "lol", "d3" or "classic" in attack setup.')
    if elemental == 'true':
        dmg_done = dmg
    if elemental == 'heal':   # * -1 if heal
        dmg_done = -dmg_done
    return round(dmg_done)


def get_target(attacker, primary, forced_primary_target,
               target_num, members_list, rnd_target):
    if primary:
        if forced_primary_target:
            target = forced_primary_target
        else:
            target = attacker.choose_target(members_list)
    else:
        if rnd_target:
            target = random.choice(members_list)
        elif target_num < len(members_list):
            target = attacker.choose_target(members_list)
        else:
            target = members_list[0]
    return target


# TODO: add a function to modify setup based on player stats and percs once we have that before running attack?
def run_attack(attacker, target_party, target_num=1, primary=True, primary_percent=100,
               rnd_target=True, forced_primary_target=None, splash_dmg=0,
               elemental='physical', vamp=0, can_crit=True, dmg_base='str_based',
               wpn_dmg_perc=100, c_hp_perc_dmg=0, max_hp_perc_dmg=0, can_dodge=True, reduction_calc='d3'):
    """

    :param attacker: npc or subclass
    :param target_party: party
    :param target_num: int: number of targets including primary / 'all' for full target party
    :param primary: bool: is there a primary target hit for primary percent
    :param primary_percent: percent of full dmg the primary target is hit for
    :param rnd_target: bool: chooses non primary targets randomly
    :param forced_primary_target: npc or subclass: used as primary target
    :param splash_dmg: dmg to non primary targets
    :param elemental: dmg type used to calculate and apply dmg / special for 'heal'(inverts dmg) and 'true'(ignores defense)
    :param vamp: int: percentage of dmg dealt affecting attacker hp. can be negative
    :param can_crit: bool:
    :param dmg_base: 'str_based' or 'int_based'. for dmg generation
    :param max_hp_perc_dmg: int: percent of target max hp as dmg
    :param c_hp_perc_dmg: int: percent of target current hp as dmg
    :param wpn_dmg_perc: int: percentage modifier for weapon dmg / set to 0 if you want only target hp pool based dmg
    :return: int: overall dmg done
    """
    members_list = attacker.party.members[:] if elemental == 'heal' else target_party.members[:]

    if target_num == 'all' or target_num > len(members_list):
        target_num = len(members_list)

    dmg_combined = 0
    while target_num > 0:
        dmg_mod = primary_percent if primary else splash_dmg
        target = get_target(attacker, primary, forced_primary_target, target_num,
                            members_list, rnd_target)
        primary = False
        is_crit = check_crit(attacker, can_crit)
        raw_dmg = generate_dmg(attacker, target, dmg_base, is_crit, wpn_dmg_perc,
                               c_hp_perc_dmg, max_hp_perc_dmg, )  # value for full dmg before and mod or reduction

        #  other modification, not really generation, not really defense reduction
        dmg_dealt = raw_dmg * dmg_mod // 100  # modify for splash or primary dmg factor
        is_dodge = check_dodge(target, can_dodge)
        if is_dodge:
            pass
            # print(f'{target.name} dodged!')
        else:
            dmg_received = defense_calc(attacker, dmg_dealt, target, elemental, reduction_calc)
            target.set_hp(-dmg_received)

            if not vamp == 0:
                run_attack(attacker, attacker.party, 1, forced_primary_target=attacker,
                           primary_percent=vamp, dmg_base=dmg_base, elemental='heal',
                           reduction_calc=reduction_calc, can_dodge=False)

            dmg_combined += dmg_received

            verb = 'healed' if dmg_received < 0 else 'hit'
            crit_str = ' with a crit!' if is_crit else '.'
            # print(f'{attacker.name} {verb} {target.name} for {abs(dmg_dealt)} pts{crit_str} {dmg_received} stuck.')
        members_list.remove(target)
        target_num -= 1
    return dmg_combined


def clock_tick(party_1, party_2):
    all_members = party_1.members + party_2.members
    for member in all_members:
        member.c += member.speed
    all_members = sorted(all_members, key=lambda m: m.c, reverse=True)

    # [print(f'c: {member.c} - name: {member.name}') for member in all_members]
    return all_members


def clock_tick_battle(party_1, party_2):
    parties = [party_1, party_2]
    # print('A Battle has started!')
    c_ticks = 0
    for member in party_1.members + party_2.members:
        member.ct = 1000
        member.c = 0

    while party_1.has_units_left and party_2.has_units_left:
        all_members = clock_tick(party_1, party_2)
        c_ticks += 1
        # print(f'ticks: {c_ticks}')
        for member in all_members:
            if member.c > member.ct:
                # print(f'its {member.name}\'s turn!')
                both_parties = parties.copy()
                both_parties.remove(member.party)
                enemy_party = both_parties[0]
                action_taken = single_unit_turn(member, enemy_party)
                if action_taken == 'attack':
                    member.c = 0
                    member.ct = 1000
                elif action_taken == 'heal':
                    member.c = 0
                    member.ct = 800
                elif action_taken == 'skip turn':
                    pass
                if not enemy_party.has_units_left:
                    break
    # if party_1.has_units_left:
    #     # print('Party 1 has won the battle!')
    # else:
    #     # print('Party 2 has won the battle!')
    for m in party_1.members + party_2.members:
        m.__dict__['ct_to_win'] = c_ticks
    return party_1.has_units_left


def c_vit_to_hp(df, start, hp_per_vit, hp_per_lvl):
    df['hp'] = (df['vit'] * hp_per_vit) + (df['lvl'] * hp_per_lvl) + start
    return df


def c_str_to_dmg(df, wpn_dmg, b_dmg_wpn_dmg_factor, start, dmg_per_level, dmg_per_str):
    df['p_dmg_wo_wpn'] = (df['str'] * dmg_per_str) + (df['lvl'] * dmg_per_level)
    df['p_dmg'] = round((df['p_dmg_wo_wpn'] / 100) * b_dmg_wpn_dmg_factor * wpn_dmg, 2) + wpn_dmg + start
    return df


def c_int_to_dmg(df, wpn_dmg, b_dmg_wpn_dmg_factor, start, dmg_per_level, dmg_per_int):
    df['m_dmg_wo_wpn'] = (df['int'] * dmg_per_int) + (df['lvl'] * dmg_per_level)
    df['m_dmg'] = round((df['m_dmg_wo_wpn'] / 100) * b_dmg_wpn_dmg_factor * wpn_dmg, 2) + wpn_dmg + start
    return df


def c_dex_to_dmg(df, wpn_dmg, b_dmg_wpn_dmg_factor, start, dmg_per_level, dmg_per_dex):
    df['d_dmg_wo_wpn'] = (df['dex'] * dmg_per_dex) + (df['lvl'] * dmg_per_level)
    df['d_dmg'] = round((df['d_dmg_wo_wpn'] / 100) * b_dmg_wpn_dmg_factor * wpn_dmg, 2) + wpn_dmg + start
    return df


def c_set_dmg(df):

    cond_list = [
        (df['m_dmg'] > df['p_dmg']) & (df['m_dmg'] > df['d_dmg']),
        (df['m_dmg'] < df['p_dmg']) & (df['d_dmg'] < df['p_dmg']),
        (df['m_dmg'] < df['d_dmg']) & (df['p_dmg'] < df['d_dmg']),
    ]
    choice_list = [df['m_dmg'], df['p_dmg'], df['d_dmg']]
    df['b_dmg'] = np.select(cond_list, choice_list)

    # df['b_dmg'] = max(df['m_dmg'], df['d_dmg'], df['p_dmg'])
    return df

# def c_set_dmg_w_wpn(df, wpn_dmg, b_dmg_wpn_dmg_factor):
#     df['b_dmg'] = df['dmg_wo_wpn'] / 100 * b_dmg_wpn_dmg_factor * wpn_dmg


def c_str_to_armor(df, start, armor_per_level, armor_per_str):
    df['str_armor'] = (df['str'] * armor_per_str) + (df['lvl'] * armor_per_level) + start
    return df


def c_toughness_to_armor(df, armor_per_toughness):
    df['armor'] = (df['toughness'] * armor_per_toughness) + df['str_armor']
    return df


def c_dex_speed_to_dodge(df, start, dodge_per_speed, dodge_per_dex):
    df['dodge'] = (df['dex'] * dodge_per_dex) + (df['speed'] * dodge_per_speed) + start
    return df


def c_dex_to_crit(df, chance_start, crit_chan_per_level, crit_chan_per_dex,
                  dmg_start, crit_dmg_per_level, crit_dmg_per_dex):
    df['crit_chan'] = (df['dex'] * crit_chan_per_dex) + (df['lvl'] * crit_chan_per_level) + chance_start
    df['crit_dmg'] = (df['dex'] * crit_dmg_per_dex) + (df['lvl'] * crit_dmg_per_level) + dmg_start
    return df


def c_avg_dmg(df):
    df['crit_hit'] = df['b_dmg'] * (df['crit_dmg'] / 100)
    df['avg_dmg'] = (df['crit_hit'] / 100) * df['crit_chan'] + df['b_dmg'] / 100 * (100 - df['crit_chan'])
    return df


def c_dex_to_speed(df, speed_per_dex,speed_per_agility, speed_factor, speed_start):
    ct = 1000
    df['speed'] = (df['dex'] * speed_per_dex) + (df['agility'] * speed_per_agility) * speed_factor + speed_start
    df['ticks_to_turn'] = round(ct / df['speed'], 2)
    return df


def c_avg_dmg_p_ticks(df):
    df['dpt100'] = round(df['avg_dmg'] * (100 / df['ticks_to_turn']), 2)
    return df


def c_d3_armor_reduction(df):
    df['d3_res_reduction'] = (df['armor'] / (df['armor'] + df['lvl'] * 5)) * 100
    df['d3_res_dmg_taken'] = df['dpt100'] / 100 * (100 - df['d3_res_reduction'])
    return df


def c_lol_res_reduction(df):
    lol_multi_cond = [df['armor'] < 0, df['armor'] >= 0]
    lol_neg_def = 2 - (100 / (100 - df['armor']))
    lol_pos_def = 100 / (100 + df['armor'])

    df['dmg_multi_lol'] = np.select(lol_multi_cond, [lol_neg_def, lol_pos_def])
    df['lol_dmg_taken'] = df['dmg_multi_lol'] * df['dpt100']
    return df


def c_avg_dmg_redu_dodge(df):
    df['lol_dmg_redu_dodge'] = df['lol_dmg_taken'] * (1 - (df['dodge'] / 100))
    df['d3_dmg_redu_dodge'] = df['d3_res_dmg_taken'] * (1 - (df['dodge'] / 100))
    return df


def c_ehp(df):
    df['lol_ehp'] = ((1 - df['dmg_multi_lol']) + (1 - (df['dodge'] / 100))) * df['hp'] + df['hp']
    df['d3_ehp'] = ((df['d3_res_reduction']) + (1 - (df['dodge'] / 100))) * df['hp'] + df['hp']
    return df


def derive_stats(df_list, vit_to_hp, str_to_dmg, toughness_to_armor, int_to_dmg, dex_to_dmg, str_to_armor, dex_speed_to_dodge, dex_to_crit,
                 wpn_dmg, b_dmg_wpn_dmg_factor, wpn_dmg_growth_per_lvl, dex_to_speed):
    for cl_df in df_list:
        wpn_dmg = wpn_dmg + (wpn_dmg * (wpn_dmg_growth_per_lvl / 100))
        c_dex_to_speed(cl_df, **dex_to_speed)
        c_vit_to_hp(cl_df, **vit_to_hp)
        c_str_to_dmg(cl_df, wpn_dmg, b_dmg_wpn_dmg_factor, **str_to_dmg)
        c_dex_to_dmg(cl_df, wpn_dmg, b_dmg_wpn_dmg_factor, **dex_to_dmg)
        c_int_to_dmg(cl_df, wpn_dmg, b_dmg_wpn_dmg_factor, **int_to_dmg)
        c_dex_to_crit(cl_df, **dex_to_crit)
        c_set_dmg(cl_df)
        c_avg_dmg(cl_df)
        c_avg_dmg_p_ticks(cl_df)
        c_str_to_armor(cl_df, **str_to_armor)
        c_toughness_to_armor(cl_df, **toughness_to_armor)
        c_dex_speed_to_dodge(cl_df, **dex_speed_to_dodge)
        c_d3_armor_reduction(cl_df)
        c_lol_res_reduction(cl_df)
        c_avg_dmg_redu_dodge(cl_df)
        c_ehp(cl_df)
    return df_list


def mk_single_class_df(levels, start,
                       vit_start, vit_p_lvl,
                       dex_start, dex_p_lvl,
                       str_start, str_p_lvl,
                       int_start, int_p_lvl,
                       agility_start, agility_p_lvl,
                       toughness_start, toughness_p_lvl ):

    df = pd.DataFrame({
        'lvl': increase_after_steps(1, 1, 1, levels, 1),
        'vit': increase_after_steps(vit_start, 1, 1, levels, vit_p_lvl),
        'dex': increase_after_steps(dex_start, 1, 1, levels, dex_p_lvl),
        'str': increase_after_steps(str_start, 1, 1, levels, str_p_lvl),
        'int': increase_after_steps(int_start, 1, 1, levels, int_p_lvl),
        'agility': increase_after_steps(agility_start, 1, 1, levels, agility_p_lvl),
        'toughness': increase_after_steps(toughness_start, 1, 1, levels, toughness_p_lvl),
    })
    return df


def mk_class_dfs(level, start, classes):
    class_list = []
    for key in classes.keys():
        cls_base_stats_setup = classes.get(key)
        df = mk_single_class_df(level, start, **cls_base_stats_setup)
        df['u_name'] = key[:-3]
        df.name = key[:-3]
        class_list.append(df)

    return class_list


def create_cl_stats(cl_base_stats, conversion_ratios):
    class_list = mk_class_dfs(**cl_base_stats)
    cls_dfs_list = derive_stats(class_list, **conversion_ratios)
    return cls_dfs_list


def rename_cols_concat(cl_df_list):
    cl_df_list_copy = []
    for cl_df in cl_df_list:
        rename_dict = {}
        cl_df_copy = cl_df.copy()
        cols = cl_df_copy.columns
        new_cols = [c + '_' + cl_df.name[:3] for c in cols]
        for old_c, new_c in zip(cols, new_cols):
            rename_dict[old_c] = new_c
        cl_df_copy.rename(columns=rename_dict, inplace=True)
        cl_df_list_copy.append(cl_df_copy)
    all_cl_df = pd.concat(cl_df_list_copy, axis=1)
    return all_cl_df


def get_unit_attribute(df, attribute):
    """

    :param df: dataframe
    :param attribute: string or list of strings
    :return: df
    """
    if isinstance(attribute, list):
        return df.apply(lambda row: [[unit.__dict__[a] for a in attribute] for unit in row])
    else:
        return df.apply(lambda row: [unit.__dict__[attribute] for unit in row])


def get_cl_suffixes(cl_df_list):
    cl_suffixes = []
    for df in cl_df_list:
        suffix = '_' + df.name[:3]
        cl_suffixes.append(suffix)
    return cl_suffixes





# running the stuff
low_start = {
    # base stats and their growth per class
    'cl_base_stats': {
        'level': 30,                        # levels the calculations are run for
        'start': 4,                         # ignore this
        'classes': {                        # set the stat growth of each class here
            'dex_class': {
                'vit_start': 4,
                'vit_p_lvl': 2,

                'dex_start': 4,
                'dex_p_lvl': 3,

                'str_start': 4,
                'str_p_lvl': 1,

                'int_start': 4,
                'int_p_lvl': 1,
            },
            'str_class': {
                'vit_start': 4,
                'vit_p_lvl': 2,

                'dex_start': 4,
                'dex_p_lvl': 1,

                'str_start': 4,
                'str_p_lvl': 3,

                'int_start': 4,
                'int_p_lvl': 1,
            },
            'int_class': {
                'vit_start': 4,
                'vit_p_lvl': 1,

                'dex_start': 4,
                'dex_p_lvl': 2,

                'str_start': 4,
                'str_p_lvl': 1,

                'int_start': 4,
                'int_p_lvl': 3,
            },
        }
    },
    # ratios for derived stats
    'conversion_ratios': {
        'wpn_dmg': 20,                      # base weapon dmg
        'b_dmg_wpn_dmg_factor': 50,         # percent of base dmg * weapon dmg
        'wpn_dmg_growth_per_lvl': 20,       # percent the weapon dmg grows per level
        'vit_to_hp': {
            'start': 1200,
            'hp_per_vit': 45,
            'hp_per_lvl': 15,
        },
        'str_to_dmg': {
            'start': 5,
            'dmg_per_level': 0.7,
            'dmg_per_str': 0.7,
        },
        'int_to_dmg': {
            'start': 5,
            'dmg_per_level': 0.6,
            'dmg_per_int': 0.9,
        },
        'str_to_armor': {
            'start': 3,
            'armor_per_level': 1,
            'armor_per_str': 5,
        },
        'dex_speed_to_dodge': {
            'start': 3,
            'dodge_per_speed': 0.6,
            'dodge_per_dex': 0.6,
        },
        'dex_to_crit': {
            'chance_start': 5,
            'crit_chan_per_level': 0.2,
            'crit_chan_per_dex': 0.7,

            'dmg_start': 125,
            'crit_dmg_per_level': 1,
            'crit_dmg_per_dex': 3,
        },
        'dex_to_speed': {
            'speed_per_dex': 0.3,
            'speed_per_lvl': 0.2,
            'speed_start': 9,
        },
    }
}


char_creation_setup = {
    # base stats and their growth per class
    'cl_base_stats': {
        'level': 30,                        # levels the calculations are run for
        'start': 4,                         # ignore this
        'classes': {                        # set the stat growth of each class here
            'dex_class': {
                'vit_start': 4,
                'vit_p_lvl': 2,

                'dex_start': 9,
                'dex_p_lvl': 4,

                'str_start': 2,
                'str_p_lvl': 1,

                'int_start': 2,
                'int_p_lvl': 1,

                'agility_start': 8,
                'agility_p_lvl': 3,

                'toughness_start': 1,
                'toughness_p_lvl': 2,
            },
            'str_class': {
                'vit_start': 6,
                'vit_p_lvl': 3,

                'dex_start': 4,
                'dex_p_lvl': 1,

                'str_start': 8,
                'str_p_lvl': 4,

                'int_start': 1,
                'int_p_lvl': 1,

                'agility_start': 5,
                'agility_p_lvl': 1,

                'toughness_start': 2,
                'toughness_p_lvl': 2,
            },
            'int_class': {
                'vit_start': 4,
                'vit_p_lvl': 1,

                'dex_start': 1,
                'dex_p_lvl': 0,

                'str_start': 2,
                'str_p_lvl': 1,

                'int_start': 10,
                'int_p_lvl': 5,

                'agility_start': 5,
                'agility_p_lvl': 2,

                'toughness_start': 1,
                'toughness_p_lvl': 1,
            },
        }
    },
    # ratios for derived stats
    'conversion_ratios': {
        'wpn_dmg': 10,                      # base weapon dmg
        'b_dmg_wpn_dmg_factor': 50,         # percent of base dmg * weapon dmg
        'wpn_dmg_growth_per_lvl': 50,       # percent the weapon dmg grows per level

        'vit_to_hp': {
            'start': 50,
            'hp_per_vit': 15,
            'hp_per_lvl': 20,
        },

        'str_to_dmg': {
            'start': 5,
            'dmg_per_level': 0.6,
            'dmg_per_str': 0.7,
        },
        'dex_to_dmg': {
            'start': 5,
            'dmg_per_level': 0.6,
            'dmg_per_dex': 0.7,
        },
        'int_to_dmg': {
            'start': 5,
            'dmg_per_level': 0.6,
            'dmg_per_int': 0.7,
        },

        'toughness_to_armor': {
            'armor_per_toughness': 1,
        },

        'str_to_armor': {
            'start': 0,
            'armor_per_level': 0.5,
            'armor_per_str': 0.5,
        },
        'dex_speed_to_dodge': {
            'start': 3,
            'dodge_per_speed': 0.3,
            'dodge_per_dex': 0.2,
        },
        'dex_to_crit': {
            'chance_start': 5,
            'crit_chan_per_level': 0.25,
            'crit_chan_per_dex': 0.25,

            'dmg_start': 125,
            'crit_dmg_per_level': 1,
            'crit_dmg_per_dex': 3,
        },
        'dex_to_speed': {
            'speed_per_dex': 0.1,
            'speed_per_agility': 0.2,
            'speed_factor': 0.1,
            'speed_start': 9,
        },
    }
}


def count_base_stats(setup):
    cls_base_stat_count = {}
    for cls_key in setup.get('cl_base_stats').get('classes').keys():
        base_stats = setup.get('cl_base_stats').get('classes').get(cls_key)
        starting_pts = sum([
            base_stats['vit_start'], base_stats['dex_start'],
            base_stats['str_start'], base_stats['int_start'],
            base_stats['agility_start'], base_stats['toughness_start'],
        ])
        growth_pts = sum([
            base_stats['vit_p_lvl'], base_stats['dex_p_lvl'],
            base_stats['str_p_lvl'], base_stats['int_p_lvl'],
            base_stats['agility_p_lvl'], base_stats['toughness_p_lvl'],
        ])
        cls_base_stat_count[cls_key] = {'starting_pts': starting_pts, 'growth_pts': growth_pts}

    return cls_base_stat_count


[print(kv) for kv in count_base_stats(char_creation_setup).items()]

cl_df_list = create_cl_stats(**char_creation_setup)

full_setup_d3 = {
    'target_num': 1,
    'primary': True,
    'primary_percent': 100,
    'rnd_target': True,
    'splash_dmg': 0,
    'elemental': 'physical',
    'vamp': 0,
    'can_crit': True,
    'dmg_base': 'magic',
    'wpn_dmg_perc': 100,
    'max_hp_perc_dmg': 0,
    'c_hp_perc_dmg': 0,
    'can_dodge': True,
    'reduction_calc': 'd3'
}

full_setup_lol = {
    'target_num': 1,
    'primary': True,
    'primary_percent': 100,
    'rnd_target': True,
    'splash_dmg': 0,
    'elemental': 'physical',
    'vamp': 0,
    'can_crit': True,
    'dmg_base': 'magic',
    'wpn_dmg_perc': 100,
    'max_hp_perc_dmg': 0,
    'c_hp_perc_dmg': 0,
    'can_dodge': True,
    'reduction_calc': 'lol'
}

cl_suffixes = get_cl_suffixes(cl_df_list)

levels = 30
fights = pd.DataFrame({'fight_nr': increase_after_steps(0, 1, 1, levels, 1)})


fight_units = add_units(fights, cl_df_list)

fight_results = calc_fights(fight_units)

all_cl_df = rename_cols_concat(cl_df_list)


def compare(all_cl_df, index_list, cl_suffixes=cl_suffixes):
    ind = []
    for i in index_list:
        for s in cl_suffixes:
            ind.append(i + s)
    return all_cl_df[ind]


def dump_setup(setup):
    with open('char_creation_setup.json', 'w') as f:
        json.dump(setup, f, indent=4)
