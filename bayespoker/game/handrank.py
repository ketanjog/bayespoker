"""
Class to determine the rank of a hand of cards.
"""
from bayespoker.deck import Card


class HandRank:

    HAND_RANKS = [
        "High Card",
        "Pair",
        "Two Pair",
        "Three of a Kind",
        "Straight",
        "Flush",
        "Full House",
        "Four of a Kind",
        "Straight Flush",
        "Royal Flush",
    ]

    def __init__(self, hand, communityCards):

        self.hand = hand
        self.communityCards = communityCards
        self.cards = self.hand + self.communityCards

        # Objects to make it easier to determine hand type
        self.cards = sorted(self.cards, reverse=True)
        self.ranks = sorted([card.rank for card in self.cards], reverse=True)
        self.suits = [card.suit for card in self.cards]
        self.rankCounts = {rank: self.ranks.count(rank) for rank in self.ranks}
        self.suitCounts = {suit: self.suits.count(suit) for suit in self.suits}
        self.rankCountsSorted = sorted(
            self.rankCounts.items(), key=lambda x: x[1], reverse=True
        )
        self.suitCountsSorted = sorted(
            self.suitCounts.items(), key=lambda x: x[1], reverse=True
        )

        self.cardsGroupedByCount = {
            self.rankCountsSorted[i]: [
                x for x in self.cards if (x.rank == self.rankCountsSorted[i])
            ]
            for i in self.rankCountsSorted
        }
        self.cardsGroupedBySuit = {
            self.suitCountsSorted[i]: [
                x for x in self.cards if (x.suit == self.suitCountsSorted[i])
            ]
            for i in self.suitCountsSorted
        }

        # Get the best hand and the cards that make up the best hand
        self.bestHand = self.getBestHand()
        self.bestHandCards = self.getBestHandCards()

    # Get the ranking of the hand type
    def getBestHand(self):
        if self.isRoyalFlush():
            return self.HAND_RANKS.index("Royal Flush")
        elif self.isStraightFlush():
            return self.HAND_RANKS.index("Straight Flush")
        elif self.isFourOfAKind():
            return self.HAND_RANKS.index("Four of a Kind")
        elif self.isFullHouse():
            return self.HAND_RANKS.index("Full House")
        elif self.isFlush():
            return self.HAND_RANKS.index("Flush")
        elif self.isStraight():
            return self.HAND_RANKS.index("Straight")
        elif self.isThreeOfAKind():
            return self.HAND_RANKS.index("Three of a Kind")
        elif self.isTwoPair():
            return self.HAND_RANKS.index("Two Pair")
        elif self.isPair():
            return self.HAND_RANKS.index("Pair")
        else:
            return self.HAND_RANKS.index("High Card")

    # Helper methods to determine hand type
    def isRoyalFlush(self):
        return self.isStraightFlush() and self.ranks[0] == "A"

    def isStraightFlush(self):
        return self.isStraight() and self.isFlush()

    def isFourOfAKind(self):
        return self.rankCountsSorted[0][1] == 4

    def isFullHouse(self):
        return self.rankCountsSorted[0][1] == 3 and self.rankCountsSorted[1][1] == 2

    def isFlush(self):
        return self.suitCountsSorted[0][1] == 5

    def isStraight(self):
        return (
            self.checkConsecutive(self.ranks[:5])
            or self.checkConsecutive(self.ranks[1:6])
            or self.checkConsecutive(self.ranks[2:])
        )

    def isThreeOfAKind(self):
        return self.rankCountsSorted[0][1] == 3

    def isTwoPair(self):
        return self.rankCountsSorted[0][1] == 2 and self.rankCountsSorted[1][1] == 2

    def isPair(self):
        return self.rankCountsSorted[0][1] == 2

    def __str__(self):
        return self.bestHand

    def __repr__(self):
        return self.__str__()

    # A method to return the best 5 card hand from the 7 cards
    def getBestHandCards(self):
        if self.isRoyalFlush():
            if self.checkCardsConsecutive(self.cards[:5]):
                return self.cards[:5]
            elif self.checkCardsConsecutive(self.cards[1:6]):
                return self.cards[1:6]
            else:
                return self.cards[2:]
        elif self.isStraightFlush():
            if self.checkCardsConsecutive(self.cards[:5]):
                return self.cards[:5]
            elif self.checkCardsConsecutive(self.cards[1:6]):
                return self.cards[1:6]
            else:
                return self.cards[2:]
        elif self.isFourOfAKind():
            return self.cardsGroupedByCount[self.rankCountsSorted[0]].append(
                self.cardsGroupedByCount[self.rankCountsSorted[1]][0]
            )
        elif self.isFullHouse():
            return self.cardsGroupedByCount[self.rankCountsSorted[0]].append(
                self.cardsGroupedByCount[self.rankCountsSorted[1]][:2]
            )
        elif self.isFlush():
            return sorted(
                self.cardsGroupedBySuit[self.suitCountsSorted[0]], reverse=True
            )[:5]
        elif self.isStraight():
            if self.checkCardsConsecutive(self.cards[:5]):
                return self.cards[:5]
            elif self.checkCardsConsecutive(self.cards[1:6]):
                return self.cards[1:6]
            else:
                return self.cards[2:]
        elif self.isThreeOfAKind():
            return (
                self.cardsGroupedByCount[self.rankCountsSorted[0]]
                .append(self.cardsGroupedByCount[self.rankCountsSorted[1]][0])
                .append(self.cardsGroupedByCount[self.rankCountsSorted[2]][0])
            )
        elif self.isTwoPair():
            return (
                self.cardsGroupedByCount[self.rankCountsSorted[0]]
                .append(self.cardsGroupedByCount[self.rankCountsSorted[1]])
                .append(self.cardsGroupedByCount[self.rankCountsSorted[2]][0])
            )
        elif self.isPair():
            return (
                self.cardsGroupedByCount[self.rankCountsSorted[0]]
                .append(self.cardsGroupedByCount[self.rankCountsSorted[1]][0])
                .append(self.cardsGroupedByCount[self.rankCountsSorted[2]][0])
                .append(self.cardsGroupedByCount[self.rankCountsSorted[3]][0])
            )
        else:
            return sorted(self.cards, reverse=True)[:5]

    # Add methods to compare two hands
    def __eq__(self, other):
        if self.bestHand == other.bestHand:
            return self.bestHandCards == other.bestHandCards

    def __lt__(self, other):
        if self.bestHand == other.bestHand:
            return self.bestHandCards < other.bestHandCards
        else:
            return self.bestHand < other.bestHand

    def __gt__(self, other):
        if self.bestHand == other.bestHand:
            return self.bestHandCards > other.bestHandCards
        else:
            return self.bestHand > other.bestHand

    def __le__(self, other):
        if self.bestHand == other.bestHand:
            return self.bestHandCards <= other.bestHandCards
        else:
            return self.bestHand <= other.bestHand

    def __ge__(self, other):
        if self.bestHand == other.bestHand:
            return self.bestHandCards >= other.bestHandCards
        else:
            return self.bestHand >= other.bestHand

    def __ne__(self, other):
        if self.bestHand == other.bestHand:
            return self.bestHandCards != other.bestHandCards
        else:
            return self.bestHand != other.bestHand

    # Helper methods to check consecutive ranks
    def checkConsecutive(l):
        return sorted(l) == list(range(min(l), max(l) + 1))

    def checkCardsConsecutive(self, cards):
        return self.checkConsecutive([Card.RANKS.index(card.rank) for card in cards])
