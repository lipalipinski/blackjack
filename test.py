"""
blackjack tests
"""

import unittest
import blackjack


class TestCard(unittest.TestCase):
    '''tests for blackjack.Card class'''

    def test_card_value(self):
        '''getting value from dict'''

        for rank, value in blackjack.rank_values.items():
            test_card = blackjack.Card('Hearts', rank)
            result = test_card.value
            self.assertEqual(result, value)

    def test_string(self):
        '''casting class as a string'''

        suit = 'H'
        rank = '10'
        result = str(blackjack.Card(suit, rank))
        self.assertEqual(result, '10 \u2661')


class TestDecks(unittest.TestCase):
    '''tests for blackjack.Deck class'''

    def test_def_cards_quantity(self):
        '''are there 52 cards in deck'''
        test_deck = blackjack.Decks()
        self.assertEqual(len(test_deck.fresh_cards), 52)

    def test_cards_quantity(self):
        '''are there 52 cards in deck'''
        test_deck = blackjack.Decks(2)
        self.assertEqual(len(test_deck.fresh_cards), 2*52)

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


class TestTable(unittest.TestCase):
    """test blackjack.Table class"""

    # .new_game
    def test_new_game(self):
        """take cards from deck"""
        test_table = blackjack.Table(1)
        test_table.new_game()
        self.assertEqual(len(test_table.deck.fresh_cards), 48)

    def test_new_game_2(self):
        """cards on the table"""
        test_table = blackjack.Table(1)
        test_table.new_game()
        self.assertEqual(len(test_table.player_cards), 2)
        self.assertEqual(len(test_table.dealers_cards), 2)

    # .end_round
    def test_end_round(self):
        """return cards to deck"""
        test_table = blackjack.Table(1)
        test_table.new_game()
        test_table.end_round()
        self.assertEqual(len(test_table.deck.used_cards), 4)

    # .hand_value
    def test_hand_value_no_aces_1(self):
        """under 21"""
        test_table = blackjack.Table(1)
        card_set = [blackjack.Card('H', '2'), blackjack.Card('H', 'J')]
        self.assertEqual(test_table.hand_value(card_set), 12)

    def test_hand_value_no_aces_2(self):
        """over 21"""
        test_table = blackjack.Table(1)
        card_set = [blackjack.Card('H', 'K'), blackjack.Card('H', 'J'),
                    blackjack.Card('H', '2')]
        self.assertFalse(test_table.hand_value(card_set))

    def test_hand_value_no_aces_3(self):
        """21"""
        test_table = blackjack.Table(1)
        card_set = [blackjack.Card('H', 'K'), blackjack.Card('H', '6'),
                    blackjack.Card('H', '5')]
        self.assertTrue(test_table.hand_value(card_set))

    def test_hand_value_with_aces_1(self):
        """under 21"""
        test_table = blackjack.Table(1)
        card_set = [blackjack.Card('H', '2'), blackjack.Card('H', 'A')]
        self.assertEqual(test_table.hand_value(card_set), 13)

    def test_hand_value_with_aces_2(self):
        """16 + ace"""
        test_table = blackjack.Table(1)
        card_set = [blackjack.Card('H', 'A'), blackjack.Card('H', '6'),
                    blackjack.Card('H', 'K')]
        self.assertEqual(test_table.hand_value(card_set), 17)

    def test_hand_value_with_aces_3(self):
        """10 + ace == 21"""
        test_table = blackjack.Table(1)
        card_set = [blackjack.Card('H', '10'), blackjack.Card('H', 'A')]
        self.assertTrue(test_table.hand_value(card_set))

    def test_hand_value_with_aces_4(self):
        """two aces"""
        test_table = blackjack.Table(1)
        card_set = [blackjack.Card('H', 'A'), blackjack.Card('H', 'A')]
        self.assertEqual(test_table.hand_value(card_set), 12)

    def test_hand_value_with_aces_5(self):
        """four aces"""
        test_table = blackjack.Table(1)
        card_set = [blackjack.Card('H', 'A'), blackjack.Card('H', 'A'),
                    blackjack.Card('H', 'A'), blackjack.Card('H', 'A')]
        self.assertEqual(test_table.hand_value(card_set), 14)

    def test_hand_value_with_aces_6(self):
        """6 + ace"""
        test_table = blackjack.Table(1)
        card_set = [blackjack.Card('H', '6'), blackjack.Card('H', 'A')]
        self.assertEqual(test_table.hand_value(card_set), 17)

    # dealers move
    def test_dealers_move_1(self):
        """dealer's blackjack"""
        test_table = blackjack.Table(1)
        test_table.dealers_cards = [blackjack.Card('H', 'K'),
                                    blackjack.Card('H', 'A')]
        self.assertTrue(test_table.dealers_move())

    def test_dealers_move_2(self):
        """dealer busts"""
        test_table = blackjack.Table(1)
        test_table.dealers_cards = [blackjack.Card('H', '8'),
                                    blackjack.Card('H', '8'),
                                    blackjack.Card('H', '6')]
        self.assertFalse(test_table.dealers_move())

    def test_dealers_move_3(self):
        """input less than 17"""
        test_table = blackjack.Table(1)
        test_table.dealers_cards = [blackjack.Card('H', '9'),
                                    blackjack.Card('H', '9')]
        result = test_table.dealers_move()
        expected = [True, False]
        expected.extend([x for x in range(17, 22)])
        self.assertIn(result, expected)

    def test_dealers_move_4(self):
        """input in (17,21)"""
        test_table = blackjack.Table(1)
        test_table.dealers_cards = [blackjack.Card('H', '9'),
                                    blackjack.Card('H', '9')]
        self.assertEqual(test_table.dealers_move(), 18)

    def test_player_hit(self):
        """player takes card"""
        test_table = blackjack.Table(1)
        test_table.player_hit()
        self.assertIsInstance(test_table.player_cards[0], blackjack.Card)



class TestPlayer(unittest.TestCase):
    """blackjack.Player class"""

    def test_win(self):
        """adding to account"""
        test_player = blackjack.Player('x', 0)
        test_player.win(10)
        self.assertEqual(test_player.account, 10)


if __name__ == '__main__':
    unittest.main()
