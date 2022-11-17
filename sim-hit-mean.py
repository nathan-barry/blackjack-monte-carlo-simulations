from deck import Deck
from player import Player

# This hits if the expected value of the deck is less than 21 - current score


class HitExpectedStrategy:
    def __init__(self, shufflePercent=.75, numOfDecks=1, numIterations=1_000_000):
        self.deck = Deck()
        self.deck.generate()
        self.player = Player(False, self.deck)
        self.dealer = Player(True, self.deck)
        self.playerWins = 0
        self.dealerWins = 0
        self.tie = 0
        self.round = 0
        self.numIterations = numIterations
        self.shuffelPercent = shufflePercent
        self.numOfDecks = numOfDecks

    def playRound(self):
        playerStatus = self.player.deal()
        dealerStatus = self.dealer.deal()

        total = 0
        for card in self.deck.cards:
            total += card.price()
        mean = total / len(self.deck.cards)

        while self.player.checkScore() < 21 - mean:
            self.player.hit()

        while self.dealer.checkScore() < 17:
            self.dealer.hit()

        if self.player.checkScore() > 21:
            self.dealerWins += 1
        elif self.dealer.checkScore() > 21:
            self.playerWins += 1
        elif self.player.checkScore() > self.dealer.checkScore():
            self.playerWins += 1
        elif self.player.checkScore() < self.dealer.checkScore():
            self.dealerWins += 1
        else:
            self.tie += 1

    def runSimulation(self):
        print("Running simulation...")
        for i in range(self.numIterations):
            self.round += 1
            self.player.resetScore()
            self.dealer.resetScore()
            if self.deck.count() <= (52 * self.numOfDecks) * self.shuffelPercent:
                # print("---SHUFFLING---")
                self.deck.generate(self.numOfDecks)
            self.playRound()
        print("\n---FINAL OUTPUT---")
        print(f"Player Score: {self.playerWins}")
        print(f"Dealer Score: {self.dealerWins}")
        print(f"Ties: {self.tie}")


b = HitExpectedStrategy()
b.runSimulation()

# ---FINAL OUTPUT---
# Player Score: 383661
# Dealer Score: 565375
