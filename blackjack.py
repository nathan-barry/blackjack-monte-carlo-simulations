from deck import Deck
from player import Player


class Blackjack:
    def __init__(self):
        self.deck = Deck()
        self.deck.generate()
        self.player = Player(False, self.deck)
        self.dealer = Player(True, self.deck)

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

            if cmd == 'pd':  # pd deck
                if (self.player.deck != self.dealer.deck):
                    raise Exception(
                        "Error: Decks not same between Player and Dealer")
                print(f"Deck: {self.player.deck}")

            if cmd == "Hit" or cmd == "h":
                bust = self.player.hit()
                self.player.show()
            if bust == 1:
                print('Player busted')
                return 1

        print("\n")
        self.dealer.show()
        if dealerStatus == 1:
            print('Dealer got Blackjack')
            return 1

        while self.dealer.checkScore() < 17:
            if self.dealer.hit() == 1:
                self.dealer.show()
                print("Dealer busted")
                return 1
            self.dealer.show()

        if self.dealer.checkScore() == self.player.checkScore():
            print("Tie")
        elif self.dealer.checkScore() > self.player.checkScore():
            print("Dealer wins")
        elif self.dealer.checkScore() < self.player.checkScore():
            print("Player wins")


b = Blackjack()
b.playRound()
