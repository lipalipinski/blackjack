"""
Blackjack
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
        return ' '.join([self.rank, suits[self.suit]])


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
        if len(self.fresh_cards) < self.cut_card:
            # if no cards on the table
            if len(self.fresh_cards)\
             + len(self.used_cards) == 52 * self.decks_number:
                print('Cut card: shuffling the deck.')
                self.fresh_cards.extend(self.used_cards)
                self.shuffle()
            # some cards on the table
            elif len(self.fresh_cards) == 0:
                random.shuffle(self.used_cards)
                return self.used_cards.pop()
        return self.fresh_cards.pop()

    def return_cards(self, cards):
        """
        put card(s) into .used_cards
        """
        if isinstance(cards, list):
            self.used_cards.extend(cards)
        else:
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

    def __str__(self):
        return f'Player {self.name}: {self.account}$'

    def bet(self, min_bet):
        """
        ask player for a bet.
        min_bet - minimal bet
        return False when user wants to quit
        """
        if self.account < min_bet:
            return False
        else:
            value = 0
            while True:
                try:
                    value = input(f'{self.name} type your bet value (bank: {self.account}$)')
                    if value == 'Q':
                        return False
                    value = int(value)
                except ValueError:
                    print('Bet value should be a number.')
                    continue

                if value in range(min_bet, self.account):
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

    def decision(self):
        """
        returns 'h' (hit) / 's' (stand) / False on user quit
        """

        self.decision_result = None
        decision = ' '
        while True:
            decision = input('Type [h] for hit or [s] for stand: ')
            if decision in ['h', 's']:
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
        self.round_counter = 0

    def hand_value(self, cards):
        """
        return blackjack hand value. Determine Ace to be 1 or 11.
        If value == 21 return True, if over return False
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
        if hand_value > 21:
            return False
        elif hand_value == 21:
            return True
        else:
            return hand_value

    def new_game(self):
        """initial deal"""
        for _ in [0, 1]:
            self.dealers_cards.append(self.deck.deal())
            self.player_cards.append(self.deck.deal())

    def dealers_move(self):
        """
        return True if dealer's 21,
        False if dealer busts or value 17-21 
        """

        while True:
            
            hand = self.hand_value(self.dealers_cards)
            if hand is True:
                # dealer's 21
                return True
            
            elif hand is False:
                # dealer busts
                return False

            elif hand < 17:
                # dealer takes card
                self.dealers_cards.append(self.deck.deal())

            else:
                # dealer's hand
                return hand

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
        if player_result == dealer_result is True:
            print('Blackjack tie!')
            self.player1.win(self.player1.bet_ammount)
            return True
        
        # Player blackjack
        elif dealer_result != player_result is True:
            print('Player has blackjack!')
            price = int(self.player1.bet_ammount * 5 / 2)
            self.player1.win(price)
            return True
        
        # dealer blackjack
        elif player_result != dealer_result is True:
            print('Dealer has blackjack!')
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
        
        # Tie
        if player_result == dealer_result is not False:
            print('Tie!')
            self.player1.win(self.player1.bet_ammount)

        # Player 21 dealer not
        elif dealer_result != player_result is True:
            print('Player wins!')
            price = self.player1.bet_ammount * 2
            self.player1.win(price)
        
        # dealer 21 player not
        elif player_result != dealer_result is True:
            print('Player lost')

        # player wins
        elif player_result > dealer_result:
            print('Player wins!')
            price = self.player1.bet_ammount * 2
            self.player1.win(price)

        # player lost
        elif player_result < dealer_result:
            print('Player lost')

    def end_round(self):
        """return cards to deck"""
        self.deck.return_cards(self.dealers_cards)
        self.deck.return_cards(self.player_cards)
        self.dealers_cards = []
        self.player_cards = []
        self.round_counter += 1

    def display(self, show_all=False):
        """
        display game. show_all - if False show only first dealer's card
        """

        clr_scr()
        print(f'Round: {self.round_counter}')
        print("Dealer's cards:")
        if show_all is True:
            for card in self.dealers_cards:
                print(card)
        else:
            print(self.dealers_cards[0])
            for card in self.dealers_cards[1:]:
                print('[]')
        print(f"Player's cards ({self.hand_value(self.player_cards)}):")
        for card in self.player_cards:
            print(card)
        print(f"Player's bank: {self.player1.account}$")
        print(f"Player's bet: {self.player1.bet_ammount}$")


class Menu():
    """
    main menu.
    state 0 - show menu, 1 - new game, 2 - quit game
    """

    def __init__(self):
        self.state = 0

    def display_menu(self):
        """display main menu"""

        clr_scr()
        print('Blackjack\nJL 2022\n')
        print('1 - new game\n2 - quit')
        while True:
            try:
                inp = int(input())
            except ValueError:
                print('Incorrect value')
            if inp in [1, 2]:
                self.state = inp
                break


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
                table.new_game()

                # player bets
                if table.player1.bet(50) is False:
                    main_menu.state = 0
                    break

                table.display()
                
                # check if blackjack
                if table.is_blackjack() is True:
                    # if blackjack start over
                    table.end_round()
                    continue

                # player's decision
                while True:

                    # player quits game
                    if table.player1.decision() is False:
                        main_menu.state = 0
                        break
                    
                    # player hits - dealer's turn
                    if table.player1.decision_result == 'h':
                        table.player_hit()
                        table.display()

                    # player stands
                    elif table.player1.decision_result == 's':
                        break
                    
                    # player bust
                    if isinstance(table.hand_value(table.player_cards), bool):
                        break
    
                table.dealers_move()
                table.display(True)
                table.round_result()
                table.end_round()


if __name__ == "__main__":
    main()
