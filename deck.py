import random
from card import Card


class Deck:
    def __init__(self):
        self.cards = []

    def __repr__(self) -> str:
        res = []
        for card in self.cards:
            res.append(f"{card.value}{card.suit}")
        return str(res)

    def generate(self, numOfDecks=1):
        self.cards = []
        for n in range(numOfDecks):
            for i in range(1, 14):
                for j in range(4):
                    self.cards.append(Card(i, j))
        random.shuffle(self.cards)

    def splitsOnly(self):
        self.cards = []
        for i in range(1, 14):
            for j in range(4):
                self.cards.append(Card(i, j))

    def draw(self, iteration):
        drawnCards = []
        for i in range(iteration):
            card = self.cards.pop()
            drawnCards.append(card)
        return drawnCards

    def count(self):
        return len(self.cards)
