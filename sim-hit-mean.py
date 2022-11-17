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
        self.playerBusts = 0
        self.dealerBusts = 0
        self.tie = 0
        self.round = 0
        self.numIterations = numIterations
        self.shuffelPercent = shufflePercent
        self.numOfDecks = numOfDecks

    def playRound(self):
        # Player and dealer draw two cards
        playerStatus = self.player.deal()
        dealerStatus = self.dealer.deal()

        # Calculates expected value of card in remaining deck
        total = 0
        # Sums value of all cards and divides it by number of cards in deck
        for card in self.deck.cards:
            total += card.price()
        mean = total / len(self.deck.cards)

        # Player draws until drawing is expected to bust
        while self.player.checkScore() < 21 - mean:
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
        print(f"Ties: {self.tie}")


b = HitExpectedStrategy()
b.runSimulation()

# ---FINAL OUTPUT---
# Player Score: 383661
# Dealer Score: 565375
