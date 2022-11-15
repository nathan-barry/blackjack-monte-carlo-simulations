from deck import Deck
from player import Player

# This hits if the expected value of the deck is less than 21 - current score


class CountCards:
    def __init__(self, shufflePercent=.75, numOfDecks=1, numIterations=1_00_000):
        self.deck = Deck()
        self.deck.generate()
        self.player = Player(False, self.deck)
        self.dealer = Player(True, self.deck)
        self.playerWins = 0
        self.dealerWins = 0
        self.tie = 0
        self.round = 0
        self.count = 0
        self.totalBlackjacks = 0
        self.playerBlackjacks = 0
        self.dealerBlackjacks = 0
        self.countWhenBlackjack = []
        self.numIterations = numIterations
        self.shuffelPercent = shufflePercent
        self.numOfDecks = numOfDecks

    def playRound(self):
        playerStatus = self.player.deal()
        dealerStatus = self.dealer.deal()

        for card in self.player.cards:
            self.countCard(card)
        self.countCard(self.dealer.cards[0])

        if playerStatus == 1:
            self.playerWins += 1
            self.totalBlackjacks += 1
            self.playerBlackjacks += 1
            self.countWhenBlackjack.append(self.count)
            if dealerStatus == 1:
                self.playerWins -= 1
                self.totalBlackjacks += 1
                self.dealerBlackjacks += 1
                self.countWhenBlackjack.append(self.count)
                return 1
            return 1

        total = 0
        for card in self.deck.cards:
            total += card.price()
        mean = total / len(self.deck.cards)

        while self.player.checkScore() < 21 - mean:
            self.player.hit()
            self.countCard(self.player.cards[len(self.player.cards) - 1])

        self.countCard(self.player.cards[1])
        while self.dealer.checkScore() < 17:
            self.dealer.hit()
            self.countCard(self.dealer.cards[len(self.dealer.cards) - 1])

        if dealerStatus == 1:
            self.totalBlackjacks += 1
            self.countWhenBlackjack.append(self.count)
            self.dealerBlackjacks += 1
            return 1

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

    def countCard(self, card):
        if card.cost <= 9 or card.cost == 1:
            self.count += 1
        elif card.cost >= 6 and card.cost != 1:
            self.count -= 1

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
        print(f"Total Blackjacks: {self.totalBlackjacks}")
        print(f"Player Blackjacks: {self.playerBlackjacks}")
        print(f"Dealer Blackjacks: {self.dealerBlackjacks}")
        totalCount = 0
        for count in self.countWhenBlackjack:
            totalCount += count
        print(
            f"Blackjack Avg. Count: {totalCount / len(self.countWhenBlackjack)}")


b = CountCards()
b.runSimulation()
