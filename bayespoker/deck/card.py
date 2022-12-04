"""
Class for a card from a deck of cards. Built in comparators for sorting, and hashable for use in sets.
"""


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.SUITS = ["C", "D", "H", "S"]
        self.RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]

    def __str__(self):
        return self.rank + self.suit

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash((self.suit, self.rank))

    def __eq__(self, other):
        return self.rank == other.rank

    def __lt__(self, other):
        return self.RANKS.index(self.rank) < self.RANKS.index(other.rank)

    def __gt__(self, other):
        return self.RANKS.index(self.rank) > self.RANKS.index(other.rank)

    def __le__(self, other):
        return self.RANKS.index(self.rank) <= self.RANKS.index(other.rank)

    def __ge__(self, other):
        return self.RANKS.index(self.rank) >= self.RANKS.index(other.rank)

    def __ne__(self, other):
        return not self.__eq__(other)
