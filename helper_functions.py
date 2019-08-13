def select_from_list(iterable, q='Whats your choice?', index_pos=False, horizontal=False):
    """
    Takes an iterable
    prints a numerated list for the user to choose from
    lets the user choose
    returns index position of user chosen item of iterable
    if index_pos=True will return index position of chosen object instead of object
    :param iterable, index_pos, horizontal:
    :return chosen item or index position:
    """
    # Atomically choose if only 1 choice.
    if len(iterable) == 1:
        if index_pos:
            return 0
        return iterable[0]

    print(q)
    if horizontal:
        for index, item in enumerate(iterable):
            display_number = str(index + 1)
            print(display_number + ': ', item, end='  ')
            print('')
    else:
        for index, item in enumerate(iterable):
            display_number = str(index + 1)
            print(display_number + ': ', item)
    choice = ""
    while not choice:
        choice = input('Number of choice: ')
        try:
            choice = 1 if not choice else int(choice)
            if choice < 1 or choice > len(iterable):
                print("Enter a number from the list!")
                choice = ""
        except ValueError:
            print("Invalid choice!")
            choice = ""

    if index_pos:
        return choice - 1
    return iterable[choice - 1]


if __name__ == "__main__":
    x = select_from_list(["Acidic Slime", "Necrotic Ooze", "Decrepit Wurm"],
                         "Choose a target:")
    print('You selected: ', x)
    x = select_from_list(["Acidic Slime"])
    print('You selected: ', x)
    x = select_from_list(["Arrows", "Candles", "Lockpicks", "Not Interested"],
                         "What would you like to buy?", False, True)
    print('You selected: ', x)