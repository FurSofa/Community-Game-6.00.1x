def player_choose_from_list(iterable, index_pos=False):
    """
    Takes an iterable
    prints a numerated list for the user to choose from
    lets the user choose
    returns index position of user chosen item of iterable
    if index_pos=True will return index position of chosen object instead of object
    :param iterable, index_pos:
    :return chosen item or index position:
    """
    for index, item in enumerate(iterable):
        display_number = str(index + 1)
        print(display_number + ': ', item)
    choice = input('Number of choice: ')
    if not choice.isdigit() or not 0 < int(choice) < (len(iterable) + 1):
        print('Enter the number of the target!')
        choice_index = player_choose_from_list(iterable, index_pos=True)
    else:
        choice_index = int(choice) - 1
    if index_pos:
        return choice_index
    return iterable[choice_index]


    #  TODO: figure out a way to get back if misstyped the menu choice
