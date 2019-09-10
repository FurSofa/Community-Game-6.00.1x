from os import system, name

class bcolors:
    HeadER = '\033[95m'
    OKBLUE = '\033[94m'
    WARNING = '\033[93m'
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



# colors:
escape_code = '\033'
low_intensity = {

}
high_intensity = {}
class Colors:



# TODO: refactor into function - no need for a class?
# TODO: make color change depending on value
class BarGFX:
    def __init__(self, current, full, length=10, f_color=bcolors.OKGREEN, m_color=bcolors.FAIL,
                 f_char='#', m_char='-'):
        '''

        :param current: int: current value - eg hp
        :param full: int: max value - eg max_hp
        :param length: int: length of the bar without border - number of chars
        :param f_color: color code : for filled ticks
        :param m_color: color code : for missing ticks
        :param f_char: str: char to display for filled ticks
        :param m_char: str: char to be displayed for not filled ticks
        '''
        self.length = length
        self.fill_color = f_color
        self.missing_color = m_color
        self.current = current
        self.full = full
        self.fill_char = f_char
        self.missing_char = m_char
        self.tick_percent = 100 / length

    def bar_str(self, no_color=False, border='|'):
        '''
        creates a string of the BarGFX
        :param no_color: bool
        :param border: char to display as border for bar - use '' for no border
        :return: str: BarGFX as string
        '''
        hp_bar = ""
        if no_color:
            f_color = ''
            m_color = ''
            end_color = ''
        else:
            f_color = self.fill_color
            m_color = self.missing_color
            end_color = bcolors.ENDC

        hp_bar_ticks = (self.current / self.full) * 100 / self.tick_percent

        while hp_bar_ticks > 0:
            hp_bar += self.fill_char
            hp_bar_ticks -= 1

        hp_bar += m_color

        while len(hp_bar) < self.length+len(m_color):
            hp_bar += self.missing_char

        return (border + f_color + hp_bar + end_color + border)

    def draw_bar_plain(self):
        hp_bar = ""
        hp_bar_ticks = (self.current / self.full) * 100 / self.tick_percent

        while hp_bar_ticks > 0:
            hp_bar += self.fill_char
            hp_bar_ticks -= 1

        while len(hp_bar) < self.length:
            hp_bar += self.missing_char
        return "|" + hp_bar + "|"

    def get_muted_char_len(self):
        return len(self.bar_str()) - len(self.bar_str(no_color=True))


# Example setup from the old RPG
#    @property
#     def hp_bar(attacker):
#         hp_bar = BarGFX(20, bcolors.OKGREEN, attacker.hp, attacker.maxhp)
#         return hp_bar
#
#     @property
#     def hp_bar_short(attacker):
#         hp_bar = BarGFX(10, bcolors.OKGREEN, attacker.hp, attacker.maxhp)
#         return hp_bar

def clear_screen():
    # for windows
    if name == 'nt':
        _ = system('cls')
        # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


camp_fire = """    
                 )
                (\033[1;33m
               /`/\\
              (% \033[1;31m%)\033[1;33m)\033[0;0m
            .-'....`-.
            `--'.'`--' """
