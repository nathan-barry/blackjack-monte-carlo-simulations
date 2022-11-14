from deck import Deck
from player import Player

# This strategy is hits if the player score is under X


class HitUnderXStrategy:
    def __init__(self, shufflePercent=.75, numOfDecks=1, numIterations=1_000_000, hitUnder=14):
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


hitUnderValues = [12, 13, 14, 15, 16, 17]
for hitUnderValue in hitUnderValues:
    print(f"Always hit under {hitUnderValue}")
    b = HitUnderXStrategy(hitUnder=hitUnderValue)
    b.runSimulation()
    print()

# Always hit under 12
# Running simulation...

# ---FINAL OUTPUT---
# Player Score: 415755
# Dealer Score: 518703

# Always hit under 13
# Running simulation...

# ---FINAL OUTPUT---
# Player Score: 418942
# Dealer Score: 509407

# Always hit under 14
# Running simulation...

# ---FINAL OUTPUT---
# Player Score: 420287
# Dealer Score: 500582

# Always hit under 15
# Running simulation...

# ---FINAL OUTPUT---
# Player Score: 418879
# Dealer Score: 494280

# Always hit under 16
# Running simulation...

# ---FINAL OUTPUT---
# Player Score: 415268
# Dealer Score: 490349

# Always hit under 17
# Running simulation...

# ---FINAL OUTPUT---
# Player Score: 409320
# Dealer Score: 489023

# Always hit under 18
# Running simulation...

# ---FINAL OUTPUT---
# Player Score: 398849
# Dealer Score: 512528

# Always hit under 19
# Running simulation...

# ---FINAL OUTPUT---
# Player Score: 363162
# Dealer Score: 564038
