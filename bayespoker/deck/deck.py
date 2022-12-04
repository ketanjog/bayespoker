"""
Class for a deck of cards.
"""

import random
from .card import Card

DECK_SIZE = 52


class Deck:
    def __init__(self):
        self.cards = []
        self.reset()

    def __str__(self):
        return str(self.cards)

    def __repr__(self):
        return self.__str__()

    def shuffle(self):
        random.shuffle(self.cards)

    def reset(self):
        self.cards = []
        for suit in Card.SUITS:
            for rank in Card.RANKS:
                self.cards.append(Card(suit, rank))

    def draw(self, n=1):
        if n > len(self.cards):
            raise ValueError("Cannot draw more cards than are in the deck")
        return [self.cards.pop() for _ in range(n)]

    def dealHand(self, n=2):
        return self.draw(n)

    def dealFlop(self):
        return self.draw(3)

    def dealTurn(self):
        return self.draw(1)

    def dealRiver(self):
        return self.draw(1)
