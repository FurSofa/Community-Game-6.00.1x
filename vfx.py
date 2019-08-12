
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    WARNING = '\033[93m'
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class BarGFX:
    def __init__(self, length, color, current, full):
        self.length = length
        self.color = color
        self.current = current
        self.full = full

        self.tick_percent = 100 / length

    def draw_bar(self):
        # create "graphic" hp/mp bars
        hp_bar = ""
        hp_bar_ticks = (self.current / self.full) * 100 / self.tick_percent

        while hp_bar_ticks > 0:
            hp_bar += "#"
            hp_bar_ticks -= 1

        while len(hp_bar) < self.length:
            hp_bar += "-"

        return ("|" + self.color + hp_bar +
                bcolors.ENDC + "|")

    def draw_bar_plain(self):
        hp_bar = ""
        hp_bar_ticks = (self.current / self.full) * 100 / self.tick_percent

        while hp_bar_ticks > 0:
            hp_bar += "#"
            hp_bar_ticks -= 1

        while len(hp_bar) < self.length:
            hp_bar += "-"
        return "|" + hp_bar + "|"

    def get_muted_char_len(self):
        return len(self.draw_bar()) - len(self.draw_bar_plain())


# Example setup from the old RPG
#    @property
#     def hp_bar(self):
#         hp_bar = BarGFX(20, bcolors.OKGREEN, self.hp, self.maxhp)
#         return hp_bar
#
#     @property
#     def hp_bar_short(self):
#         hp_bar = BarGFX(10, bcolors.OKGREEN, self.hp, self.maxhp)
#         return hp_bar
