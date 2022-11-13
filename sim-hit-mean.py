from deck import Deck
from player import Player

# This hits if the expected value of the deck is less than 21 - current score


class HitExpectedStrategy:
    def __init__(self, shufflePercent=.75, numOfDecks=1, numIterations=100000):
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

    def playRound(self):
        playerStatus = self.player.deal()
        dealerStatus = self.dealer.deal()

        while self.dealer.checkScore() < 17:
            self.dealer.hit()

        if self.dealer.checkScore() > 21:
            self.playerWins += 1
            # print(
            #     f"Player Score: {self.player.score}    Dealer Score: {self.dealer.score}    PLAYER WINS")
        else:
            self.dealerWins += 1
            # print(
            #     f"Player Score: {self.player.score}    Dealer Score: {self.dealer.score}    DEALER WINS")

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


b = FoldStrategy()
b.runSimulation()
