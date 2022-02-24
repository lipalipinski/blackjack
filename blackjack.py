"""
Blackjack v1
by JL 2022
"""
import random

suits = {'H': '\u2661', 'D': '\u2662', 'S': '\u2664', 'C': '\u2667'}
rank_values = {'A': 0, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
               '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10,
               'Q': 10, 'K': 10}


def clr_scr():
    """clear console with 100 blank lines"""
    print('\n'*100)


class Card():
    '''
    single card class
    '''

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = rank_values[rank]

    def __str__(self):
        return ''.join([self.rank, suits[self.suit]])

    def __int__(self):
        return self.value

    def __lt__(self, other):
        return self.value < other

    def __le__(self, other):
        return self.value <= other

    def __eq__(self, other):
        return self.value == other

    def __ne__(self, other):
        return self.value != other

    def __gt__(self, other):
        return self.value < other

    def __ge__(self, other):
        return self.value <= other


class Decks():
    '''
    given number of 52 cards decks (shuffled)
    .cut_card - when fewer cards left, get new decks
    '''

    def __init__(self, number=1):
        """
        number - number of decks
        """
        self.decks_number = number
        self.cut_card = random.randint(15, 25)
        self.fresh_cards = []
        self.used_cards = []

        for _ in range(number):
            for suit in suits.keys():
                for rank in rank_values.keys():
                    self.fresh_cards.append(Card(suit, rank))
        self.shuffle()

    def shuffle(self):
        '''
        shuffle the deck
        '''
        random.shuffle(self.fresh_cards)

    def deal(self):
        '''
        pop one card from the deck.
        if cut card met and no cards on the table, join used and shuffle
        if cards on the table shufle used and pop from used
        '''
        # cut card
        if len(self.fresh_cards) < self.cut_card:

            # if no cards on the table
            if len(self.fresh_cards) + len(self.used_cards) == 52 * self.decks_number:
                print('Cut card: shuffling the deck.')
                self.fresh_cards.extend(self.used_cards)
                self.used_cards = []
                self.cut_card = random.randint(15, 25)
                self.shuffle()

            # some cards on the table
            elif len(self.fresh_cards) > 0:
                print('Cut card (dealing fresh)')

            # no fresh cards
            elif len(self.fresh_cards) == 0:
                random.shuffle(self.used_cards)
                print('No new cards, shuffling returned, dealing from returned.')
                return self.used_cards.pop()

        return self.fresh_cards.pop()

    def return_cards(self, cards):
        """
        put card(s) into .used_cards
        """
        if isinstance(cards, list):
            self.used_cards.extend(cards)
        elif isinstance(cards, Card):
            self.used_cards.append(cards)


class Player():
    """
    human blackjack player
    """

    def __init__(self, name, account):
        self.name = name
        self.account = account
        self.bet_ammount = 0
        self.decision_result = None

        self.bjck = ''

    def __str__(self):
        return f'Player {self.name}: {self.account}$'

    def bet(self, min_bet):
        """
        ask player for a bet.
        min_bet - minimal bet
        return False when user wants to quit
        """
        # no money
        if self.account == 0:
            while True:
                inp = input('Game over!\n[Q] to quit:')
                if inp in ['q', 'Q']:
                    return False

        # not enaught money
        elif self.account <= min_bet:

            # decision
            while True:
                inp = input(f'Not enaught money to bet ({self.account}$)\n'
                            'Do you want to go all in? (y/n)')

                # go all in
                if inp in ['y', 'Y']:
                    self.bet_ammount = self.account
                    self.account = 0
                    break

                # end game
                elif inp in ['n', 'N']:
                    while True:
                        inp = input('Game over!\n[Q] to quit:')
                        if inp in ['q', 'Q']:
                            return False

        # money ok
        else:
            value = 0
            while True:
                try:
                    value = input(f'Type your bet value (bank: {self.account}$): ')
                    if value == 'Q':
                        return False
                    value = int(value)
                except ValueError:
                    print('Bet value should be a number.')
                    continue

                if value in range(min_bet, self.account + 1):
                    break
                else:
                    print(f'Bet value should be between {min_bet} and {self.account}')
            self.account -= value
            self.bet_ammount = value

    def win(self, ammount):
        """
        add ammount to account
        """
        self.account += ammount

    def decision(self, hand):
        """
        hand - [] of cards in hand
        return 'h' (hit) / 's' (stand) / 'd' (double-down) False on user quit
        """

        self.decision_result = None
        options = ['h', 's']
        prompt = 'Type [h]it / [s]tand'
        decision = ' '

        # possible double down?
        if self.account >= self.bet_ammount and len(hand) == 2:
            options.append('d')
            prompt += ' / [d]ouble down'

        while True:
            decision = input(prompt + ': ')
            if decision in options:
                self.decision_result = decision
                break
            elif decision == 'Q':
                return False


class Table():
    """
    main table. hold players, cards and display
    """

    def __init__(self, decks_num):
        """decks_num - number of decks"""
        self.deck = Decks(decks_num)
        self.player1 = Player('Player1', 1000)
        self.dealers_cards = []
        self.player_cards = []
        self.round_counter = 1

        # display
        self.dealer_bjck = ''
        self.round_result_disp = ''
        self.messages = []

    def hand_value(self, cards):
        """
        return blackjack hand value. Determine Ace to be 1 or 11.
        Return cards value
        """
        hand_value = 0
        for card in cards:
            if card.value != 0:
                hand_value += card.value
        for card in cards:
            if card.value == 0 and hand_value > 10:
                hand_value += 1
            elif card.value == 0 and hand_value <= 10:
                hand_value += 11
        return hand_value

    def new_game(self):
        """initial deal"""
        for _ in [0, 1]:
            self.dealers_cards.append(self.deck.deal())
            self.player_cards.append(self.deck.deal())

    def dealers_move(self):
        """
        takes cards until 17 or more
        """

        while True:

            hand = self.hand_value(self.dealers_cards)
            if hand >= 17:
                break

            elif hand < 17:
                # dealer takes card
                self.dealers_cards.append(self.deck.deal())

    def player_hit(self):
        """player takes a card"""
        self.player_cards.append(self.deck.deal())

    def is_blackjack(self):
        """
        check if blackjack (after first deal).
        return True if blackjack, False if not
        """
        player_result = self.hand_value(self.player_cards)
        dealer_result = self.hand_value(self.dealers_cards)

        # Tie blackjack
        if player_result == dealer_result == 21:
            self.dealer_bjck = 'Blackjack!'
            self.player1.bjck = 'Blackjack!'
            self.round_result_disp = 'Tie!'
            self.player1.win(self.player1.bet_ammount)
            return True

        # Player blackjack
        elif dealer_result != player_result == 21:
            self.player1.bjck = 'Blackjack!'
            self.round_result_disp = f'Player wins! (Bank +{int(self.player1.bet_ammount*3/2)}$)'
            price = int(self.player1.bet_ammount * 5 / 2)
            self.player1.win(price)
            return True

        # dealer blackjack
        elif player_result != dealer_result == 21:
            self.dealer_bjck = 'Blackjack!'
            self.round_result_disp = f'Player lost! (lost bet: {self.player1.bet_ammount}$)'
            return True

        # no blackjack
        return False

    def round_result(self):
        """
        determine round results
        """
        player_result = self.hand_value(self.player_cards)
        dealer_result = self.hand_value(self.dealers_cards)
        print(f'Player {player_result}\nDealer {dealer_result}')

        if dealer_result > 21:
            self.dealer_bjck = 'Bust!'

        # player over 21
        if player_result > 21:
            self.round_result_disp = f'Player lost! (lost bet: {self.player1.bet_ammount}$)'
            self.player1.bjck = 'Bust!'

        # dealer over 21
        elif dealer_result > 21:
            self.round_result_disp = f'Player wins! (Bank +{self.player1.bet_ammount}$)'
            price = self.player1.bet_ammount * 2
            self.player1.win(price)

        # both 21 or less
        else:

            # tie
            if player_result == dealer_result:
                self.round_result_disp = 'Tie!'
                self.player1.win(self.player1.bet_ammount)

            # player > dealer
            elif player_result > dealer_result:
                self.round_result_disp = f'Player wins! (Bank +{self.player1.bet_ammount}$)'
                price = self.player1.bet_ammount * 2
                self.player1.win(price)

            # player < dealer
            else:
                self.round_result_disp = f'Player lost! (lost bet: {self.player1.bet_ammount}$)'
        self.player1.bet_ammount = 0

    def end_round(self):
        """return cards to deck"""
        self.deck.return_cards(self.dealers_cards)
        self.deck.return_cards(self.player_cards)
        self.dealers_cards = []
        self.player_cards = []

        self.player1.bet_ammount = 0
        self.dealer_bjck = ''
        self.player1.bjck = ''
        self.round_result_disp = ''
        self.round_counter += 1

        decision = input('Press [ENTER] to continnue, press [q] to quit game...')
        if decision in ['Q', 'q']:
            return False

    def display(self, show_all=False):
        """
        display game. show_all - if False show only first dealer's card
        """

        self.player_cards.sort()
        self.dealers_cards.sort()

        p_cards_li = []
        for card in self.player_cards:
            p_cards_li.append(str(card))

        d_cards_li = []
        for card in self.dealers_cards:
            d_cards_li.append(str(card))

        clr_scr()
        print('{0:^60}'.format(f'Round: {self.round_counter}'))
        print('{0:<30}{1:>30}'.format(
               "Dealer:",
               "Player:"
               ))
        print("{0:>60}".format(f"bank: {self.player1.account}$"))
        print("{0:>60}".format(f"bet: {self.player1.bet_ammount}$"))
        print('')

        # show all
        if show_all is True:
            # cards
            print('{0:<30}{1:>30}'.format(' '.join(d_cards_li),
                                          ' '.join(p_cards_li)))
            # hand values
            print('{0:<30}{1:>30}'.format(
                    f'({self.hand_value(self.dealers_cards)})',
                    f'({self.hand_value(self.player_cards)})'
                    ))
            # blackjack / bust
            print('{0:<30}{1:>30}'.format(self.dealer_bjck, self.player1.bjck))

        # hide dealer's cards
        else:
            print('{0:<30}{1:>30}'.format(f'{str(self.dealers_cards[0])} []',
                                          ' '.join(p_cards_li)))
            print('{0:<30}{1:>30}'.format(
                  '(?)',
                  f'({self.hand_value(self.player_cards)})'
                  ))
            print('{0:>60}'.format(self.player1.bjck))

        for message in self.messages:
            print('{0:^60}'.format(message))
        self.messages = []

        print('{0:^60}'.format(self.round_result_disp))


class Menu():
    """
    main menu.
    state 0 - show menu, 1 - new game, 2 - quit game
    """

    def __init__(self):
        self.state = 0
        self.logo = [
                r'     ____   __              __      _               __  ',
                r'    / __ ) / /____ _ _____ / /__   (_)____ _ _____ / /__',
                r'   / __  |/ // __ `// ___// //_/  / // __ `// ___// //_/',
                r'  / /_/ // // /_/ // /__ / ,<    / // /_/ // /__ / ,<   ',
                r' /_____//_/ \__,_/ \___//_/|_|__/ / \__,_/ \___//_/|_|  ',
                r'                             /___/                      ',
                r'                                            by JL       '
                ]

    def display_menu(self):
        """display main menu"""

        clr_scr()
        for line in self.logo:
            print(line)
        print('{0:^60}'.format('Menu:'))
        print('{0:^60}'.format('1 - new game'))
        print('{0:^60}'.format('2 - quit'))

        while True:
            try:
                inp = int(input())
            except ValueError:
                print('Incorrect value')
            if inp in [1, 2]:
                self.state = inp
                break

    def outro(self):
        """goodbye message"""
        clr_scr()
        for line in self.logo:
            print(line)
        print('{0:^60}'.format('Bye!'))
        print('{0:^60}'.format('2022'))


def main():
    """
    main function
    """

    main_menu = Menu()
    while main_menu.state != 2:

        # display menu
        if main_menu.state == 0:
            main_menu.display_menu()

        # new game
        elif main_menu.state == 1:

            table = Table(1)

            # game loop
            while True:

                table.display(True)
                table.new_game()

                # player bets
                if table.player1.bet(50) is False:
                    main_menu.state = 0
                    break

                table.display()

                # check if blackjack
                if table.is_blackjack() is True:
                    # if blackjack start over
                    table.display(True)
                    table.end_round()
                    continue

                # player's decision
                while True:

                    # player quits game
                    if table.player1.decision(table.player_cards) is False:
                        main_menu.state = 0
                        break

                    # player hits - dealer's turn
                    if table.player1.decision_result == 'h':
                        table.player_hit()
                        table.display()

                    # player stands
                    elif table.player1.decision_result == 's':
                        break

                    # player double down
                    if table.player1.decision_result == 'd':
                        table.messages.append('Double down!')
                        table.player1.account -= table.player1.bet_ammount
                        table.player1.bet_ammount *= 2
                        table.player_hit()
                        break

                    # player bust or 21
                    if table.hand_value(table.player_cards) >= 21:
                        break

                table.dealers_move()
                table.round_result()
                table.display(True)

                if table.end_round() is False:
                    main_menu.state = 0
                    break

    # outro
    main_menu.outro()


if __name__ == "__main__":
    main()
