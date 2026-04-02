from itertools import accumulate
from threading import Event

from player import *
import games

class NormalFormGame:
    def __init__(self, game):
        """
        Initialize the normal-form game with a given payoff matrix.
        :param payoff_matrix: A dictionary where keys are (p1_action, p2_action) tuples,
                              and values are (p1_payoff, p2_payoff) tuples.
        """
        self.payoff_matrix = game[1]
        self.actions = game[0]

    def play_game(self, player1, player2, rounds=100):
        """
        Simulate the game for a given number of rounds.
        :param player1: Player 1 instance
        :param player2: Player 2 instance
        :param rounds: Number of rounds to play
        :return: List of outcomes [(p1_payoff, p2_payoff), ...]
        """
        results = []
        for _ in range(rounds):

            action1 = player1.choose_action()
            action2 = player2.choose_action()
            result = self.payoff_matrix[(action1, action2)]
            results.append(result)

            player1.inform(action1, action2)
            player2.inform(action2, action1)
        return results

def main():
    game = NormalFormGame(games.Chicken)
    p1 = HundredPlayer(game)
    p2 = Player(game, strategy=always_cooperate)

    outcomes = game.play_game(p1, p2)
    p1_outcome = sum(map(lambda x: x[0], outcomes))
    p2_outcome = sum(map(lambda x: x[1], outcomes))
    print("p1 total = ", p1_outcome, ", p2 total = ", p2_outcome)

if __name__ == "__main__":
    main()