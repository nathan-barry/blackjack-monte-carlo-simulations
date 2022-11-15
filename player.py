from deck import Deck


class Player:
    def __init__(self, isDealer, deck):
        self.cards = []
        self.splitCards = []
        self.isDealer = isDealer
        self.deck = deck
        self.score = 0
        self.splitScore = 0

    def resetScore(self):
        self.cards = []
        self.score = 0
        self.splitCards = []
        self.splitScore = 0

    def hit(self):
        self.cards.extend(self.deck.draw(1))
        self.checkScore()
        if self.score > 21:
            return 1
        return 0

    def deal(self):
        self.cards.extend(self.deck.draw(2))
        self.checkScore()
        if self.score == 21:
            return 1
        return 0

    def checkScore(self):
        aces = 0
        self.score = 0
        for card in self.cards:
            if card.price() == 11:
                aces += 1
            self.score += card.price()

        while aces != 0 and self.score > 21:
            aces -= 1
            self.score -= 10
        return self.score

    def show(self):
        if self.isDealer:
            current = "Dealer"
        else:
            current = "Player"

        print(f"{current}'s Cards")

        for i in self.cards:
            i.show()

        print(f"{current}'s Score: {str(self.score)}\n")

    def hitSplit(self):
        self.splitCards.extend(self.deck.draw(1))
        self.checkScoreSplit()
        if self.splitScore > 21:
            return 1
        return 0

    def checkScoreSplit(self):
        aces = 0
        self.splitScore = 0
        print(f"split deck length: {len(self.splitCards)}")
        for card in self.splitCards:
            if card.price() == 11:
                aces += 1
            self.splitScore += card.price()

        while aces != 0 and self.splitScore > 21:
            aces -= 1
            self.splitScore -= 10
        return self.splitScore

    def showSplit(self):
        print(f"Player's Cards")

        minSize = min(len(self.cards), len(self.splitCards))

        for i in range(minSize):
            print('┌───────┐      ┌───────┐')
            print(
                f'| {self.cards[i].value:<2}    |      | {self.splitCards[i].value:<2}    |')
            print('|       |      |       |')
            print(
                f'|   {self.cards[i].suit}   |      |   {self.splitCards[i].suit}   |')
            print('|       |      |       |')
            print(
                f'|    {self.cards[i].value:>2} |      |    {self.splitCards[i].value:>2} |')
            print('└───────┘      └───────┘')

        if (len(self.cards) > len(self.splitCards)):
            # first hand is larger
            for i in range(minSize, len(self.cards)):
                print('┌───────┐')
                print(f'| {self.cards[i].value:<2}    |')
                print('|       |')
                print(f'|   {self.cards[i].suit}   |')
                print('|       |')
                print(f'|    {self.cards[i].value:>2} |')
                print('└───────┘')
        else:
            # second hand is larger
            for i in range(minSize, len(self.cards)):
                print('               ┌───────┐')
                print(f'               | {self.splitCards[i].value:<2}    |')
                print('               |       |')
                print(f'               |   {self.splitCards[i].suit}   |')
                print('               |       |')
                print(f'               |    {self.splitCards[i].value:>2} |')
                print('               └───────┘')

        print(f"Player's Hand 1: {str(self.score)}")
        print(f"Player's Hand 2: {str(self.splitScore)}\n")
