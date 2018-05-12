import socket
import sys
import time
from threading import Thread
from components import Game, Piece

used_characters = []
players_whove_selected = []
character_assignments = {} #dict of (character, player id) pairs
game_started = 0
num_players = 0
#game_over = 0

# Function handles game initialization for a single player
def initialize_player(id, players):
    global used_characters, players_whove_selected, character_assignments, game_started, num_players
    conn  = players[id]
    # Process input from player until someone presses "Start Game"
    while game_started == 0:
        print("-----------------------------------")
        print("player with id "+str(id)+" is in waiting room. listening...")
        data = conn.recv(1024).decode() 
        if game_started == 1:
            break
        data = data[:-1] # remove \n character
        print ("player with id " + str(id) + " sent: " + str(data) + '\n')
        # data should either be an integer 0-5 indicating character selection/deselection or -1 indicating "start game"
        if data == '-1': # If player pressed "Start Game"
            game_started = 1
            print("player # " + str(id) + "pressed start. game_started set to 1\n")

        # If player has already chosen their character, unassign it
        elif id in players_whove_selected:
            used_characters.remove(data)
            players_whove_selected.remove(id)
            character_assignments.pop(data)
            num_players = num_players-1
            print("Player had already selected. Sending confirmation of deselection  back to player\n")
            data = "1\r\n"
            conn.send(data.encode())
            print("current character assignments:\n")
            print(character_assignments)
            print("\n")
        # If player hasnt chosen character yet and character is unused,
        # assign them that character
        elif data not in used_characters:
            print("Assigning them that character...\n")
            used_characters.append(data)
            players_whove_selected.append(id)
            character_assignments[data] = id
            num_players = num_players+1
            print("Sending 1 back to player for confirmation\n")
            data = "1\r\n"
            conn.send(data.encode())
            print("current character assignments:\n")
            print(character_assignments)
            print("\n")
        # If character is used, don't assign it
        elif data in used_characters:
            print("Sending 0 back to player because character has been taken")
            data = "0\r\n"
            conn.send(data.encode())

        

# Function handles game initialization
# Accepts character selections and creates the playing pieces and game object
def initialize_game():
    global used_characters, players_whove_selected, character_assignments, game_started, num_players
    used_characters = []
    players_whove_selected = []
    character_assignments = {} #dict of (character, player id) pairs
    game_started = 0
    num_players = 0

    players = {} #dict of (player id, socket object) pairs
    
    # Set up connection
    host = "172.31.27.46"
    port = 5000
    mySocket = socket.socket()
    mySocket.bind((host,port))
    mySocket.listen(1)
    mySocket.settimeout(2)
    while game_started == 0:
        try:
            conn, addr = mySocket.accept()      
            id = addr[1]
            print ("Connection from: " + str(addr)+ ". User's id will be " + str(id))
            players[id] = conn
            Thread(target=initialize_player, args=(id, players)).start()
        except Exception as e:
            continue

    # convert keys in character_assignments to strings 
    for key in character_assignments:
        if key == '0':
            character_assignments['Baron Green'] = character_assignments.pop('0')
        elif key == '1':
            character_assignments['Lady Peacock'] = character_assignments.pop('1')
        elif key == '2':
            character_assignments['Madam White'] = character_assignments.pop('2')
        elif key == '3':
            character_assignments['Lady Scarlet'] = character_assignments.pop('3')    
        elif key == '4':
            character_assignments['Dr. Plum'] = character_assignments.pop('4')
        elif key == '5':
            character_assignments['General Mustard'] = character_assignments.pop('5')

    # convert keys in character_assignments to strings 
    for character in used_characters:
        if character == '0':
            used_characters.insert(0,'Baron Green')
            used_characters.remove('0')
        elif character == '1':
            used_characters.insert(0,'Lady Peacock')
            used_characters.remove('1')
        elif character == '2':
            used_characters.insert(0,'Madam White')
            used_characters.remove('2')
        elif character == '3':
            used_characters.insert(0,'Lady Scarlet')
            used_characters.remove('3')
        elif character == '4':
            used_characters.insert(0,'Dr. Plum')
            used_characters.remove('4')
        elif character == '5':
            used_characters.insert(0,'General Mustard')
            used_characters.remove('5')
        else:
            print("character was not replaced. character value = ")
            print(character)

    print("\n\n---------------------------\n\ngame is ready to start\n\n character assignments:\n")
    print(character_assignments)
    print('\n\nused characters:')
    print(used_characters)
    print('\n\nnumber of players: '+str(num_players)+'\n\n')

    
    print("-----------------------------\n\ncreating game!\n\n ------------------\n\n")
    game = Game(num_players, used_characters)
    game.print()

    print("sending clients game started signal")
    broadcast_message("gamestarted",players)

    time.sleep(.5)
    print("sending players the card data...\n")
    # send clients their cards and who got how many cards
    cards_dealt = str(num_players)
    for piece in game.pieces:
        if piece.cards != []:
            cards_dealt = cards_dealt + ',' + str(len(piece.cards))
    for character in character_assignments:
        piece_index = get_piece(game, character)
        piece = game.pieces[piece_index]
        num_cards = str(len(piece.cards))
        deck = ','.join(piece.cards)
        message = '9,'+cards_dealt + ',' + deck
        send_message(message, piece, character_assignments, players)

    print("\n*\n*\n*\n******done initializing game!!!!!!!!!!!*****\n*\n*\n*\n*")
    # can game just be passed like this? would it be better to create it in the main function?
    return game, character_assignments, players

# Function sends message to specified player(piece)
def send_message(message, piece, character_assignments, players):
    # message needs to be a string
    id = character_assignments[piece.character]
    conn = players[id]
    data = message+"\r\n"
    conn.send(data.encode())

# Function sends message to all players(pieces)
def broadcast_message(message, players):
    # message needs to be a string
    data = message+"\r\n"
    for id, conn in players.items():
        conn.send(data.encode())

# Function waits for and retrieves a message from the player associated with piece
def receive_message(piece, character_assignments, players):
    id = character_assignments[piece.character]
    conn = players[id]
    data = conn.recv(1024).decode()
    data = data[:-1] # remove \n character
    if data == '':
        time.sleep(.5)
        data = conn.recv(1024).decode()
    # data should be a string. need to double check
    return data

# Function handles player's turn
def handle_turn(game, piece, character_assignments, players, winner,game_over): 
    
    # request move from player 
    send_message("5,"+str(piece.was_just_moved_by_suggestn)+','+piece.position, piece, character_assignments, players)
    turn = receive_message(piece, character_assignments, players)

    while (turn != "-1") and (game_over == 0): # while move is not over
        print("move received.\n")
        move = turn.split(',')
        if move[0] == '2': # if player moved locations
            piece.position = move[1] # make sure format matches that in components.py
            broadcast_message("2,"+piece.character+","+move[1], players) 
            print("player moved to "+piece.position+'\n')
        elif move[0] == '3': # if move was a suggestion
            suggestion = move[1:]
            print("player made a suggestion: ")
            print(suggestion)
            print('\n')
            handle_suggestion(suggestion, game, piece, character_assignments, players)
        elif move[0] == '4':
            accusation = move[1:] 
            print("player made an accusation: ")
            print(accusation)
            print('\n')           
            game_over=handle_accusation(accusation, game, piece, character_assignments, players, winner, game_over)
            break
        if game_over == 1:
            print('the game ended during their turn so their turn is over\n')
            break;
        turn = receive_message(piece, character_assignments, players)

    piece.was_just_moved_by_suggestn = 0
    return game_over

# Function returns index of piece with specified character
def get_piece(game, character):
    for i in range(6):
        piece = game.pieces[i]
        if piece.character == character:
            return i
    print("ERROR: PIECE NOT FOUND. CHARACTER: "+character)
    return -1

# Function handles suggestions
def handle_suggestion(suggestion, game, piece, character_assignments, players):
    who = suggestion[0]
    room = suggestion[1]
    weapon = suggestion[2]

    # if suggested piece is not already in that room, move them into it
    who_piece = game.pieces[get_piece(game, who)] 
    if who_piece.position != room:
        who_piece.position = room
        who_piece.was_just_moved_by_suggestn = 1
        broadcast_message("22,"+who+","+room, players)
        print("moving suggested piece ("+who+")into the room\n")
    # see who can disprove the suggestion
    was_disproved = 0
    player_who_disproved = ""
    card_used_to_disprove = ""
    player_num = get_piece(game, piece.character)
    # start from player's left
    i = (player_num+1)%6
    pieces = game.pieces
    while i != player_num:
        if who in pieces[i].cards:
            was_disproved = 1
            player_who_disproved = pieces[i].character
            card_used_to_disprove = who
            break
        elif room in pieces[i].cards:
            was_disproved = 1
            player_who_disproved = pieces[i].character
            card_used_to_disprove = room
            break
        elif weapon in pieces[i].cards:
            was_disproved = 1
            player_who_disproved = pieces[i].character
            card_used_to_disprove = weapon
            break
        i = (i+1)%6
    # broadcast the result
    print("the suggestion was disproved by player: " +player_who_disproved+" who used the card: "+card_used_to_disprove+'\n\n')
    send_message("-3,"+str(was_disproved)+","+player_who_disproved+","+card_used_to_disprove, piece, character_assignments, players) 
    broadcast_message("3,"+piece.character+","+who+","+room+","+weapon+','+player_who_disproved, players)

# Function handles accusations
def handle_accusation(accusation, game, piece, character_assignments, players, winner, game_over):
    # if accusation was wrong:
    if set(game.answer) != set(accusation):
        piece.has_guessed = 1
        broadcast_message("4,"+piece.character+",0", players) 
        print("incorrect accusation.\n")
    # if accusation was correct:
    else: 
        game_over = 1 ##see if this actually changes game_over value
        winner = piece.character 
        broadcast_message("4,"+piece.character+",1," + accusation[0]+","+accusation[1]+","+accusation[2], players)
        print('correct accusation!\n')
    return game_over

if __name__ == '__main__':
    #global game_over

    print("\n\n\nintializing game...\n\n\n")
    game, character_assignments, players  = initialize_game()
    game_over = 0
    winner = ""
    print("\nbeginning game loop....\n\n\n")
    time.sleep(5)
    while game_over == 0:
        pieces_without_turns = 0
        for piece in game.pieces: # pieces are already in order of play
            # skip pieces not in play or who have made a wrong accusation
            if game_over == 1:
                break
            if piece.is_in_play==0 or piece.has_guessed==1:
                pieces_without_turns = pieces_without_turns+1
                if pieces_without_turns == 6:
                    print("there are no more players with turns.\n game state:")
                    game.print()
                    game_over = 1
                    break
                continue
            print("\n\n beginning turn for player "+piece.character+"...\n\n")
            game_over=handle_turn(game, piece, character_assignments, players, winner, game_over)
    print("\n\ngame over, closing connections\n\n")
    #close all connections
    for id in players:
        conn = players[id]
        conn.close()
    print("\n\nconnections closed. exiting\n\n")


