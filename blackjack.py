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

    def printSplitScores(self):
        print(
            f"First Hand: {self.player.checkScore()}    Second Hand: {self.player.checkScoreSplit()}    Dealer's Score: {self.dealer.checkScore()}")

    def playRound(self):
        playerStatus = self.player.deal()
        dealerStatus = self.dealer.deal()

        betNotValid = True
        print(f"Cash: {self.cash}\n")
        while betNotValid:
            betAmount = input(f"Bet Amount (default {self.tableMinimum}): ")
            if betAmount == "":
                betAmount = 10
                betNotValid = False
            if self.cash - int(betAmount) >= 0:
                betNotValid = False
                betAmount = int(betAmount)

        self.cash -= betAmount
        betAmount2 = betAmount

        subprocess.run('clear', shell=True)

        self.player.show()

        if playerStatus == 1:
            print('Player got Blackjack!')
            self.playerScore += 1
            if dealerStatus == 1:
                print("Player and Dealer got Blackjack (TIE)")
                self.playerScore -= 1
                return 1
            self.cash += betAmount + (betAmount) * 1.5  # 3/2 payout
            return 1

        cmd = ""

        split = False
        canSplit = False
        canDouble = False
        hasDoubled = False
        hasSplit = False
        handOneDone = False
        hand1bj = False
        hand2bj = False

        if (len(self.player.cards) == 2) and self.player.cards[0].value == self.player.cards[1].value:
            canSplit = True
            print("CAN SPLIT")

        if (self.cash >= betAmount):
            canDouble = True

        while cmd != "2":
            bust = 0
            print(
                f"Dealer's Top Card is: {self.dealer.cards[0].value}{self.dealer.cards[0].suit}")
            if hasSplit:
                print(
                    f"Cash: {self.cash}    Bet Amount 1: {betAmount}    Bet Amount 2: {betAmount2}\n")
            else:
                print(f"Cash: {self.cash}    Bet Amount: {betAmount}\n")

            if hasSplit:
                if handOneDone:
                    print("Second Hand")
                else:
                    print("First Hand")
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
                input("seen")

            if not handOneDone:
                if cmd == "1":
                    bust = self.player.hit()
                    if hasSplit:
                        self.player.showSplit()
                    else:
                        self.player.show()
                elif cmd == "3" and canDouble:
                    self.cash -= betAmount
                    betAmount += betAmount
                    hasDoubled = True
                    bust = self.player.hit()
                    if hasSplit:
                        self.player.showSplit()
                    else:
                        self.player.show()
                    print(
                        f"You drew a {self.player.cards[-1].value}{self.player.cards[-1].suit}")
                    cmd = "2"
                    if hasSplit:
                        cmd = ""
                        self.player.showSplit()
                    handOneDone = True
                elif cmd == "2":
                    handOneDone = True
                    if hasSplit:
                        cmd = ""
                        self.player.showSplit()
                elif cmd == "4" and canSplit:
                    self.player.splitCards.append(self.player.cards.pop())
                    self.cash -= betAmount
                    self.player.hit()
                    self.player.hitSplit()
                    hasSplit = True
                    self.player.showSplit()
                    if self.player.checkScore() == 21:
                        print('First Hand got Blackjack!')
                        handOneDone = True
                        hand1bj = True
                        handOneDone = True
                    if self.player.checkScoreSplit() == 21:
                        print('Second Hand got Blackjack!')
                        hand2bj = True
                else:
                    if hasSplit:
                        self.player.showSplit()
                    else:
                        self.player.show()
                if bust == 1 and not hasSplit:
                    print('Player busted, DEALER WINS\n')
                    handOneDone = True
                    self.playerScore -= 1
                    return 1
                if bust == 1 and hasSplit:
                    print('Hand 1 busted\n')
                    handOneDone = True
                    hasDoubled = False
                    self.playerScore -= 1
            elif hand2bj:
                cmd = "2"
            else:
                if cmd == "1":
                    bust = self.player.hitSplit()
                    self.player.showSplit()
                elif cmd == "3" and canDouble:
                    self.cash -= betAmount2
                    betAmount2 += betAmount2
                    hasDoubled = True
                    bust = self.player.hitSplit()
                    self.player.showSplit()
                    print(
                        f"You drew a {self.player.cards[-1].value}{self.player.cards[-1].suit}")
                    cmd = "2"
                else:
                    self.player.showSplit()
                if bust == 1:
                    print('Hand 2 busted\n')
                    self.playerScore -= 1

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
                self.cash += betAmount * 2
                if hasSplit:
                    self.cash += betAmount2 * 2
                self.playerScore += 1
                return 1
        self.dealer.show()

        if hasSplit:
            self.printSplitScores()
            print("\nFirst Hand")
        else:
            self.printScores()
        if hand1bj:
            print("Hand 1 blackjack")
            self.cash += betAmount * 1.5
        elif self.player.checkScore() > 21:
            print("BUSTED HAND\n")
        elif self.dealer.checkScore() == self.player.checkScore():
            print("TIE\n")
            self.cash += betAmount
        elif self.dealer.checkScore() > self.player.checkScore():
            print("DEALER WINS\n")
            self.playerScore -= 1
        elif self.dealer.checkScore() < self.player.checkScore():
            print("PLAYER WINS\n")
            self.cash += betAmount * 2
            self.playerScore += 1
        if hasSplit:
            print("Second Hand")
            if hand1bj:
                print("Hand 2 blackjack")
                self.cash += betAmount2 * 1.5
            elif self.player.checkScoreSplit() > 21:
                print("BUSTED HAND\n")
            elif self.dealer.checkScore() == self.player.checkScoreSplit():
                print("TIE\n")
                self.cash += betAmount2
            elif self.dealer.checkScore() > self.player.checkScoreSplit():
                print("DEALER WINS\n")
                self.playerScore -= 1
            elif self.dealer.checkScore() < self.player.checkScoreSplit():
                print("PLAYER WINS\n")
                self.cash += betAmount * 2
                self.playerScore += 1

    def playGame(self):
        self.deck.splitsOnly()
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
