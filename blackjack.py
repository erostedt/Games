from random import shuffle


class BlackJack:

    def __init__(self, players, bets, original_player_count):
        """
        Creates a BlackJack instance
        :param players: How many players.
        :param bets: Each players bet
        :param original_player_count: Number of player in first round
        """
        self.players = players
        self.deck = self.construct_deck()
        self.sums = [0]*original_player_count
        self.bets = bets
        self.dealer = 0
        self.busted = [False]*original_player_count # Which players have busted
        self.wants_to_play = [True]*original_player_count   # Which players didn't stick last turn
        self.original_player_count = original_player_count

    @staticmethod
    def construct_deck():
        """
        Constructs a deck
        :return: Deck
        """
        print('________________________')
        print('Constructs a new deck')
        print('________________________')
        deck = [i for i in range(2, 11) for j in range(4)]
        deck += ['J', 'J', 'J', 'J', 'Q', 'Q', 'Q', 'Q', 'K', 'K', 'K', 'K', 'A', 'A', 'A', 'A']
        shuffle(deck)
        return deck

    def convert_to_number(self, c, is_dealer=False):
        """
        Converts card to value
        :param c: Card c
        :param is_dealer: Check if draw was from dealer or player
        :return: Card value
        """
        if c == 'J' or c == 'Q' or c == 'K':
            if is_dealer:
                print('Dealer got a: {}, this is worth 10 points'.format(c))
            else:
                print('You got a: {}, this is worth 10 points'.format(c))
            return 10
        elif c != 'A':
            if is_dealer:
                print('Dealer got a: {}'.format(c))
            else:
                print('You got a: {}'.format(c))
            return c
        else:
            if is_dealer:
                if self.dealer + 11 > 21:
                    ace = 1
                else:
                    ace = 11
                print('Dealer got an ace and used it as: {}'.format(ace))
                return ace
            ace = 0
            while ace != 1 and ace != 11:
                ace = int(input('You got an ace! Want to use it as 1 or 11? '))
                if ace != 1 and ace != 11:
                    print('Not ok number, try again')
            return ace

    def draw(self):
        """
        Draws a card, if deck is empty, construct a new deck
        :return: drawn card
        """
        if len(self.deck) == 0:
            self.deck = self.construct_deck()
        return self.deck.pop()

    def check_winnings(self):
        """
        Checks the players winning
        :return: Winnings
        """
        winnings = [0]*self.original_player_count
        for player in self.players:
            if self.busted[player]:
                winnings[player] -= self.bets[player]
            else:
                if self.dealer > 21 or self.sums[player] > self.dealer:
                    winnings[player] += int(1.5 * self.bets[player])
                elif self.sums[player] < self.dealer:
                    winnings[player] -= self.bets[player]
        return winnings

    def check_non_busted(self):
        """
        Check which players are not busted
        :return: non_busted players
        """
        non_busted_players = []
        for player in self.players:
            if self.sums[player] <= 21:
                non_busted_players.append(player)
            else:
                self.busted[player] = True
        return non_busted_players

    def display(self):
        """
        Displayes players sums
        """
        print('_______________________________________')
        for player in self.players:
            print('Player: {} has sum of: {}'.format(player+1, self.sums[player]))
        print('_______________________________________')

    def play(self):
        """
        Play the game
        :return: winnings
        """
        game_over = False
        while not game_over:
            self.display()
            'Everybody draw or stay'
            non_busted_players = self.check_non_busted()
            if non_busted_players is not None:
                drawers = 0
                for player in non_busted_players:
                    if self.wants_to_play[player] and self.sums[player] < 21:
                        strategy = int(input('Player: {} Type 1 to draw a card, 0 for staying '.format(player + 1)))
                        if strategy == 0:
                            self.wants_to_play[player] = False
                        else:
                            drawers += 1
                            self.sums[player] += self.convert_to_number(self.draw())
                            if self.sums[player] > 21:
                                print('Busted!')
                if drawers == 0:
                    game_over = True
            else:
                game_over = True

        # Dealers turn
        print('_______________________________________')
        while self.dealer < 17:
            self.dealer += self.convert_to_number(self.draw(), is_dealer=True)
        print('_______________________________________')
        print('Dealer got: ', self.dealer)
        self.display()

        # Report winnings
        winnings = self.check_winnings()
        for player in self.players:
            if winnings[player] >= 0:
                print('Player: {} won {} $'.format(player + 1, winnings[player]))
            else:
                print('Player: {} lost {} $'.format(player + 1, -winnings[player]))
        return winnings


if __name__ == '__main__':
    # Load players and there inserted amounts
    player_count = int(input('How many Players? '))
    players = [player for player in range(player_count)]
    cash = []
    continue_to_play = True
    for player in players:
        money = int(input('Player: {}, insert an amount of dollars: '.format(player + 1)))
        cash.append(money)

    # Main Loop over games until all players are out or players terminate the game
    while continue_to_play:
        # Display and load bets
        print('_______________________________________')
        for player in players:
            print('Player: {} has {} $ left'.format(player+1, cash[player]))
        print('_______________________________________')
        bets = [0]*player_count
        for player in players:
            ok_bet = False
            while 1:
                bet = int(input('Player: {}, bet an amount of dollars: '.format(player + 1)))
                if bet <= cash[player]:
                    bets[player] = bet
                    break
                else:
                    print('You cannot bet that much')

        # Create new BlackJack instance
        bj = BlackJack(players=players, bets=bets, original_player_count=player_count)
        winnings = bj.play()
        print('_______________________________________')
        for player in players:
            cash[player] += winnings[player]
            if cash[player] <= 0:
                print('Player: {} has {} $ left'.format(player + 1, cash[player]))
                print('Player: {} is out'.format(player + 1))
        players = [player for player in players if cash[player] > 0]
        print('_______________________________________')

        # Play another round?
        if len(players) == 0:
            print('All players are out\n')
            continue_to_play = 0
        else:
            continue_to_play = int(input('Type 1 to play again and 0 to quit '))
        if continue_to_play == 0:
            print('Game finished')
