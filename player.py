from deck import Deck


class Player:
    def __init__(self, isDealer, deck):
        self.cards = []
        self.isDealer = isDealer
        self.deck = deck
        self.score = 0

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
        counter = 0
        self.score = 0
        for card in self.cards:
            if card.price() == 11:
                counter += 1
            self.score += card.price()

        while counter != 0 and self.score > 21:
            counter -= 1
            self.score -= 10
        return self.score

    def show(self):
        if self.isDealer:
            print("Dealer's Cards")
        else:
            print("Player's Cards")

        for i in self.cards:
            i.show()

        print("Score: " + str(self.score))
