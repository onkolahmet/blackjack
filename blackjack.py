import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
          'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

game_on = True
general = True
adjusted = False


# creating a card object for flexibility of usage
class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        if adjusted and self.rank == "Ace":
            self.value = 1
            return \
                self.rank + " of " + self.suit + " (" + str(self.value) + ") ~ (Ace = 1 instead of 11)"
        else:
            return self.rank + " of " + self.suit + " (" + str(self.value) + ")"


# creating a shuffled deck
class Deck:

    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                card_to_add = Card(suit, rank)
                self.deck.append(card_to_add)

    def __str__(self):
        deck_str = ''
        for card in self.deck:
            deck_str += '\n\t' + card.__str__()

        return "The deck we have is:" + deck_str

    def shuffle(self):
        random.shuffle(self.deck)

    def pick_one(self):
        return self.deck.pop()


# creating card sets that player and dealer has
class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0  # start with zero value
        self.aces = 0  # add an attribute to keep track of aces

    def add_card(self, card):
        ## in case when multiple card objects are drawn
        if type(card) == type([]):
            self.cards.extend(card)
            for ace in card:
                if ace.rank == "Ace":
                    self.aces += 1
                    self.adjust_for_ace()
                else:
                    self.value += card.value

            if self.aces != 0:
                self.adjust_for_ace()

        ## in case when a single card object is drawn
        else:
            self.cards.append(card)
            if card.rank == "Ace":
                self.aces += 1

            self.value += card.value

    def adjust_for_ace(self):
        global adjusted
        while self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1
            adjusted = True


# chips that player have
class Chips:

    def __init__(self, total):
        self.total = total  # default value or supplied by a user input
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


# asking for bet amount
def take_bet(chips):
    while True:
        try:
            chips.bet = int(input("How much chips would you like to bet ?"))
        except:
            print("That's not a valid chip type to bet.Integer expected.")
            continue
        if chips.bet > chips.total:
            print(f"You don't have enough chips ({chips.total}) to take the corresponding bet ({chips.bet}).")
        else:
            break


# player draws card from the deck
def hit(deck, hand):
    hand.add_card(deck.pick_one())
    hand.adjust_for_ace()


# deciding whether drawing a card or giving the turn to dealer
def hit_or_stand(deck, hand):
    global game_on
    while True:
        decision = str(input("Would you like to hit(h) or stand(s) ?"))
        if decision[0].lower() != "s" and decision[0].lower() != "h" and \
                decision.lower() != "stand" and decision.lower() != "lower":
            print("You should enter hit(h) or stand(s)")
            continue
        elif decision[0].lower() == "s":
            print("Player stands. Dealer's turn.")
            game_on = False
        elif decision[0].lower() == "h":
            hit(deck, hand)
        break


# showing the cards with one of the dealer's card as hidden
def show_some(player, dealer):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('', dealer.cards[1])
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    if player.value > 21:
        show_all(player, dealer)


# showing all the cards
def show_all(player, dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =", dealer.value)

    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =", player.value)


def player_busts(chips):
    print("Player busts,Dealer wins!")
    chips.lose_bet()


def player_wins(chips):
    print("Player wins,Dealer busts!")
    chips.win_bet()


def dealer_busts(chips):
    print("Dealer busts,Player wins!")
    chips.win_bet()


def dealer_wins(chips):
    print("Dealer wins,Player busts!")
    chips.lose_bet()


def push():
    print("Game is tied! It's a push.")


while general:
    print("Welcome to the blackjack game simulation!")
    print("Get as close to 21 as possible to win without going over!")
    print("Dealer hits until it reaches to 17 when player stands.")
    deck_to_play = Deck()
    deck_to_play.shuffle()

    # dealing two cards to player
    player_hand = Hand()
    player_hand.add_card(deck_to_play.pick_one())
    player_hand.add_card(deck_to_play.pick_one())

    # dealing two card to dealer
    dealer_hand = Hand()
    dealer_hand.add_card(deck_to_play.pick_one())
    dealer_hand.add_card(deck_to_play.pick_one())

    # prompting the player to bet some chips
    while True:
        try:
            player_chips = Chips(int(input("Enter the amount you want to start with: ")))
        except ValueError:
            print("You should enter an integer")
        else:
            break

    take_bet(player_chips)

    # showing the hand of the player's and half part of the dealer's
    show_some(player_hand, dealer_hand)

    while game_on:
        hit_or_stand(deck_to_play, player_hand)
        show_some(player_hand, dealer_hand)
        if player_hand.value > 21:
            player_busts(player_chips)
            break

    if player_hand.value <= 21:
        while dealer_hand.value < 17:
            hit(deck_to_play, dealer_hand)

        show_all(player_hand, dealer_hand)

        if dealer_hand.value > 21:
            dealer_busts(player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_chips)
        else:
            push()

    # Inform Player about their chips in total
    print("\nPlayer's winnings stand at", player_chips.total)

    while True:
        new_game = input("Would you like to play again ?(Y or N)")
        if new_game[0].lower() != "y" and new_game[0].lower() != "n" \
                and new_game.lower() != "yes" and new_game.lower() != "no":
            print("You entered invalid input.Please type Yes(Y) or No(n)")
            continue
        if new_game[0].lower() == "y":
            game_on = True
            adjusted = False
            break
        elif new_game[0].lower() == "n":
            print("Thanks for playing!")
            game_on = False
            general = False
            break
