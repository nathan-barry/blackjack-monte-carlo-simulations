from deck import Deck
from player import Player


class Blackjack:
    def __init__(self, shufflePercent=.75, numOfDecks=1):
        self.deck = Deck()
        self.deck.generate()
        self.player = Player(False, self.deck)
        self.dealer = Player(True, self.deck)
        self.playerScore = 0
        self.round = 0
        self.shuffelPercent = shufflePercent
        self.numOfDecks = numOfDecks

    def printScores(self):
        print(
            f"Player's Score: {self.player.checkScore()}    Dealer's Score: {self.dealer.checkScore()}")

    def playRound(self):
        playerStatus = self.player.deal()
        dealerStatus = self.dealer.deal()

        self.player.show()

        if playerStatus == 1:
            print('Player got Blackjack!')
            if dealerStatus == 1:
                print("Player and Dealer got Blackjack (tie)")
            return 1

        cmd = ""

        while cmd != "Stand" and cmd != "s":
            bust = 0
            cmd = input("Hit or Stand? ")

            print("\n")

            if cmd == 'pd':  # pd deck
                if (self.player.deck != self.dealer.deck):
                    raise Exception(
                        "Error: Decks not same between Player and Dealer")
                print(f"Deck: {self.player.deck}")

            if cmd == "Hit" or cmd == "h":
                bust = self.player.hit()
                self.player.show()
            if bust == 1:
                print('Player busted, dealer wins\n')
                self.playerScore -= 1
                return 1

        print("\n")
        self.dealer.show()
        if dealerStatus == 1:
            self.printScores()
            print('Dealer got Blackjack')
            return 1

        while self.dealer.checkScore() < 17:
            if self.dealer.hit() == 1:
                self.dealer.show()
                print("Dealer busted, player wins\n")
                self.playerScore += 1
                return 1
            self.dealer.show()

        self.printScores()
        if self.dealer.checkScore() == self.player.checkScore():
            print("Tie\n")
        elif self.dealer.checkScore() > self.player.checkScore():
            print("Dealer wins\n")
            self.playerScore -= 1
        elif self.dealer.checkScore() < self.player.checkScore():
            print("Player wins\n")
            self.playerScore += 1

    def playGame(self):
        while self.deck:
            self.round += 1
            self.player.resetScore()
            self.dealer.resetScore()
            if self.deck.count() <= (52 * self.numOfDecks) * self.shuffelPercent:
                print("---SHUFFLING---")
                self.deck.generate(self.numOfDecks)
            self.playRound()
            print(f"Deck count: {self.deck.count()}")
            print(f"Round: {self.round}")
            print(f"Player Score: {self.playerScore}\n")

            if input("Play again?: [y]/n ") == 'n':
                break


b = Blackjack()
b.playGame()
