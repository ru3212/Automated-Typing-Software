"""Typing test implementation"""
from typing import Any

from utils import lower, split, remove_punctuation, lines_from_file
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    # BEGIN PROBLEM 1
    i = k
    while len(paragraphs) > i:
        if select(paragraphs[k]) == True:
            return paragraphs[k]
        elif select(paragraphs[i]) == True:
            paragraphs[k] = paragraphs[i]
            paragraphs[i] = ''
            return paragraphs[k]
        else:
            i += 1
    return ''
    "*** YOUR CODE HERE ***"
    # END PROBLEM 1


def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    def select(paragraph):
        has_word_topic = False
        paragraph = lower(paragraph)
        paragraph = remove_punctuation(paragraph)
        paragraph = split(paragraph)
        for i in topic:
            for k in paragraph:
                if i == k:
                    has_word_topic = True
        return has_word_topic
    return select
    "*** YOUR CODE HERE ***"
    # END PROBLEM 2


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    typed = split(typed)
    reference = split(reference)
    num = 0
    denom = len(typed)
    higher_length = 0
    if len(reference) < len(typed):
        lower_length = len(reference)
    else:
        lower_length = len(typed)
    for i in range(lower_length):
        if reference[i] == typed[i]:
            num += 1
    if denom == 0:
        return 0.0
    return (num / denom) * 100
    "*** YOUR CODE HERE ***"
    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    t_in_min = elapsed / 60
    words = len(typed)
    return (words / 5) / t_in_min
    "*** YOUR CODE HERE ***"
    # END PROBLEM 4


def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than LIMIT.
    """
    # BEGIN PROBLEM 5

    for x in range(len(valid_words)):
        if valid_words[x] == user_word:
            return user_word

    lowest_diff = len(user_word)
    current_diff = 0
    min_diff = 0
    for x in valid_words:
        current_diff = diff_function(user_word, x, limit)
        if lowest_diff > current_diff:
            lowest_diff = current_diff
            min_diff = x

    if lowest_diff > limit:
        return user_word
    return min_diff

    "*** YOUR CODE HERE ***"
    # END PROBLEM 5


def shifty_shifts(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    # BEGIN PROBLEM 6
    start = list(start)
    goal = list(goal)
    diff = 0
    min_list = []
    max_list = []
    if limit < 0:
        return 1
    if len(start) != len(goal):
        diff = abs(len(start) - len(goal))
        min_list = min(start, goal)
        max_list = max(start, goal)
        max_list = max_list[:(len(min_list))]
    else:
        min_list = start
        max_list = goal

    if min_list == max_list:
        return 0 + diff
    elif min_list[0] == max_list[0]:
        return shifty_shifts(start[1:], goal[1:], limit)
    else:
        return 1 + shifty_shifts(start[1:], goal[1:], limit - 1)
    # END PROBLEM 6


def pawssible_patches(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL."""


    #if ______________: # Fill in the condition#
        # BEGIN
    start = list(start)
    goal = list(goal)
    if limit < 0:
        return 1
    elif start == goal:
        return 0
    elif goal == [] or start == []:
        return len(start) + len(goal)
    elif start[0] == goal[0]:
        return pawssible_patches(start[1:], goal[1:], limit)
    else:
        add_diff = 1 + pawssible_patches(start, goal[1:], limit - 1)
        remove_diff = 1 + pawssible_patches((start[1:]), goal, limit - 1) # make sure the element in start is removed
        substitute_diff = 1 + pawssible_patches(start[1:], goal[1:], limit - 1)
        return min(add_diff, remove_diff, substitute_diff)


        # END

    #elif ___________: # Feel free to remove or add additional cases
        # BEGIN
        "*** YOUR CODE HERE ***"
        # END

    #else:
        add_diff = ... # Fill in these lines
        remove_diff = ...
        substitute_diff = ...
        # BEGIN
        "*** YOUR CODE HERE ***"
        # END


def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function'


###########
# Phase 3 #
###########


def report_progress(typed, prompt, user_id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8
    correct = typed
    has_failed = False
    for x in range(len(typed)):
        if not has_failed:
            if typed[x] != prompt[x]:
                correct = typed[:x]
                has_failed = True
    prog = len(correct) / len(prompt)
    send({'id': user_id, 'progress': prog})
    return prog

    "*** YOUR CODE HERE ***"
    # END PROBLEM 8


def fastest_words_report(times_per_player, words):
    """Return a text description of the fastest words typed by each player."""
    game = time_per_word(times_per_player, words)
    fastest = fastest_words(game)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def time_per_word(times_per_player, words):
    """Given timing data, return a game data abstraction, which contains a list
    of words and the amount of time each player took to type each word.

    Arguments:
        times_per_player: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.
        words: a list of words, in the order they are typed.
    """
    # BEGIN PROBLEM 9
    total_diffs = []
    for x in range(len(times_per_player)):
        diffs = []
        for y in range(len(times_per_player[x]) - 1):
            diffs.append(times_per_player[x][y + 1] - times_per_player[x][y])
        total_diffs.append(diffs)
    return game(words, total_diffs)
    "*** YOUR CODE HERE ***"
    # END PROBLEM 9


def fastest_words(game):
    """Return a list of lists of which words each player typed fastest.

    Arguments:
        game: a game data abstraction as returned by time_per_word.
    Returns:
        a list of lists containing which words each player typed fastest
    """
    player_indices = range(len(all_times(game)))  # contains an *index* for each player
    word_indices = range(len(all_words(game)))    # contains an *index* for each word
    # BEGIN PROBLEM 10
    fin_list = []
    for z in player_indices:
        fin_list.append([])
    times = all_times(game)
    min_diff = 0
    first_tie = 0
    player_score_index = 0
    for x in word_indices:
        current_word = word_at(game, x)
        min_diff = len(times) * 10
        for y in player_indices:
            curr_time = time(game, y, x)
            if curr_time < min_diff:
                min_diff = curr_time
                player_score_index = y
                first_tie = y
            elif curr_time == min_diff:
                player_score_index = first_tie
        fin_list[player_score_index].append(current_word)
    return fin_list

    "*** YOUR CODE HERE ***"
    # END PROBLEM 10


def game(words, times):
    """A data abstraction containing all words typed and their times."""
    assert all([type(w) == str for w in words]), 'words should be a list of strings'
    assert all([type(t) == list for t in times]), 'times should be a list of lists'
    assert all([isinstance(i, (int, float)) for t in times for i in t]), 'times lists should contain numbers'
    assert all([len(t) == len(words) for t in times]), 'There should be one word per time.'
    return [words, times]


def word_at(game, word_index):
    """A selector function that gets the word with index word_index"""
    assert 0 <= word_index < len(game[0]), "word_index out of range of words"
    return game[0][word_index]


def all_words(game):
    """A selector function for all the words in the game"""
    return game[0]


def all_times(game):
    """A selector function for all typing times for all players"""
    return game[1]


def time(game, player_num, word_index):
    """A selector function for the time it took player_num to type the word at word_index"""
    assert word_index < len(game[0]), "word_index out of range of words"
    assert player_num < len(game[1]), "player_num out of range of players"
    return game[1][player_num][word_index]


def game_string(game):
    """A helper function that takes in a game object and returns a string representation of it"""
    return "game(%s, %s)" % (game[0], game[1])

enable_multiplayer = False  # Change to True when you're ready to race.

##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)