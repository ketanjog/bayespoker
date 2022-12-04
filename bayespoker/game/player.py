"""
This class represents a player in a game of poker. The player has a hand of cards, and a bankroll. The player can bet, fold, or call.
The player uses a strategy to determine what action to take.
"""

from bayespoker.deck import Card


class Player:
    def __init__(self, bankroll, strategy):
        self.bankroll = bankroll
        self.strategy = strategy
        self.hand = []
        self.bet = 0
        self.folded = False

    def __str__(self):
        return str(self.hand)

    def __repr__(self):
        return self.__str__()

    def showHand(self):
        return self.hand

    def play(self, game):
        if self.folded:
            return 0
        return self.strategy.action(game, bankroll=self.bankroll, hand=self.hand)

    def receiveHand(self, hand):
        self.hand = hand
