from deck import Deck
from player import Player

# This strategy is hits if the player score is under X


class HitUnderXStrategy:
    def __init__(self, shufflePercent=.75, numOfDecks=1, numIterations=1_00_000, hitUnder=14):
        self.deck = Deck()
        self.deck.generate()
        self.player = Player(False, self.deck)
        self.dealer = Player(True, self.deck)
        self.playerWins = 0
        self.dealerWins = 0
        self.playerBusts = 0
        self.dealerBusts = 0
        self.tie = 0
        self.round = 0
        self.numIterations = numIterations
        self.shuffelPercent = shufflePercent
        self.numOfDecks = numOfDecks
        self.hitUnder = hitUnder

    def playRound(self):
        # Player and dealer draw two cards
        playerStatus = self.player.deal()
        dealerStatus = self.dealer.deal()

        # Player draws until above X
        while self.player.checkScore() < self.hitUnder:
            self.player.hit()

        # Player busts, DEALER WINS
        if self.player.checkScore() > 21:
            self.dealerWins += 1
            self.playerBusts += 1
            return  # return early

        # Dealer draws until above 17
        while self.dealer.checkScore() < 17:
            self.dealer.hit()

        # Dealer busts, PLAYER WINS
        if self.dealer.checkScore() > 21:
            self.playerWins += 1
            self.dealerBusts += 1

        # Player has higher score, PLAYER WINS
        elif self.player.checkScore() > self.dealer.checkScore():
            self.playerWins += 1

        # Dealer has higher score, DEALER WINS
        elif self.player.checkScore() < self.dealer.checkScore():
            self.dealerWins += 1

        # Player and dealer has same score, TIE
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
        print(f"Ties: {self.tie}\n")

        print(f"Player Busts: {self.playerBusts}")
        print(f"Dealer Busts: {self.dealerBusts}")


hitUnderValues = [12, 13, 14, 15, 16, 17]
for hitUnderValue in hitUnderValues:
    print(f"Always hit under {hitUnderValue}")
    b = HitUnderXStrategy(hitUnder=hitUnderValue)
    b.runSimulation()
    print()
