## Tristan Harley Lawrence Tew
## UTLN: 1560227
## CS150
## Please note that the black formatting package was used to clean up this code

import random

import games


# Example strategies
def always_defect(game):
    """Always selects the last action (assuming defection in a game like Prisoner's Dilemma)."""
    return game.actions[-1]

def always_cooperate(game):
    """Always selects the first action (assuming cooperation in a game like Prisoner's Dilemma)."""
    return game.actions[0]

def always_random(game):
    """Always selects a random action"""
    return random.choice(game.actions)


class Player:
    def __init__(self, game, strategy=always_cooperate):
        """
        Initialize player with a strategy.
        :param strategy: A function that determines the player's move given the game's payoff matrix.
        """
        self._game = game
        self._strategy = strategy

    def inform(self, my_action, other_action):
        return self._game.payoff_matrix[(my_action, other_action)]

    def choose_action(self):
        """
        Select an action based on the strategy function.
        :param game: The normal-form game (payoff matrix)
        :return: Chosen action (index)
        """
        return self._strategy(self._game)

# Tit for Tat player
class TFT(Player):
    def __init__(self, game):
        super().__init__(game)
        self._my_action = game.actions[0]
        self._other_action = game.actions[0]

    def inform(self, my_action, other_action):
        self._other_action = other_action

    def choose_action(self):
        return self._other_action


# Take example from assignment 2, use it as validation/test case
class EveryN(Player):
    def __init__(self, game, n: int = 5):
        super().__init__(game)
        self._my_action = game.actions[0]
        self._other_action = game.actions[0]
        self.rounds = 0
        self.n = n

    def inform(self, my_action, other_action):
        self._other_action = other_action

    def choose_action(self):
        """Every N rounds, defect; used to simulate something
        from our lectures and test strategy more thoroughly"""
        self.rounds += 1
        if self.rounds % self.n == 0:
            action = self._game.actions[-1]
        else:
            action = self._game.actions[0]

        return action

## task 2, 100 iteration player, NO input strategy this time, needs to be internal
class HundredPlayer(Player):
    """Agent which uses T4T except for the final hand which allows for victories
    in states with cooperation up to the end unless the other agent defects"""

    def __init__(self, game):
        super().__init__(game)
        self.rounds = 0
        self._other_action = game.actions[0]

    def inform(self, my_action, other_action):
        ## this should functionally be no different than the given TFT example
        self._other_action = other_action

    def choose_action(self):
        """Plays standard T4T except for the final round where there is no future penalty
        to try and steal points at the end. In the best case, this improves on perpetual
        cooperation by allowing a 0-year sentence final round; in the worst case, we
        play an opponent who doesn't start off cooperating and we never reach cooperation
        """

        outcome = None
        outcome_score = None

        self.rounds += 1

        ## our hundred player should defect on the final round because if
        ## we have cooperation then we can steal a few points at the end
        if self.rounds == 100:

            ## originally, this was simply defect using indexing, but
            ## that might not always work with every normal form game
            for action in self._game.actions:
                my_score, their_score = self._game.payoff_matrix[
                    (action, self._other_action)
                ]
                ## either update the outcome score on the first iteration OR
                ## choose the best strategy given what the other players will do
                if (outcome is None) or (outcome_score < my_score):
                    outcome_score = my_score
                    outcome = action

        ## else, use basic tit-for-tat play with no boosts/differences.
        ## in the best case, we are cooperative and reach the best outcome
        else:
            outcome = self._other_action

        return outcome


class MixPlayer(Player):
    """A player which uses a basic probabalistic approach paired with simple guardrails
    to avoid serious consequences of stationary strategies and maintain the
    core principles described within the Axelrod tournament"""

    def __init__(self, game, base_prob_weight: float = 0.5, trend_weight: float = 0.5):
        super().__init__(game)

        self._other_action = game.actions[0]
        self.opp_history = []
        self.other_moves_counter = {action: 0 for action in self._game.actions}
        self.enemy_defected = False
        self.base_probability = 1 / len(self._game.actions)
        self.base_prob_weight = base_prob_weight
        self.trend_weight = trend_weight

    def inform(self, my_action, other_action):
        """

        :param my_action: the action that this agent took
        :param other_action: the action that the other agent took
        :return: None, simply updates internals
        """
        payouts = self._game.payoff_matrix[(my_action, other_action)]

        ## if we've been wronged, that's a defection
        if my_action != other_action and payouts[0] < payouts[1]:
            self.enemy_defected = True

        self.opp_history.append(other_action)
        self._other_action = other_action

    def choose_action(self):
        """
        Choose the best action based on rules and if rules not met, then use stochastic
        forgiveness to determine what happens next

        :return: str: the move which we have selected
        """

        cooperate = self._game.actions[0]

        ## originally, this was simply defect using indexing, but
        ## that might not always work with every normal form game
        defect_move = None
        defect_move_score = None

        for action in self._game.actions:
            my_score, their_score = self._game.payoff_matrix[
                (action, self._other_action)
            ]
            ## either update the outcome score on the first iteration OR
            ## choose the best strategy given what the other players will do
            if (defect_move is None) or (defect_move_score < my_score):
                defect_move_score = my_score
                defect_move = action

        ## use the default start option if no defection has occurred, we cannot be the aggressor
        if not self.enemy_defected:
            return cooperate

        ## force defect if it's been more than two iterations and the opponent is spamming
        ## defect as that is a sign of a non-cooperative bot that can tank our tournament score
        elif len(self.opp_history) > 3 and cooperate not in self.opp_history:
            return defect_move

        ## based on observed edge case, we should be able to catch the simplest
        ## alternating patterns and respond accordingly
        elif len(self.opp_history) >= 4:
            if (self.opp_history[-1] == self.opp_history[-3]) and (
                self.opp_history[-2] == self.opp_history[-4]
            ):
                return self.opp_history[-2]

            ## so if we don't find a simple alternator, use probabilities to determine our best path forward.
            else:
                pass

        ## generally speaking, agents who are streaking cooperation are unlikely to induce
        ## retribution, make the probability of cooperation at this point 50% baseline probability
        ## plus the actual rate of cooperation to avoid biasing away from collaboration
        cooperation_rate = len([x for x in self.opp_history if x == cooperate]) / len(
            self.opp_history
        )

        ## By making this probabilistic, the agent has the ability to forgive being
        ## defected on in the past instead of being locked into a choice from that point on
        p_cooperate = (self.base_prob_weight * self.base_probability) + (
            self.trend_weight * cooperation_rate
        )
        if random.random() < p_cooperate:
            return cooperate
        else:
            return defect_move
