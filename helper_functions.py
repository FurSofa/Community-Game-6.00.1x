def select_from_list(iterable, index_pos=False, q='Whats your choice?'):
    """
    Takes an iterable
    prints a numerated list for the user to choose from
    lets the user choose
    returns index position of user chosen item of iterable
    if index_pos=True will return index position of chosen object instead of object
    :param iterable, index_pos:
    :return chosen item or index position:
    """
    print(q)
    for index, item in enumerate(iterable):
        display_number = str(index + 1)
        print(display_number + ': ', item)
    choice = ""
    while not choice:
        try:
            choice = int(input('Number of choice: '))
            if choice < 1 or choice > len(iterable):
                print("Enter a number from the list!")
                choice = ""
        except ValueError:
            print("Invalid choice!")
    
    if index_pos:
        return choice - 1
    return iterable[choice-1]


def select_from_list_horizontal(iterable, index_pos=False, q='\nWho do you want to attack?'):
    """
    Takes an iterable
    prints a numerated list -- HORIZONTALLY --
    for the user to choose from, lets the user choose
    returns index position of user chosen item of iterable
    if index_pos=True will return index position of chosen object instead of object
    :param question, iterable, index_pos:
    :return chosen item or index position:
    """
    if len(iterable) < 2:
        choice_index = 0
        if index_pos:
            return choice_index
        return iterable[choice_index]
    print(q)
    for index, item in enumerate(iterable):
        display_number = str(index + 1)
        print(display_number + ': ', item, end='  ')
    choice = input('')
    if choice == '':
        choice_index = 0
        if index_pos:
            return choice_index
        return iterable[choice_index]

    if not choice.isdigit() or not 0 < int(choice) <= len(iterable):
        print('Please select a number from the list!')
        choice_index = select_from_list(iterable, index_pos=True, q=q)
    else:
        choice_index = int(choice) - 1
    if index_pos:
        return choice_index
    return iterable[choice_index]

if __name__ == '__main__':
    x = select_from_list(['one', 'two', 'three'])
    y = select_from_list_horizontal(['one', 'two', 'three'], True)
