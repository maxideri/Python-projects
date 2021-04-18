import random

suits = ('Corazones', 'Diamantes', 'Trebol', 'Picas')
ranks = ('Dos', 'Tres', 'Cuatro', 'Cinco', 'Seis', 'Siete', 'Ocho', 'Nueve', 'Diez', 'J', 'Q', 'K', 'As')
values = {'Dos':2, 'Tres':3, 'Cuatro':4, 'Cinco':5, 'Seis':6, 'Siete':7, 'Ocho':8, 'Nueve':9, 'Diez':10, 'J':10,
             'Q':10, 'K':10, 'As':11}
playing = True

# Clase cartas
class Card:

    def __init__(self,suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f'{self.rank} de {self.suit}'

# Clase mesa con objetos de la clase carta
class Deck:

    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))

    def __str__(self):
        for card in self.deck:
            print (card)

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()

# Clase mano
class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces

    def add_card(self,card):
        self.cards.append(card)
        self.value = self.value + values[card.rank]
        if card.rank == 'Ace':
            self.aces = self.aces + 1  # add to self.aces

    def adjust_for_ace(self):
         while self.value > 21 and self.aces:
            self.value = self.value - 10
            self.aces = self.value - 1 

# Clase fichas
class Chips:

    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0

    def win_bet(self):
        self.total = self.total + self.bet

    def lose_bet(self):
        self.total = self.total - self.bet

# Funcion para recibir apuestas
def take_bet(chips):
    while True:
        try:
            chips.bet = int(input(f'¿Cuantos apuestas? Te quedan {chips.total} fichas: '))
        except:
            print ('Ingresa un valor numérico por favor: ')
        else:
            if chips.bet > chips.total:
                print (f'Su apuesta debe ser menor a {chips.total}')
            else:
                break

# Funcion para pedir una carta
def hit(deck,hand):
    card = deck.deal()
    hand.add_card(card)
    hand.adjust_for_ace()

# Funcion consulta para ver si apuesta o pasa
def hit_or_stand(deck,hand, name):
    global playing  # to control an upcoming while loop

    while True:
        r = input('Quieres una carta más (H) o pasar (P): ')
        if r.upper() == "H":
            hit(deck, hand)
        elif r.upper() == "P":
            print(f"{name} pasa. Es turno de la casa")
            playing = False
        else:
            print('Elija una opción valida por favor')
            continue
        break

# Funcion para mostrar cartas al principio
def show_some(player,dealer, name):
    print("Mano del crupier ")
    print('Primera carta oculta')
    print(f"Segunda carta: {dealer.cards[1]}")

    print(f"\nMano de {name}: ")
    for cards in player.cards:
        print(cards)

# Funcion para mostrar cartas al final
def show_all(player,dealer,name):
    print("\nMano del crupier: ")
    for cards in dealer.cards:
        print(cards)
    print(f"El total es: {dealer.value}")

    print(f"\nMano de {name}: ")
    for cards in player.cards:
        print(cards)
    print(f"El total es: {player.value}")

######## Funciones para saber quien gana ##########
def player_busts(chips,name):
    print(f'{name} supero 21. La casa gana')
    chips.lose_bet()

def player_wins(chips,name):
    print(f"\n{name} gana")
    chips.win_bet()

def dealer_busts(chips,name):
    print (f"\nLa casa supero 21. {name} gana")
    chips.win_bet()

def dealer_wins(chips):
    print("\nLa casa gana")
    chips.lose_bet()

def push(name):
    print(f"\nLa casa y {name} estan empatados")
#####################################################

name = input("Cual es tu nombre: ")
  # Set up the Player's chips
chips = Chips()

while True:
    print("\nBienvenido al blackjack de Casino Deri")
   

    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Prompt the Player for their bet
    take_bet(chips)


    # Show cards (but keep one dealer card hidden)
    print (f"\n########")
    show_some(player_hand,dealer_hand,name)
    
    turno = 1
    while playing:  # recall this variable from our hit_or_stand function

        # Prompt for Player to Hit or Stand
        hit_or_stand(deck,player_hand,name)


        # Show cards (but keep one dealer card hidden)
        print (f'\n########')
        turno = turno + 1
        show_some(player_hand,dealer_hand,name)

        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(chips,name)
            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if player_hand.value <= 21:

        while dealer_hand.value < 17:
            hit(deck,dealer_hand)

        # Show all cards
        print (f'\n########')
        turno = turno + 1
        show_all(player_hand,dealer_hand,name)
        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(chips,name)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(chips)
        elif player_hand.value > dealer_hand.value:
            player_wins(chips,name)
        else:
            push(name)

    # Inform Player of their chips total 
    print (f'Tenes {chips.total} fichas')

    # Ask to play again
    new_game = input("Queres jugar de nuevo: ")
    
    if new_game[0].lower()=='s':
        playing=True
        continue
    else:
        print("Gracias por jugar")
        break
