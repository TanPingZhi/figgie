# diamond clubs hearts spades
# diamond: red
# clubs: black
# hearts: red
# spades: black

import itertools
from math import comb


def figgie_odds(diamonds, clubs, hearts, spades):
    permutations = sorted(list(set(itertools.permutations([12, 10, 10, 8]))))
    suits = ['diamonds', 'clubs', 'hearts', 'spades']
    odds = []
    for i in range(4):
        filtered_permutations = [x for x in permutations if x[i] == 12]
        probability = 0
        for permutation in filtered_permutations:
            probability += comb(permutation[0], diamonds) * comb(permutation[1], clubs) * comb(
                permutation[2], hearts) * comb(permutation[3], spades)
        odds.append(probability)
    total = sum(odds)
    odds = [x / total for x in odds]
    argmax = odds.index(max(odds))
    print(f'Goal suit: {suits[(argmax + 2) % 4]}')
    print(f'P = {round(odds[argmax], 2)}')

    print(f'♠: {round(odds[1], 2)}') # prob of spades is from clubs - odd[1]
    print(f'♣: {round(odds[3], 2)}') # prob of clubs is from spades - odd[3]
    print(f'♦: {round(odds[2], 2)}') # prob of diamonds is from hearts - odd[2]
    print(f'♥: {round(odds[0], 2)}') # prob of hearts is from diamonds - odd[0]

    # you will need to decide whether buying more is worth it


def main():
    print("Enter the number of spades, clubs, diamonds, hearts separated by spaces (or type 'exit' to quit):")
    while True:
        user_input = input("> ")
        if user_input.lower() == 'exit':
            break
        try:
            # diamonds, clubs, hearts, spades = map(int, user_input.split())
            spades, clubs, diamonds, hearts = map(int, user_input.split())

            figgie_odds(diamonds, clubs, hearts, spades)
        except ValueError:
            print("Invalid input. Please enter four integers separated by spaces.")
        print()


if __name__ == "__main__":
    main()
