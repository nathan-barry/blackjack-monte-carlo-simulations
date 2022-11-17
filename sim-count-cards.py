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
        self.playerBusts = 0
        self.dealerBusts = 0
        self.tie = 0
        self.round = 0
        self.count = 0
        self.totalBlackjacks = 0
        self.playerBlackjacks = 0
        self.dealerBlackjacks = 0
        self.countWhenBlackjack = []
        self.countWhenPlayerBust = []
        self.countWhenDealerBust = []
        self.countWhenPlayerWin = []
        self.countWhenDealerWin = []
        self.countWhenTie = []
        self.numIterations = numIterations
        self.shuffelPercent = shufflePercent
        self.numOfDecks = numOfDecks

    def playRound(self):
        # Player and dealer draw two cards
        playerStatus = self.player.deal()
        dealerStatus = self.dealer.deal()

        # Counts cards in players hands
        for card in self.player.cards:
            self.countCard(card)

        # Counts revealed Dealer card
        self.countCard(self.dealer.cards[0])

        # Player Blackjack
        if playerStatus == 1:
            self.playerBlackjacks += 1
            self.countWhenBlackjack.append(self.count)
            # Dealer Blackjack (if player blackjack)
            if dealerStatus == 1:
                self.playerWins -= 1
                self.totalBlackjacks += 1
                self.dealerBlackjacks += 1
                self.countWhenBlackjack.append(self.count)
                return 1
            self.playerWins += 1
            self.countWhenPlayerWin.append(self.count)
            return 1

        # Calculates expected value of card in remaining deck
        total = 0
        # Sums value of all cards and divides it by number of cards in deck
        for card in self.deck.cards:
            total += card.price()
        mean = total / len(self.deck.cards)

        # Player draws until drawing is expected to bust
        while self.player.checkScore() < 21 - mean:
            self.player.hit()
            # Counts drawn player card
            self.countCard(self.player.cards[len(self.player.cards) - 1])

        # Counts Dealer's second card
        self.countCard(self.dealer.cards[1])

        # Player busts, DEALER WINS
        if self.player.checkScore() > 21:
            self.dealerWins += 1
            self.playerBusts += 1
            self.countWhenPlayerBust.append(self.count)
            self.countWhenDealerWin.append(self.count)
            return  # return early

        # Dealer draws until above 17
        while self.dealer.checkScore() < 17:
            self.dealer.hit()
            # Counts drawn dealer card
            self.countCard(self.dealer.cards[len(self.dealer.cards) - 1])

        # Dealer Blackjack, DEALER WIN
        if dealerStatus == 1:
            self.totalBlackjacks += 1
            self.countWhenBlackjack.append(self.count)
            self.dealerBlackjacks += 1
            self.countWhenDealerWin.append(self.count)
            return 1

        # Dealer busts, PLAYER WINS
        if self.dealer.checkScore() > 21:
            self.playerWins += 1
            self.dealerBusts += 1
            self.countWhenDealerBust.append(self.count)
            self.countWhenPlayerWin.append(self.count)

        # Player has higher score, PLAYER WINS
        elif self.player.checkScore() > self.dealer.checkScore():
            self.playerWins += 1
            self.countWhenPlayerWin.append(self.count)

        # Dealer has higher score, DEALER WINS
        elif self.player.checkScore() < self.dealer.checkScore():
            self.dealerWins += 1
            self.countWhenDealerWin.append(self.count)

        # Player and dealer has same score, TIE
        else:
            self.tie += 1
            self.countWhenTie.append(self.count)

    def countCard(self, card):
        # 10, J, Q, K, A
        if card.cost >= 10 or card.cost == 1:
            self.count -= 1
        # 2, 3, 4, 5, 6
        elif card.cost <= 6 and card.cost != 1:
            self.count += 1

    def runSimulation(self):
        print("Running simulation...")
        for i in range(self.numIterations):
            self.round += 1
            self.player.resetScore()
            self.dealer.resetScore()
            if self.deck.count() <= (52 * self.numOfDecks) * self.shuffelPercent:
                # print("---SHUFFLING---")
                self.count = 0
                self.deck.generate(self.numOfDecks)
            self.playRound()
        print("\n---FINAL OUTPUT---")

        # Calculate average count when player wins
        print(f"Player Score: {self.playerWins}")
        totalCount = 0
        for count in self.countWhenPlayerWin:
            totalCount += count
        print(
            f"Player Win Avg. Count: {totalCount / len(self.countWhenPlayerWin)}\n")

        # Calculate average count when dealer wins
        print(f"Dealer Score: {self.dealerWins}")
        totalCount = 0
        for count in self.countWhenDealerWin:
            totalCount += count
        print(
            f"Dealer Win Avg. Count: {totalCount / len(self.countWhenDealerWin)}\n")

        # Calculate average count when ties
        print(f"Ties: {self.tie}")
        totalCount = 0
        for count in self.countWhenTie:
            totalCount += count
        print(
            f"Tie Avg. Count: {totalCount / len(self.countWhenTie)}\n")

        # Calculate average count when player bust
        print(f"Player Busts: {self.playerBusts}")
        totalCount = 0
        for count in self.countWhenPlayerBust:
            totalCount += count
        print(
            f"Player Bust Avg. Count: {totalCount / len(self.countWhenPlayerBust)}")

        # Calculate average count when dealer bust
        print(f"Dealer Busts: {self.dealerBusts}")
        totalCount = 0
        for count in self.countWhenDealerBust:
            totalCount += count
        print(
            f"Dealer Bust Avg. Count: {totalCount / len(self.countWhenDealerBust)}\n")

        # Calculate average count when blackjack
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
