"""
A class to run a game of poker. The game is played with a standard 52 card deck, and the game is played with 2-10 players.

This class is responsible for dealing the cards, and determining the winner of the game.

This is the Texas Hold'em variant of poker, which is the most popular variant of poker in the world.
"""

from bayespoker.deck.deck import Deck
from bayespoker.game.player import Player
from bayespoker.game.handrank import HandRank


class Bet:
    def __init__(self, player, amount):
        self.player = player
        self.amount = amount

    def __str__(self):
        return f"{self.player.name} bets {self.amount}"

    def __repr__(self):
        return self.__str__()


class Game:
    def __init__(self, players, bigBlind, smallBlind, ante):
        self.players = players
        self.bigBlind = bigBlind
        self.smallBlind = smallBlind
        self.ante = ante
        self.deck = Deck()
        self.pot = 0
        self.bets = {}
        self.bettingRound = 0
        self.bettingOrder = []
        self.communityCards = []
        self.winner = None
        self.winningHand = None
        self.roundConlude = False
        self.activePlayers = self.players

    def __str__(self):
        return str(
            f"Texas HoldEm %d\\%d Game, %d players"
            % (self.bigBlind, self.smallBlind, len(self.players))
        )

    def __repr__(self):
        return self.__str__()

    def deal(self):

        # Set game state
        self.bettingRound = 0
        self.bets = {}
        self.pot = 0
        self.communityCards = []
        self.winner = None
        self.winningHand = None

        # Shuffle the deck
        self.deck.reset()
        self.deck.shuffle()

        # Set betting order
        self.players.append(self.players.pop(0))
        self.bettingOrder = self.players

        # Deal the cards
        for player in self.players:
            player.receiveHand(self.deck.dealHand())

        # Collect Small blind
        self.bets[self.bettingOrder[0]] = Bet(self.bettingOrder[0], self.smallBlind)

        # Collect Big blind
        self.bets[self.bettingOrder[1]] = Bet(self.bettingOrder[1], self.bigBlind)

        # Collect Ante
        for player in self.players:
            self.bets[player] = Bet(player, self.ante)

        # Deduct from bankrolls and add to pot
        for player in self.players:
            player.bankroll -= self.bets[player].amount
            self.pot += self.bets[player].amount

    def dealFlop(self):
        self.communityCards += self.deck.dealFlop()

    def dealTurn(self):
        self.communityCards += self.deck.dealTurn()

    def dealRiver(self):
        self.communityCards += self.deck.dealRiver()

    def showdown(self):

        # Determine winner
        winners = {}
        for player in self.players:
            hand = HandRank(player.hand, self.communityCards)
            if len(winners) == 0:
                winners.add(player)
            else:
                currentWinner = next(iter(winners))
                if hand > currentWinner.hand:
                    winners = {player}
                elif hand == currentWinner.hand:
                    winners.append(player)

        # Pay out winner
        for winner in winners:
            winner.bankroll += self.pot / len(winners)

    def play(self):

        # Deal the cards
        self.deal()

        # Pre-Flop
        self.playBettingRound()

        # Flop
        self.communityCards += self.deck.dealFlop()
        self.playBettingRound()

        # Turn
        self.communityCards += self.deck.dealTurn()
        self.playBettingRound()

        # River
        self.communityCards += self.deck.dealRiver()
        self.playBettingRound()

        # Showdown
        self.showdown()

    # Check if the betting round is over
    def checkRoundConclude(self):
        # Check if all players have bet the same amount
        # If so, the round is over
        betAmounts = [bet.amount for bet in self.bets.values()][-self.activePlayers :]
        betAmounts = [i for i in betAmounts if i != 0]

        # Edit bettings order to reflect new active players
        self.bettingOrder = [
            self.bettingOrder[i]
            for i in range(len(self.bettingOrder))
            if self.bets[-(self.activePlayers - i)] != 0
        ]

        # Set new active players
        self.activePlayers = len(betAmounts)

        if len(set(betAmounts)) == 1:
            return True
        else:
            return False

    # Play a betting round
    def playBettingRound(self):

        # Set game state
        self.bettingRound += 1
        self.bets = {}

        # Set betting order
        self.bettingOrder = self.players

        # Play betting round
        while not self.roundConclude:
            for player in self.bettingOrder:
                self.bets.append(Bet(player, player.play(self)))

                # Deduct from bankrolls and add to pot
                player.bankroll -= self.bets[player].amount
                self.pot += self.bets[player].amount

            # Check if round is over
            self.roundConclude = self.checkRoundConclude()
