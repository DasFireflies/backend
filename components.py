import random

class Game:
    # Function initializes a game, including dealing the cards and creating 
    # the pieces
    # Function takes as input the number of players and the list of characters
    # chosen by the players
    def __init__(self, num_players=0, used_characters=[]):
        self.num_players = num_players

        # Pick 3 cards from deck to be the answer
        character_cards = ['miss_scarlet', 'colonel_mustard', 'mrs_white', 'mr_green', 'mrs_peacock', 'professor_plum']
        room_cards = ['study', 'hall', 'lounge', 'library', 'billiard', 'dining', 'conservatory', 'ballroom', 'kitchen']
        weapon_cards = ['rope', 'lead_pipe', 'knife', 'wrench', 'candlestick', 'revolver']
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
        characters = ['miss_scarlet', 'colonel_mustard', 'mrs_white', 'mr_green', 'mrs_peacock', 'professor_plum']
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
        print("*Number of players: "+str(self.num_players)+"\n")
        print("----------------------------------\n")
        print("*Answer: ")
        print(self.answer)
        print("\n----------------------------------\n")
        print("*Pieces:\n")
        for piece in self.pieces:
            piece.print()
            print("----------------------------------\n")




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
        if character == 'colonel_mustard':
            self.position = 'lounge_dining'
            self.color = 'yellow'
        elif character == 'miss_scarlet':
            self.position = 'hall_lounge'
            self.color = 'red'
        elif character == 'professor_plum':
            self.position = 'study_library'
            self.color = 'purple'
        elif character == 'mr_green':
            self.position = 'conservatory_ballroom'
            self.color = 'green'
        elif character == 'mrs_white':
            self.position = 'ballroom_kitchen'
            self.color = 'white'
        elif character == 'mrs_peacock':
            self.position = 'library_conservatory'
            self.color = 'blue'

        self.character = character
        self.is_in_play = is_in_play # whether a player picked this piece
        self.cards = cards 
        self.has_guessed = 0 # whether or not the player has made an accusation
        self.was_just_moved_by_suggestn = 0

    def print(self):
        print("character = "+self.character+'\n')
        print("color = "+self.color+'\n')
        print('is_in_play = '+str(self.is_in_play)+'\n')
        print("cards = ")
        print(self.cards)
        print('\n')
        print("has_guessed = "+str(self.has_guessed)+'\n')
        print("was_just_moved_by_suggestn = "+str(self.was_just_moved_by_suggestn)+'\n\n')


        
                         
