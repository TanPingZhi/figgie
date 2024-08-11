import itertools
from math import comb
from scipy.stats import rankdata


def figgie_odds(diamonds, clubs, hearts, spades):
    # set to remove duplicates of two 10s
    permutations = sorted(list(set(itertools.permutations([12, 10, 10, 8]))))
    values = [spades, clubs, diamonds, hearts]
    # suits = ['♦', '♣', '♥', '♠']
    suits = ['♠', '♣', '♦', '♥',]

    odds = [] # odds[i] = odds that suits[i] is the 12 suit
    for i in range(4):
        filtered_permutations = [x for x in permutations if x[i] == 12]
        events = 0
        for permutation in filtered_permutations:
            events += comb(permutation[0], spades) * comb(permutation[1], clubs) * comb(
                permutation[2], diamonds) * comb(permutation[3], hearts)
        odds.append(events)
    total = sum(odds)
    odds = [x / total for x in odds]

    goal_odds = [odds[1], odds[0], odds[3], odds[2]]

    ranking = rankdata(goal_odds, method='min')

    for idx in range(4):
        stars_padded = ("*" * ranking[idx]).ljust(4)
        print(
            f'{suits[idx]} {round(goal_odds[idx], 2)} {stars_padded}', end=' ')

        if values[idx] > 6:
            print(f'(SELL;      Excess: {values[idx] - 6})', end=' ')
        elif values[idx] == 6:
            print(f'(CORNERED)           ', end=' ')
        else:
            expected_gain = 100 * goal_odds[idx]
            quantity_to_buy = 6 - values[idx]
            expected_cost_each = round(expected_gain / quantity_to_buy, 2)
            print(f'(BUY2WIN;  {quantity_to_buy} @ ${expected_cost_each})', end=' ') # if you want to buy for the majority win

        if values[idx] >= 6:
            keep_value = round(goal_odds[idx] * (100 + values[idx] * 10), 2)
            print(f'(WIN Keep value: {keep_value})')

        else:
            keep_value = round(values[idx] * 10 * goal_odds[idx], 2)
            print(f'(NO WIN Keep value: {keep_value})')

    # you will need to decide whether buying more is worth it


def main():
    print("Enter the number of spades, clubs, diamonds, hearts separated by spaces (or type 'exit' to quit):")
    while True:
        user_input = input("> ")
        print("For a profitable round w/o doing anything, the total keep value > 40")
        print("If WIN Keep value < bid, just sell.")
        print("=" * 80)
        if user_input.lower() == 'exit':
            break
        try:
            # diamonds, clubs, hearts, spades = map(int, user_input.split())
            spades, clubs, diamonds, hearts = map(int, user_input.split())

            figgie_odds(diamonds=diamonds, clubs=clubs,
                        hearts=hearts, spades=spades)
        except ValueError:
            print("Invalid input. Please enter four integers separated by spaces.")
        print()


if __name__ == "__main__":
    main()
