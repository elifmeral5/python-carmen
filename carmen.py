"""
File: carmen.py
Author: Elif Meral
Date: 05/13/2024
Section: 24
E-mail: elifm1@umbc.edu
Description:
    The user plays the game carmen to find Carmen Sandiego by searching places
        looking at clues, and talking to people.

"""

import json


def load_game(game_file_name):
    """
    :param game_file_name: a string with the game file name
    :return: a dictionary with the game data, or empty if the game file doesn't exist.
    """

    try:
        game = {}
        with open(game_file_name) as game_file:
            game = json.loads(game_file.read())
    except FileNotFoundError:
        print('That file does not exist. ')
        return None

    return game


def update_game_data(choice, game):
    """
    :param choice: a string with what the user wants to do
    :param game: a dictionary with the game data
    :return: the updated dictionary with the game data
    """
    if choice.startswith('talk to '):
        # finds the person
        find_person = choice.split(' ')
        found_person = len(find_person) - 1
        person = find_person[found_person]
        # Unlock location(s)
        if person in game['people']:
            loc_to_unlock = game['people'][person].get('unlock-locations', [])
            for loc in loc_to_unlock:
                if loc in game['locations']:
                    game['locations'][loc]['starts-locked'] = False

            # Unlock people
            people_to_unlock = game['people'][person].get('unlock-people', [])
            for per in people_to_unlock:
                if per in game['people']:
                    game['people'][per]['starts-hidden'] = False

    if choice.startswith('investigate'):
        find_investigation = choice.split(' ')
        found_investigation = len(find_investigation) - 1
        the_investigation = find_investigation[found_investigation]
        # Unlock location(s)
        if the_investigation == 'Brandenburg-Gate':
            loc_to_unlock = game['clues'][the_investigation].get('unlock-locations')
            for loc in loc_to_unlock:
                if loc in game['locations']:
                    game['locations'][loc]['starts-locked'] = False

            # Unlock people
            people_to_unlock = game['clues'][the_investigation].get('unlock-people')
            for per in people_to_unlock:
                if per in game['people']:
                    game['people'][per]['starts-hidden'] = False

    return game


# displays the people in the location when asked


def display_people(location, spoken, game):
    """
    :param location: users current location
    :param spoken: list of people the user has talked to.
    :param game: a dictionary with the game data
    :return: none
    """
    for name, data in game['people'].items():
        if data['location'] == location and not data.get('starts-hidden', False):
            if name in spoken:
                status = game['people'][name]['conversation']
            else:
                status = 'Not Spoken To Yet'

            print(name, '     ', status)


# allows the person user picks to say their conversation and updates to them being spoken to.


def talk_to(choice, spoken, game, current_location):
    """
    :param choice: a string with what the user wants to do
    :param spoken: list of people user talked to
    :param game: a dictionary with the game data
    :param current_location: users current location
    :return: updated version of the game
    """
    # gets the person the user wants to talk to
    find_person = choice.split(' ')
    found_person = len(find_person) - 1
    person = find_person[found_person]

    if person in game['people']:
        person_data = game['people'][person]
        if person_data['location'] == current_location:
            spoken.append(person)
            convo = game['people'][person]['conversation']
            print(convo)

            game = update_game_data(choice, game)
        else:
            print(person, 'is not in', current_location)
    else:
        print('There is no one named', person, 'here.')

    return game


# displays all the locations


def locations(game):
    """
    :param game: game dictionary
    :return: None
    """
    all_locations = game.get('locations')
    for loc in all_locations:
        if game['locations'][loc]['starts-locked']:
            print(loc + '     Locked')
        else:
            print(loc + '     Unlocked')


# checks to see if the location is unlocked and reachable using RECURSION


def check_path(current_location, wanted_location, game, visited):
    """
    :param current_location: users current location
    :param wanted_location: the location user wants to go to
    :param game: the game dictionary
    :param visited: keep track of the visited places
    :return: either True or False
    """
    if current_location == wanted_location:
        return True

    visited.append(current_location)
    current_location_data = game['locations'].get(current_location)
    # print(current_location_data)
    # print(current_location_data.get('connections', []))
    for next_location in current_location_data.get('connections', []):
        if not game['locations'][next_location].get('starts-locked', True) and next_location not in visited:
            if check_path(next_location, wanted_location, game, visited):
                return True

    return False


# function for travelling location


def display_location(current_location, wanted_location, game):
    """
    :param current_location: users current location
    :param wanted_location: the location user wants to go to
    :param game: game dictionary
    :return: True or False and the location
    """
    # gathers all the locations in the game
    all_locations = game.get('locations')
    # print(all_locations)

    # Gets the location user wants
    find_location = wanted_location.split(' ')
    found_location = len(find_location) - 1
    location = find_location[found_location]
    # print(location)
    # checking if the input location is valid
    if location not in all_locations:
        print('The location', location, 'does not exist. ')
        return False, current_location

    visited = []

    # checks if the location can be traveled to
    if check_path(current_location, location, game, visited):
        print('You have traveled to', location)
        return True, location
    else:
        print('You are unable to travel to', location)
        return False, current_location


# displays the clue in current location when user asks


def display_clue(current_location, game):
    """
    :param current_location: users current location
    :param game: the game dictionary
    :return: None
    """
    if current_location == 'Berlin':
        if game.get['clues']['Brandenburg-Gate']['starts-hidden']:
            print('Brandenburg-Gate Clue')
        else:
            print('Brandenburg-Gate Clue: ' + game['clues']['Brandenburg-Gate']['clue-text'])
    else:
        print('There is no clue here.')


# investigates Brandenburg-Gate


def investigate(choice, current_location, game):
    """
    :param choice: a string with what the user wants to do
    :param current_location: users current location
    :param game:
    :return: none
    """
    # gathers what is being investigated
    find_investigation = choice.split(' ')
    found_investigation = len(find_investigation) - 1
    the_investigation = find_investigation[found_investigation]
    if the_investigation == 'Brandenburg-Gate':
        if current_location == 'Berlin':
            print(game['clues']['Brandenburg-Gate']['clue-text'])
        else:
            print('This place does not exist in your current location.')
    else:
        print('An investigation can not be made here.')


# checks to see if carmen is there


def catch_carmen(current_location, tries, carmen_status):
    """
    :param current_location: users current location
    :param tries: amount of times the user tries
    :param carmen_status: keeps track on if carmen was found or not
    :return: carmen_status and tries
    """
    if current_location == 'Moscow':
        carmen_status = True
        return carmen_status, tries
    else:
        tries += 1
        print('Nice try but Carmen is not here! You have', 3 - tries, 'tries left.')
        carmen_status = False
        return carmen_status, tries


# runs function according to what the user asks for


def check_input(choice, current_location, spoken, game, tries, carmen_status, visited):
    """
    :param choice: input of what the user wants to do
    :param current_location: the users current location
    :param spoken: keeps track of who is spoken to
    :param game: the game dictionary
    :param tries: keeps track oof how many times the user tried to catch Carmen
    :param carmen_status: keeps track of whether carmen is found
    :param visited: keeps track of visited locations
    :return: Whether a valid response was given and played out or not.
    """
    action_taken = False

    if choice.startswith('display people'):
        display_people(current_location, spoken, game)
        action_taken = True

    elif choice.startswith('talk to'):
        game = talk_to(choice, spoken, game, current_location)
        action_taken = True

    elif choice.startswith('display locations'):
        locations(game)
        action_taken = True

    elif choice.startswith('go to') or choice.startswith('travel to'):
        success, new_location = display_location(current_location, choice, game)
        if success:
            current_location = new_location
        action_taken = True

    elif choice.startswith('display clue'):
        display_clue(current_location, game)
        action_taken = True

    elif choice.startswith('investigate the'):
        investigate(choice, current_location, game)
        update_game_data(choice, game)
        action_taken = True

    elif choice.startswith('catch'):
        carmen_status, tries = catch_carmen(current_location, tries, carmen_status)
        action_taken = True

    return action_taken, current_location, tries, carmen_status


# RUNS THE WHOLE GAME


def carmen_sandiego(game_file_name):
    """
    :param game_file_name: inserts the game dicitionary
    :return: the whole game is played
    """
    game = load_game(game_file_name)
    if not game:
        return

    spoken = []
    visited = []
    current_location = game['starting-location']
    tries = 0
    carmen_status = False

    print('You are at', current_location)
    while True:
        choice = input('What would you like to do? ')

        if choice == 'quit' or choice == 'exit':
            print('end game')
            return False

        if tries >= 2:
            print('You ran out of tries and lost the game.')
            return False

        if carmen_status:
            print('You have caught Carmen Sandiego! You win the game!')
            return True

        action_taken, current_location, tries, carmen_status = check_input(choice, current_location, spoken, game, tries,
                                                             carmen_status, visited)
        if carmen_status:
            print('You have caught Carmen Sandiego! You win the game!')
            return True

        if not action_taken:
            print('This is not an acceptable action. Try Again.')


if __name__ == '__main__':
    game_file_name = input('Which game do you want to play? ')
    carmen_sandiego(game_file_name)
