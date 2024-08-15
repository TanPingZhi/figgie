import itertools
from math import comb
from scipy.stats import rankdata

SUITS = ['♠', '♣', '♦', '♥',]


def figgie_odds(spades, clubs, diamonds, hearts):
    # set to remove duplicates of two 10s
    permutations = sorted(list(set(itertools.permutations([12, 10, 10, 8]))))
    

    goal_odds = [[0, 0, 0] for i in range(4)]
    # goal_odds[i][0] = events that suits[i] is goal suit with 8 cards
    # goal_odds[i][1] = events that suits[i] is goal suit with 10 cards
    # goal_odds[i][2] = total events that suits[i] is goal suit
    for i in range(4):
        filtered_permutations = [x for x in permutations if x[i] == 12]
        for permutation in filtered_permutations:
            events = comb(permutation[0], spades) * comb(permutation[1], clubs) * comb(
                permutation[2], diamonds) * comb(permutation[3], hearts)
            if i == 0:
                if permutation[1] == 8:
                    goal_odds[1][0] += events
                elif permutation[1] == 10:
                    goal_odds[1][1] += events
            elif i == 1:
                if permutation[0] == 8:
                    goal_odds[0][0] += events
                elif permutation[0] == 10:
                    goal_odds[0][1] += events
            elif i == 2:
                if permutation[3] == 8:
                    goal_odds[3][0] += events
                elif permutation[3] == 10:
                    goal_odds[3][1] += events
            elif i == 3:
                if permutation[2] == 8:
                    goal_odds[2][0] += events
                elif permutation[2] == 10:
                    goal_odds[2][1] += events
    for i in range(4):
        goal_odds[i][2] = goal_odds[i][0] + goal_odds[i][1]

    total = 0
    for i in range(4):
        total += goal_odds[i][2]
    for i in range(4):
        goal_odds[i][0] /= total
        goal_odds[i][1] /= total
        goal_odds[i][2] /= total

    return goal_odds


def major_win_keep_values(hand, goal_odds):
    """
    hand: given cards in hand in the order of spades, clubs, diamonds, hearts
    This will return the value of the suit if it's goal suit and you have the majority of the suit.
    returns list of size 4
    """

    keep_value = [0, 0, 0, 0]
    for i in range(4):
        if hand[i] == 0:
            keep_value[i] = 0
        else:
            keep_value[i] = goal_odds[i][0] * (120 + hand[i] * 10) + goal_odds[i][1] * (100 + hand[i] * 10)
    return keep_value

def minor_win_keep_values(hand, goal_odds):
    """
    This will return the value of the suit if it's goal suit and you do not have the majority of the suit.
    returns list of size 4
    """
    keep_value = [0, 0, 0, 0]
    for i in range(4):
        keep_value[i] = hand[i] * 10 * goal_odds[i][0] + hand[i] * 10 * goal_odds[i][1]
    return keep_value

def chances_stars(goal_odds):
    # consider only goal_odds[i][2]
    ranking = rankdata([goal_odds[i][2] for i in range(4)], method='min')
    stars = []
    for idx in range(4):
        stars_padded = ("*" * ranking[idx]).ljust(4)
        stars.append(stars_padded)
    return stars

def buy_to_confirm_majority(hand, goal_odds, major_win_keep_values):
    expected_cost = [None] * 4
    for i in range(4):
        if hand[i] >= 6:
            expected_cost[i] = '-'
        else:
            quantity_to_buy = 6 - hand[i]
            expected_cost[i] = f'{quantity_to_buy} @ ${str(round(major_win_keep_values[i] / quantity_to_buy, 1)).rjust(4)}'
    return expected_cost


def print_grid(suits, final_goal_odds, stars, major_win_keep, minor_win_keep, buy_cost):
    print(f"{'Suit':<5} {'Odds':<8} {'Stars':<5} {'Major':>10} {'Minor':>10} {'Buy to Confirm':>15}")
    print("-" * 60)
    for i in range(4):
        print(f"{suits[i]:<5} {final_goal_odds[i]:<8.2} {stars[i]:<5} {major_win_keep[i]:>10.2f} {minor_win_keep[i]:>10.2f} {buy_cost[i]:>15}")
    print("-" * 60)

def main():
    while True:
        print("Enter the number of spades, clubs, diamonds, hearts separated by spaces (or type 'exit' to quit):")
        user_input = input("> ")
        print("=" * 80)
        if user_input.lower() == 'exit':
            break
        spades, clubs, diamonds, hearts = map(int, user_input.split())

        goal_odds = figgie_odds(spades=spades, clubs=clubs, diamonds=diamonds, hearts=hearts)
        stars = chances_stars(goal_odds)
        major_win_keep = major_win_keep_values([spades, clubs, diamonds, hearts], goal_odds)
        minor_win_keep = minor_win_keep_values([spades, clubs, diamonds, hearts], goal_odds)
        buy_cost = buy_to_confirm_majority([spades, clubs, diamonds, hearts], goal_odds, major_win_keep)

        final_goal_odds = [goal_odds[i][2] for i in range(4)]
        print_grid(SUITS, final_goal_odds, stars, major_win_keep, minor_win_keep, buy_cost)
        


if __name__ == '__main__':
    main()
