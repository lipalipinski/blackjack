"""
blackjack tests
"""

import unittest
import blackjack


class TestCardInit(unittest.TestCase):
    '''blackjack.Card class initialisation'''

    def test_card_value(self):
        '''getting value from dict'''

        for rank, value in blackjack.rank_values.items():
            test_card = blackjack.Card('H', rank)
            result = test_card.value
            self.assertEqual(result, value)


class TestCardSorting(unittest.TestCase):
    """blackjack.Card class sorting and comparisions"""
    def test_string(self):
        '''casting class as a string'''

        suit = 'H'
        rank = '10'
        result = str(blackjack.Card(suit, rank))
        self.assertEqual(result, '10\u2661')

    def test__lt__(self):
        """less than"""
        card_1 = blackjack.Card('H', 'A')
        card_2 = blackjack.Card('H', 'K')
        self.assertTrue(card_1 < card_2)

    def test__le__(self):
        """less equal"""
        card_1 = blackjack.Card('H', 'A')
        card_2 = blackjack.Card('H', 'A')
        self.assertTrue(card_1 <= card_2)

    def test__eq__(self):
        """equal"""
        card_1 = blackjack.Card('H', 'A')
        card_2 = blackjack.Card('H', 'A')
        self.assertTrue(card_1 == card_2)

    def test__ne__(self):
        """not equal"""
        card_1 = blackjack.Card('H', 'A')
        card_2 = blackjack.Card('H', 'K')
        self.assertTrue(card_1 != card_2)

    def test__gt__(self):
        """greater"""
        card_1 = blackjack.Card('H', 'K')
        card_2 = blackjack.Card('H', 'A')
        self.assertTrue(card_1 > card_2)

    def test__ge__(self):
        """greater equal"""
        card_1 = blackjack.Card('H', 'K')
        card_2 = blackjack.Card('H', 'K')
        self.assertTrue(card_1 >= card_2)

    def test_sorting(self):
        """greater equal"""
        card_1 = blackjack.Card('H', 'K')
        card_2 = blackjack.Card('H', 'A')
        lista = [card_1, card_2]
        lista.sort()
        self.assertEqual(lista, [card_2, card_1])

class TestCardHash(unittest.TestCase):
    """blackjack.Card class hash"""

    def test__hash__(self):
        """Card.__hash__()"""
        card_1 = blackjack.Card('H', 'A')
        card_2 = blackjack.Card('H', 'K')
        test_set = set()
        test_set.add(card_1)
        test_set.add(card_2)
        self.assertEqual(len(test_set), 2)

class TestHand(unittest.TestCase):
    '''
    test class Hand
    '''

    # .hand_value
    def test_hand_value_no_aces_1(self):
        """under 21"""
        test_hand = blackjack.Hand()
        test_hand.extend([blackjack.Card('H', '2'), blackjack.Card('H', 'J')])
        self.assertEqual(int(test_hand), 12)

    def test_hand_value_with_aces_1(self):
        """under 21"""
        test_hand = blackjack.Hand()
        test_hand.extend([blackjack.Card('H', '2'), blackjack.Card('H', 'A')])
        self.assertEqual(int(test_hand), 13)

    def test_hand_value_with_aces_2(self):
        """16 + ace"""
        test_hand = blackjack.Hand()
        test_hand.extend([blackjack.Card('H', 'A'), blackjack.Card('H', '6'),
                    blackjack.Card('H', 'K')])
        self.assertEqual(int(test_hand), 17)

    def test_hand_value_with_aces_3(self):
        """10 + ace == 21"""
        test_hand = blackjack.Hand()
        test_hand.extend([blackjack.Card('H', '10'), blackjack.Card('H', 'A')])
        self.assertEqual(int(test_hand), 21)

    def test_hand_value_with_aces_4(self):
        """two aces"""
        test_hand = blackjack.Hand()
        test_hand.extend([blackjack.Card('H', 'A'), blackjack.Card('H', 'A')])
        self.assertEqual(int(test_hand), 12)

    def test_hand_value_with_aces_5(self):
        """four aces"""
        test_hand = blackjack.Hand()
        test_hand.extend([blackjack.Card('H', 'A'), blackjack.Card('H', 'A'),
                          blackjack.Card('H', 'A'), blackjack.Card('H', 'A')])
        self.assertEqual(int(test_hand), 14)

    def test_hand_value_with_aces_6(self):
        """6 + ace"""
        test_hand = blackjack.Hand()
        test_hand.extend([blackjack.Card('H', '6'), blackjack.Card('H', 'A')])
        self.assertEqual(int(test_hand), 17)


class TestDecks(unittest.TestCase):
    '''tests for blackjack.Deck class'''

    def test_def_cards_quantity(self):
        '''are there 52 unique cards in deck'''
        test_deck = blackjack.Decks()
        uniq_set = set()
        for card in test_deck.fresh_cards:
            uniq_set.add(card)
        self.assertEqual(len(uniq_set), 52)

    def test_cards_quantity(self):
        '''creating multiple decks'''
        test_deck = blackjack.Decks(2)
        self.assertEqual(len(test_deck.fresh_cards), 2*52)

    def test_def_cards_quantity_2(self):
        '''are there 52 unique cards in 2 decks'''
        test_deck = blackjack.Decks(2)
        uniq_set = set()
        for card in test_deck.fresh_cards:
            uniq_set.add(card)
        self.assertEqual(len(uniq_set), 52)

    def test_shuffle(self):
        '''is shuffle shuffling a deck'''

        test_deck = blackjack.Decks()
        not_shuffled = list(test_deck.fresh_cards)
        test_deck.shuffle()
        self.assertNotEqual(not_shuffled, test_deck.fresh_cards)

    def test_return_cards_list(self):
        """return list of cards"""
        lista = [blackjack.Card('Hearts', '2'),
                 blackjack.Card('Hearts', '3')]
        test_deck = blackjack.Decks()
        test_deck.return_cards(lista)
        self.assertEqual(test_deck.used_cards, lista)

    def test_return_cards_card(self):
        """return single card"""
        karta = blackjack.Card('Hearts', '2')
        test_deck = blackjack.Decks()
        test_deck.return_cards(karta)
        self.assertEqual(test_deck.used_cards[0], karta)

    def test_deal_all_cards(self):
        """deal all cards to table (no returns)"""
        test_deck = blackjack.Decks()
        for _ in range(52):
            karta = test_deck.deal()
            self.assertTrue(isinstance(karta, blackjack.Card))
        self.assertEqual(len(test_deck.fresh_cards), 0)

    def test_deal_not_table(self):
        """keep dealing after cut_card (no cards on table)"""
        test_deck = blackjack.Decks()
        for _ in range(53):
            karta = test_deck.deal()
            test_deck.return_cards(karta)
            self.assertTrue(isinstance(karta, blackjack.Card))

    def test_deal_cards_on_table(self):
        """keep dealing after cut_card (cards on table)"""
        test_deck = blackjack.Decks()
        for _ in range(52):
            karta = test_deck.deal()
            test_deck.return_cards(karta)
            self.assertTrue(isinstance(karta, blackjack.Card))
        for _ in range(52):
            karta = test_deck.deal()
            self.assertTrue(isinstance(karta, blackjack.Card))


class TestPlayer(unittest.TestCase):
    """blackjack.Player class"""

    def test_win_1(self):
        """returning bet"""
        test_player = blackjack.Player('x', 1000)
        test_player.bet_ammount = 50
        test_player.win(1)
        self.assertEqual(test_player.account, 1050)

    def test_win_2(self):
        """blackjack (5/2 bet)"""
        test_player = blackjack.Player('x', 1000)
        test_player.bet_ammount = 50
        test_player.win(5/2)
        self.assertEqual(test_player.account, 1125)

    def test_win_3(self):
        """game over test"""
        test_player = blackjack.Player('x', 0)
        test_player.bet_ammount = 50
        test_player.win(0)
        self.assertEqual(test_player.message, 'Game Over!')
        self.assertFalse(test_player.game_on)
        self.assertFalse(test_player.is_in)

    def test_hit(self):
        """player takes card"""
        test_player = blackjack.Player('x', 1000)
        test_deck = blackjack.Decks(1)
        test_player.hit(test_deck)
        self.assertIsInstance(test_player.hand[0], blackjack.Card)


if __name__ == '__main__':
    unittest.main()
