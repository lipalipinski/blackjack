import unittest
import blackjack


class TestCard(unittest.TestCase):
    '''tests for war.Card class'''

    def test_card_value(self):
        '''getting value from dict'''

        for rank, value in blackjack.values.items():
            test_card = blackjack.Card('Hearts', rank)
            result = test_card.value
            self.assertEqual(result, value)

    def test_string(self):
        '''casting class as a string'''

        suit = 'Hearts'
        rank = 'Ten'
        result = str(blackjack.Card(suit, rank))
        self.assertEqual(result, 'Ten of Hearts')


class TestDeck(unittest.TestCase):
    '''tests for war.Deck class'''

    def test_cards_quantity(self):
        '''are there 52 cards in deck'''
        test_deck = blackjack.Deck()
        self.assertEqual(len(test_deck.all_cards), 52)

    def test_shuffle(self):
        '''is shuffle shuffling a deck'''

        test_deck = blackjack.Deck()
        not_shuffled = list(test_deck.all_cards)
        test_deck.shuffle()
        self.assertNotEqual(not_shuffled, test_deck.all_cards)


if __name__ == '__main__':
    unittest.main()
    