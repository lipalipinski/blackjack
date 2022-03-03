"""
Blackjack v2
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
        return self.value > other

    def __ge__(self, other):
        return self.value >= other

    def __hash__(self):
        return hash((self.suit, self.rank))


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
        self.messages = []

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
                self.messages.append('Cut card: shuffling the deck.')
                self.fresh_cards.extend(self.used_cards)
                self.used_cards = []
                self.cut_card = random.randint(15, 25)
                self.shuffle()

            # some cards on the table
            elif len(self.fresh_cards) > 0:
                self.messages.append('Cut card (dealing fresh)')

            # no fresh cards
            elif len(self.fresh_cards) == 0:
                random.shuffle(self.used_cards)
                self.messages.append('No new cards, shuffling returned, dealing from returned.')
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
        elif isinstance(cards, Hand):
            self.used_cards.append(cards)


class Hand(list):
    """
    blackjack hand of cards
    """

    def __int__(self):
        """
        return blackjack hand value. Determine Ace to be 1 or 11.
        """
        hand_value = 0
        for card in self:
            if card.value != 0:
                hand_value += card.value
        for card in self:
            if card.value == 0 and hand_value > 10:
                hand_value += 1
            elif card.value == 0 and hand_value <= 10:
                hand_value += 11
        return hand_value

    def __str__(self):
        self.sort()
        return ' '.join([str(card) for card in self])


class Player():
    """
    human blackjack player
    """

    def __init__(self, name, account):
        self.name = name
        self.account = account

        # player can and wants to play
        self.is_in = True
        # player has decision to make
        self.game_on = True

        self.bet_ammount = 0
        self.hand = Hand()
        self.decision_result = None
        self.message = ''

    def __str__(self):
        return f'Player {self.name}: {self.account}$'

    def bet(self, min_bet):
        """
        ask player for a bet.
        min_bet - minimal bet
        return False when user wants to quit
        """
        # not enaught money
        if self.account <= min_bet:

            # decision
            while True:
                inp = input(f'{self.name}: not enaught money to bet ({self.account}$)\n'
                            'Do you want to go all in? (y/n)')

                # go all in
                if inp in ['y', 'Y']:
                    self.bet_ammount = self.account
                    self.account = 0
                    break

                # end game
                elif inp in ['n', 'N']:
                    self.game_on = False
                    self.is_in = False
                    self.message = 'Game Over!'
                    return False

        # money ok
        else:
            value = 0
            while True:
                try:
                    value = input(f'{self.name}, type your bet value (bank: {self.account}$): ')

                    if value == 'Q':
                        self.game_on = False
                        self.is_in = False
                        self.message = 'Game Over!'
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

    def hit(self, deck):
        """player takes a cardfrom a deck"""
        self.hand.append(deck.deal())

    def win(self, ratio):
        """
        add bet_ammount * ratio to credit,
        check if game over, if so set self.message, game_on, is_in
        """
        self.account += int(self.bet_ammount * ratio)
        self.bet_ammount = 0

        if self.account == self.bet_ammount == 0:
            self.message = 'Game Over!'
            self.game_on = False
            self.is_in = False

    def decision(self):
        """
        hand - [] of cards in hand
        return 'h' (hit) / 's' (stand) / 'd' (double-down) False on user quit
        """

        self.decision_result = None
        options = ['h', 's']
        prompt = f'{self.name}, type [h]it / [s]tand'
        decision = ' '

        # possible double down?
        if self.account >= self.bet_ammount and len(self.hand) == 2:
            options.append('d')
            prompt += ' / [d]ouble down'

        while True:
            decision = input(prompt + ': ')
            if decision in options:
                self.decision_result = decision
                break
            elif decision == 'Q':
                return False

    def hand_value(self):
        """
        return hand value, set player.message if Bust or Blackjack
        """
        if int(self.hand) > 21:
            self.message = 'Bust!'
        elif int(self.hand) == 21 and len(self.hand) == 2:
            self.message = 'Blackjack!'
        return int(self.hand)


class Table():
    """
    main table. holds players, cards and display
    """

    def __init__(self, start_credit=1000):
        """
        decks_num - number of decks, players_num - number of players,
        start_credit - player's start credit
        """

        self.round_counter = 1

        # players
        self.players = []
        while True:

            # ask for player's name
            name = input("Type player's name and hit [Enter]: ")
            self.players.append(Player(name, start_credit))

            # players full
            if len(self.players) == 3:
                break
            # add another player?
            else:
                another = ''
                while another not in ['y', 'Y', 'n', 'N']:
                    another = input('Do you want to add another player? [Y/N] ')
                if another in ['y', 'Y']:
                    continue
                else:
                    break

        self.deck = Decks(len(self.players))

        # dealer
        self.dealers_cards = Hand()
        self.dealer_bjck = ''

        # display
        self.round_result_disp = []
        self.messages = []

    def new_game(self):
        """initial deal"""

        for _ in [0, 1]:
            self.dealers_cards.append(self.deck.deal())
            for player in self.players:
                if player.is_in is True:
                    player.hit(self.deck)

    def dealers_move(self):
        """
        takes cards until 17 or more
        """

        while True:

            if int(self.dealers_cards) >= 17:
                break

            elif int(self.dealers_cards) < 17:
                # dealer takes card
                self.dealers_cards.append(self.deck.deal())

    def is_blackjack(self):
        """
        check if blackjack (after first deal).
        return True if blackjack, False if not
        adjust player's credit, set player bet = 0
        """
        players_result = [player.hand_value() for player in self.players]
        dealer_result = int(self.dealers_cards)

        # Tie blackjack
        if 21 in players_result and dealer_result == 21:

            for player in self.players:

                if player.is_in is True:

                    # player has blackjack
                    if player.hand_value() == 21:

                        # return bet to player's credit
                        self.round_result_disp.append(
                            f'{player.name}: Blackjack Tie! Bet ({player.bet_ammount}$) is being returned.'
                            )
                        player.win(1)

                    # player lost
                    else:
                        self.round_result_disp.append(
                            f'{player.name} lost! (lost bet: {player.bet_ammount}$)'
                            )
                    player.win(0)

            self.dealer_bjck = 'Blackjack!'
            return True

        # Player blackjack
        elif 21 in players_result and dealer_result != 21:

            for player in self.players:

                if player.is_in is True:

                    # player's blackjack
                    if player.hand_value() == 21:
                        self.round_result_disp.append(
                            f'{player.name} wins! (Bank +{int(player.bet_ammount*3/2)}$)'
                            )
                        player.win(5/2)

                    # player's lost
                    else:
                        self.round_result_disp.append(
                            f'{player.name} lost! (lost bet: {player.bet_ammount}$)'
                            )
                        player.win(0)

            return True

        # dealer blackjack
        elif 21 not in players_result and dealer_result == 21:
            self.dealer_bjck = 'Blackjack!'
            self.round_result_disp.append(
                    'Dealer: Blackjack!'
                )

            # player's loss
            for player in self.players:

                if player.is_in is True:

                    self.round_result_disp.append(
                        f'{player.name} lost! (lost bet: {player.bet_ammount}$)'
                    )
                    player.win(0)

            return True

        # no blackjack
        return False

    def round_result(self):
        """
        determine round results
        """
        for player in self.players:
            player.hand_value()
        dealer_result = int(self.dealers_cards)

        # dealer bust
        if dealer_result > 21:
            self.dealer_bjck = 'Bust!'
            self.round_result_disp.append('Dealer busts!')

            for player in self.players:

                if player.is_in is True:

                    # player wins
                    if player.hand_value() <= 21:
                        self.round_result_disp.append(
                            f'{player.name} wins! (Bank +{player.bet_ammount}$)'
                            )
                        player.win(2)

                    # player bust
                    else:
                        self.round_result_disp.append(
                            f'{player.name} busts! (lost bet: {player.bet_ammount}$)'
                            )
                        player.win(0)

        # dealer <= 21
        else:
            for player in self.players:

                if player.is_in is True:

                    # player bust
                    if player.hand_value() > 21:
                        self.round_result_disp.append(
                            f'{player.name} busts! (lost bet: {player.bet_ammount}$)'
                            )

                        player.win(0)

                    else:

                        # tie
                        if player.hand_value() == dealer_result:
                            self.round_result_disp.append(
                                f'{player.name} ties! Bet ({player.bet_ammount}$) is being returned.'
                                )
                            player.win(1)

                        # win
                        elif player.hand_value() > dealer_result:
                            self.round_result_disp.append(
                                f'{player.name} wins! (Bank +{player.bet_ammount}$)'
                                )
                            player.win(2)
                        # lost
                        else:
                            self.round_result_disp.append(
                                f'{player.name} lost! (lost bet: {player.bet_ammount}$)'
                                )
                            player.win(0)

    def end_round(self):
        """return cards to deck, reset round vars"""
        self.deck.return_cards(self.dealers_cards)
        self.dealers_cards = Hand()

        # reset player rounds
        for player in self.players:
            if player.is_in is True:
                self.deck.return_cards(player.hand)
                player.hand = Hand()
                player.bet_ammount = 0
                player.message = ''
                player.game_on = True
            else:
                player.hand = Hand()
                player.message = 'Game Over!'

        self.dealer_bjck = ''
        self.round_result_disp = []
        self.round_counter += 1

        decision = input('Press [ENTER] to continnue, press [q] to quit game...')
        if decision in ['Q', 'q']:
            return False

    def display(self, show_all=False):
        """
        display game. show_all - if False show only first dealer's card
        """

        # one player
        if len(self.players) == 1:

            clr_scr()
            print('{0:^60}'.format(f'Round: {self.round_counter}'))
            print('{0:<30}{1:>30}'.format(
                "Dealer:",
                f"{self.players[0].name}:"
                ))
            print("{0:>60}".format(f"bank: {self.players[0].account}$"))
            print("{0:>60}".format(f"bet: {self.players[0].bet_ammount}$"))
            print('')

            # show all
            if show_all is True:
                # cards
                print('{0:<30}{1:>30}'.format(str(self.dealers_cards),
                                              str(self.players[0].hand)))
                # hand values
                print('{0:<30}{1:>30}'.format(
                        f'({int(self.dealers_cards)})',
                        f'({self.players[0].hand_value()})'
                        ))
                # blackjack / bust
                print('{0:<30}{1:>30}'.format(self.dealer_bjck, self.players[0].message))

            # hide dealer's cards
            else:
                print('{0:<30}{1:>30}'.format(f'{str(self.dealers_cards[0])} []',
                                              str(self.players[0].hand)))
                print('{0:<30}{1:>30}'.format(
                    '(?)',
                    f'({self.players[0].hand_value()})'
                    ))
                print('{0:>60}'.format(self.players[0].message))

        # multiplayer
        else:

            clr_scr()

            # dealer
            print('{0:^60}'.format(f'Round: {self.round_counter}\n'))
            print('{0:^60}'.format("Dealer:"))

            # dealer show all
            if show_all is True:
                # cards
                print('{0:^60}'.format(str(self.dealers_cards)))
                # hand values
                print('{0:^60}\n'.format(
                    f'({str(int(self.dealers_cards))}){self.dealer_bjck}'
                    ))

            # hide dealer's cards
            else:
                print('{0:^60}'.format(f'{str(self.dealers_cards[0])} []'))
                print('{0:^60}\n'.format('(?)'))

            # players
            columns = ''
            rows = [[], [], [], [], [], [], []]
            for i, player in enumerate(self.players):

                columns += r'{'+str(i)+r':<20}'

                rows[0].append(player.name)
                rows[1].append(f'Credit: {player.account}$')
                rows[2].append(f'Bet: {player.bet_ammount}$')
                rows[3].append('')
                rows[4].append(str(player.hand))
                rows[5].append(f'({player.hand_value()})')
                rows[6].append(player.message)

            for row in rows:
                print(columns.format(*row))

            print('')

        # move deck messages to table messages
        self.messages.extend(self.deck.messages)
        self.deck.messages = []

        for message in self.messages:
            print('{0:^60}'.format(message))
        self.messages = []

        for msg in self.round_result_disp:
            print('{0:^60}'.format(msg))


class Menu():
    """
    main menu.
    state 0 - show menu, 1 - new game,
    2 - about, 3 - quit game
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
        print(*self.logo, sep='\n')
        print('{0:^60}'.format('Menu:'))
        print('{0:^60}'.format('1 - Play Blackjack'))
        print('{0:^60}'.format('2 - About'))
        print('{0:^60}'.format('3 - Quit'))

        while True:

            inp = None
            try:
                inp = int(input())
            except ValueError:
                print('Incorrect value')
            if inp in [1, 2, 3]:
                self.state = inp
                break

    def about(self):
        '''game info'''

        abc = ['                                                        ',
               'Players plays against dealer. Aim is to get as close to ',
               '21 as possible, but not higher! Two = 2, Three = 3 etc..',
               'Face Cards = 10, Ace = 1 or 11, whichever gives better  ',
               'score.                                                  ',
               'Game run:                                               ',
               '1 - players places thair bets                           ',
               '2 - two cards for player (faces up) and for dealer (one ',
               '    up, one down)                                       ',
               '3 - players move: hit (take a card)/stand (pass)/double ',
               '    down (doble the bet and take exactly one card)      ',
               '4 - dealer takes cards until he reaches 17 or more      ',
               '5 - turn result (bet is being returned on tie game)     ',
               '                                                        ',
               'Blackjack (two cards of 21 value) always wins, except   ',
               'for a tie game. Winning with blackjack gives 3/2 of a bet',
               'The deck is being shuffled after reaching a cut card when',
               'there is no cards on the table. Cut card is placed      ',
               'randomly by a dealer (between 15th and 25th cardfrom the',
               'bottom). Number od single decks in a game deck = number ',
               'of players                                              ',         
               '                                                        ',
               'GOOD LUCK!                                              ']

        clr_scr()
        print(*self.logo, sep='\n')
        print(*abc, sep='\n')
        input('Press [ENTER] to exit...')
        self.state = 0

    def outro(self):
        """goodbye message"""
        clr_scr()
        print(*self.logo, sep='\n')
        print('{0:^60}'.format('Bye!'))
        print('{0:^60}'.format('2022'))


def main():
    """
    main function
    """

    main_menu = Menu()
    while main_menu.state != 3:

        # display menu
        if main_menu.state == 0:
            main_menu.display_menu()

        # display about
        if main_menu.state == 2:
            main_menu.about()

        # new game
        elif main_menu.state == 1:

            clr_scr()
            table = Table(1000)

            # game loop
            while True:

                table.display(True)

                # players bet
                for player in table.players:
                    if player.is_in is True:
                        player.bet(50)
                        table.display(True)

                table.new_game()
                table.display()

                # check if blackjack
                if table.is_blackjack() is True:
                    # if blackjack start over
                    table.display(True)
                    table.end_round()
                    continue

                # players decisions
                while any([player.game_on for player in table.players]):

                    for player in table.players:
                        if player.game_on is True:

                            # player quits game
                            if player.decision() is False:
                                player.game_on = False
                                player.is_in = False

                            # player hits - dealer's turn
                            if player.decision_result == 'h':
                                player.hit(table.deck)
                                table.display()

                            # player stands
                            elif player.decision_result == 's':
                                player.game_on = False

                            # player double down
                            if player.decision_result == 'd':
                                table.messages.append(f'{player.name} Double down!')
                                player.account -= player.bet_ammount
                                player.bet_ammount *= 2
                                player.hit(table.deck)
                                player.game_on = False
                                table.display()

                            # player bust or 21
                            if player.hand_value() >= 21:
                                player.game_on = False

                table.dealers_move()
                table.round_result()

                table.display(True)

                if not any([player.is_in for player in table.players]):
                    table.end_round()
                    main_menu.state = 0
                    break

                # [q] for quit
                if table.end_round() is False:
                    main_menu.state = 0
                    break

    # outro
    main_menu.outro()


if __name__ == "__main__":
    main()
