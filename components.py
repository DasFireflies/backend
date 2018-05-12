import random

class Game:
    # Function initializes a game, including dealing the cards and creating 
    # the pieces
    # Function takes as input the number of players and the list of characters
    # chosen by the players
    def __init__(self, num_players=0, used_characters=[]):
        self.num_players = num_players

        # Pick 3 cards from deck to be the answer
        character_cards = ['Lady Scarlet', 'General Mustard', 'Madam White', 'Baron Green', 'Lady Peacock', 'Dr. Plum']
        room_cards = ['Study', 'Great Hall', 'Lounge', 'Library', 'Billiard Room', 'Dining Room', 'Conservatory', 'Ballroom', 'Kitchen']
        weapon_cards = ['Rope', 'Lead Pipe', 'Knife', 'Wrench', 'Candlestick', 'Revolver']
        guilty_character = character_cards[random.randint(0,5)]
        guilty_room = room_cards[random.randint(0,8)]
        guilty_weapon = weapon_cards[random.randint(0,5)]
        self.answer = [guilty_character, guilty_room, guilty_weapon]
        character_cards.remove(guilty_character)
        room_cards.remove(guilty_room)
        weapon_cards.remove(guilty_weapon)
        # Distribute remaining cards
        deck = character_cards + room_cards + weapon_cards
        decks = [None] * num_players
        for i in range(num_players):
            decks[i] = []
        player = 0
        while(len(deck) > 0):
            card = deck[random.randint(0,len(deck)-1)]
            decks[player].append(card)
            deck.remove(card)
            player = (player+1) % num_players

        # Creating game pieces
        pieces = [] 
        characters = ['Lady Scarlet', 'General Mustard', 'Madam White', 'Baron Green', 'Lady Peacock', 'Dr. Plum']
        player_number = 0
        for character in characters:
            if character in used_characters:
                pieces.append(Piece(character, 1, decks[player_number]))
                player_number = player_number + 1
            else:
                pieces.append(Piece(character, 0)) 
        self.pieces = pieces

    def print(self):
        print("Printing game...\n--------------------------------\n")
        print("*Pieces:\n")
        for piece in self.pieces:
            piece.print()
            print("----------------------------------\n")
        print("*Number of players: "+str(self.num_players)+"\n")
        print("----------------------------------\n")
        print("*Answer: ")
        print(self.answer)
        print("\n----------------------------------\n")
        print("************************************")

    def print_locations(self):
        print("Printing piece locations...\n--------------------------------\n")
        for piece in self.pieces:
            piece.print_location()        




class Piece:
    # Function creates a game piece
    # This consists of: 
    #  -assigning it a character,
    #  -its position on the board, 
    #  -the piece's color, 
    #  -whether or not its being used by one of the players,
    #  -the player's deck of cards, 
    #  -whether or not the player has made an accusation,
    #  -whether or not it was just moved into a room by  another player making a suggestion
    def __init__(self, character, is_in_play, cards=[]):
        if character == 'General Mustard':
            self.position = 'Hall 5'
            self.color = 'yellow'
        elif character == 'Lady Scarlet':
            self.position = 'Hall 2'
            self.color = 'red'
        elif character == 'Dr. Plum':
            self.position = 'Hall 3'
            self.color = 'purple'
        elif character == 'Baron Green':
            self.position = 'Hall 11'
            self.color = 'green'
        elif character == 'Madam White':
            self.position = 'Hall 12'
            self.color = 'white'
        elif character == 'Lady Peacock':
            self.position = 'Hall 8'
            self.color = 'blue'

        self.character = character
        self.is_in_play = is_in_play # whether a player picked this piece
        self.cards = cards 
        self.has_guessed = 0 # whether or not the player has made an accusation
        self.was_just_moved_by_suggestn = 0

    def print(self):
        print("character = "+self.character)
        print("position = "+self.position)
        print("color = "+self.color)
        print('is_in_play = '+str(self.is_in_play))
        print("cards = ")
        print(self.cards)
        print("has_guessed = "+str(self.has_guessed))
        print("was_just_moved_by_suggestn = "+str(self.was_just_moved_by_suggestn)+'\n')

    def print_location(self):
        print(self.character +": position = "+self.position)
    
                         
