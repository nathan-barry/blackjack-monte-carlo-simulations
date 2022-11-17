from deck import Deck
from player import Player

# This strategy is fold every single round


class FoldStrategy:
    def __init__(self, shufflePercent=.75, numOfDecks=1, numIterations=100000):
        self.deck = Deck()
        self.deck.generate()
        self.player = Player(False, self.deck)
        self.dealer = Player(True, self.deck)
        self.playerWins = 0
        self.dealerWins = 0
        self.ties = 0
        self.round = 0
        self.numIterations = numIterations
        self.shuffelPercent = shufflePercent
        self.numOfDecks = numOfDecks

    def playRound(self):
        # Player and dealer draw two cards
        playerStatus = self.player.deal()
        dealerStatus = self.dealer.deal()

        # 0 chance of player busting

        # Dealer draws until above 17
        while self.dealer.checkScore() < 17:
            self.dealer.hit()

        # Dealer busts, PLAYER WINS
        if self.dealer.checkScore() > 21:
            self.playerWins += 1

        # Player has higher score, PLAYER WINS
        elif self.player.checkScore() > self.dealer.checkScore():
            self.playerWins += 1

        # Dealer has higher score, DEALER WINS
        elif self.player.checkScore() < self.dealer.checkScore():
            self.dealerWins += 1

        # Player and dealer has same score, TIE
        else:
            self.ties += 1
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
        print(f"Ties: {self.ties}")


b = FoldStrategy()
b.runSimulation()
