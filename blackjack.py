from deck import Deck
from player import Player
import subprocess


class Blackjack:
    def __init__(self, shufflePercent=.75, numOfDecks=1):
        self.deck = Deck()
        self.deck.generate()
        self.player = Player(False, self.deck)
        self.dealer = Player(True, self.deck)
        self.playerScore = 0
        self.round = 0
        self.cash = 500
        self.tableMinimum = 10
        self.shuffelPercent = shufflePercent
        self.numOfDecks = numOfDecks

    def printScores(self):
        print(
            f"Player's Score: {self.player.checkScore()}    Dealer's Score: {self.dealer.checkScore()}")

    def playRound(self):
        playerStatus = self.player.deal()
        dealerStatus = self.dealer.deal()

        betNotValid = True
        print(f"Cash: {self.cash}\n")
        while betNotValid:
            betAmount = input(f"Bet Amount (default {self.tableMinimum}): ")
            if self.cash - int(betAmount) >= 0:
                betNotValid = False
                betAmount = int(betAmount)
            if betAmount == "":
                betAmount = 10
                betNotValid = False

        self.cash -= betAmount

        subprocess.run('clear', shell=True)

        self.player.show()

        if playerStatus == 1:
            print('Player got Blackjack!')
            self.playerScore += 1
            if dealerStatus == 1:
                print("Player and Dealer got Blackjack (TIE)")
                self.playerScore -= 1
            return 1

        cmd = ""

        split = False
        canSplit = False
        canDouble = False
        hasDoubled = False
        hasSplit = False

        if (self.player.cards == 2) and self.player.cards[0].value == self.player.cards[1].value:
            canSplit = True

        if (self.cash >= betAmount):
            canDouble = True

        while cmd != "2":
            bust = 0
            print(
                f"Dealer's Top Card is: {self.dealer.cards[0].value}{self.dealer.cards[0].suit}\n")
            print(f"Cash: {self.cash}    Bet Amount: {betAmount}\n")
            if canSplit and canDouble and not hasSplit and not hasDoubled:
                cmd = input("Hit: 1\nStand: 2\nDouble: 3\nSplit: 4\n")
            elif canSplit and not hasSplit:
                cmd = input("Hit: 1\nStand: 2\nSplit: 4\n")
            elif canDouble and not hasDoubled:
                cmd = input("Hit: 1\nStand: 2\nDouble: 3\n")
            else:
                cmd = input("Hit: 1\nStand: 2\n")

            subprocess.run('clear', shell=True)

            if cmd == 'p':  # pd deck
                if (self.player.deck != self.dealer.deck):
                    raise Exception(
                        "Error: Decks not same between Player and Dealer")
                print(f"Deck: {self.player.deck}")

            if cmd == "1":
                bust = self.player.hit()
                self.player.show()
            if cmd == "3" and canDouble:
                self.cash -= betAmount
                betAmount += betAmount
                hasDoubled = True
                self.player.show()
            if cmd == "4" and canSplit:
                self.cas
                hasDoubled = True
                self.player.show()
            if bust == 1:
                print('Player busted, DEALER WINS\n')
                self.playerScore -= 1
                return 1

        subprocess.run('clear', shell=True)
        if dealerStatus == 1:
            self.dealer.show()
            self.printScores()
            print('Dealer got Blackjack, DEALER WINS\n')
            return 1

        while self.dealer.checkScore() < 17:
            if self.dealer.hit() == 1:
                self.dealer.show()
                print("Dealer busted, PLAYER WINS\n")
                self.playerScore += 1
                return 1
        self.dealer.show()

        self.printScores()
        if self.dealer.checkScore() == self.player.checkScore():
            print("TIE\n")
        elif self.dealer.checkScore() > self.player.checkScore():
            print("DEALER WINS\n")
            self.playerScore -= 1
        elif self.dealer.checkScore() < self.player.checkScore():
            print("PLAYER WINS\n")
            self.playerScore += 1

    def playGame(self):
        while self.cash > self.tableMinimum:
            subprocess.run('clear', shell=True)
            self.round += 1
            self.player.resetScore()
            self.dealer.resetScore()
            if self.deck.count() <= (52 * self.numOfDecks) * self.shuffelPercent:
                print("---SHUFFLING---")
                self.deck.generate(self.numOfDecks)
            self.playRound()
            print(f"Deck count: {self.deck.count()}")
            print(f"Round: {self.round}")
            print(f"Cash: {self.cash}\n")

            if input("Play again?: [y]/n ") == 'n':
                break


b = Blackjack()
b.playGame()
