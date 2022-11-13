from deck import Deck
from player import Player

# This strategy is hits if the player score is under X


class HitUnderXStrategy:
    def __init__(self, shufflePercent=.75, numOfDecks=1, numIterations=100000, hitUnder=14):
        self.deck = Deck()
        self.deck.generate()
        self.player = Player(False, self.deck)
        self.dealer = Player(True, self.deck)
        self.playerWins = 0
        self.dealerWins = 0
        self.round = 0
        self.numIterations = numIterations
        self.shuffelPercent = shufflePercent
        self.numOfDecks = numOfDecks
        self.hitUnder = hitUnder

    def playRound(self):
        playerStatus = self.player.deal()
        dealerStatus = self.dealer.deal()

        while self.player.checkScore() < self.hitUnder:
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


hitUnderValues = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
for hitUnderValue in hitUnderValues:
    print(f"Always hit under {hitUnderValue}")
    b = HitUnderXStrategy(hitUnder=hitUnderValue)
    b.runSimulation()
    print()
