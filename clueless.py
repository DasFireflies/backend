import socket
import sys
import time
from components import Game, Piece

# Function handles game initialization
# Accepts character selections and creates the playing pieces and game object
def initialize_game():

    #****right now this only handles single player****
    #****need to implement threading to handle multiple players****

    used_characters = []
    players_whove_selected = []
    character_assignments = {} #dict of (character, player id) pairs
    players = {} #dict of (player id, socket object) pairs
    num_players = 0
    game_started = 0
    # Set up connection
    host = "172.31.27.46"
    port = 5000
    mySocket = socket.socket()
    mySocket.bind((host,port))
    mySocket.listen(1)
    conn, addr = mySocket.accept()
    id = addr[1]
    print ("Connection from: " + str(addr)+ ". User's id will be " + str(id))
    players[id] = conn
    # Process input from player until someone presses "Start Game"
    while game_started == 0:
        data = conn.recv(1024).decode()
        print ("data received: " + str(data) + " from player with id " + str(id))
        # data should either be an integer 0-5 indicating character selection/deselection or -1 indicating "start game"
        if data == '':
            continue

        elif data == '-1': # If player pressed "Start Game"
            game_started = 1

        # If player has already chosen their character, unassign it
        elif id in players_whove_selected:
            used_characters.remove(data)
            players_whove_selected.remove(id)
            character_assignments.pop(data)
            num_players = num_players-1
            print("Sending confirmation of deselection  back to player")
            data = "1\r\n"
            conn.send(data.encode())
        # If player hasnt chosen character yet and character is unused,
        # assign them that character
        elif data not in used_characters:
            print("Assigning them that character...\n")
            used_characters.append(data)
            players_whove_selected.append(id)
            print("character marked as used.\n")
            character_assignments[data] = id
            print("player and character are paired\n")
            num_players = num_players+1
            print("player count increased\n")
            print("Sending 1 back to player")
            data = "1\r\n"
            conn.send(data.encode())
            print("data sent")
        # If character is used, don't assign it
        elif data in used_characters:
            print("Sending 0 back to player because character has been taken")
            data = "0\r\n"
            conn.send(data.encode())

        time.sleep(.5)

    game = Game(num_players, used_characters)

    # convert keys in character_assignments to strings 
    for key in character_assignments:
        if key == 0:
            character_assignments['mr_green'] = character_assignments.pop(0)
        elif key == 1:
            character_assignments['mrs_peacock'] = character_assignments.pop(1)
        elif key == 2:
            character_assignments['mrs_white'] = character_assignments.pop(2)
        elif key == 3:
            character_assignments['miss_scarlet'] = character_assignments.pop(3)    
        elif key == 4:
            character_assignments['professor_plum'] = character_assignments.pop(4)
        elif key == 5:
            character_assignments['colonel_mustard'] = character_assignments.pop(5)

    # can game just be passed like this? would it be better to create it in the main function?
    return game, character_assignments, players


# Function sends message to specified player(piece)
def send_message(message, piece, character_assignments, players):
    # message needs to be a string
    id = character_assignments[piece.character]
    conn = players[id]
    data = message+"\r\n"
    conn.send(data.encode())

# Function waits for and retrieves a message from the player associated with piece
def receive_message(piece, character_assignments, players):
    id = character_assignments[piece.character]
    conn = players[id]
    data = conn.recv(1024).decode()
    if data == '':
        time.sleep(.5)
        data = conn.recv(1024).decode()
    # data should be a string. need to double check
    return data

# Function handles player's turn
def handle_turn(game, piece, character_assignments, players, game_over, winner): 
    # request move from player 
    # can use function send_message

    turn = receive_message(piece, character_assignments, players)

    # parse turn

    if piece moved spaces:
        piece.position = new location in string format. make sure format matches a location in components.py 
        send update to all players

    if move was a suggestion:
        handle_suggestion(suggestion, game, piece, character_assignments, players)

    elif move was an accusation:
        handle_accusation(accusation, game, piece, character_assignments, players, game_over, winner)

    piece.was_just_moved_by_suggestn = 0


# Function handles suggestions
def handle_suggestion(suggestion, game, piece, character_assignments, players):
    who = suggestion[0]
    room = suggestion[1]
    weapon = suggestion[2]

    if character who was suggested is not already in the room:
        update their location to that room
        change that pieces was_just_moved_by_suggestn attribute to equal 1
        send update to all players that that character was moved by a suggestion
    was_disproved = 0
    player_who_disproved = -1
    card_used_to_disprove = ""
    loop through players, starting at whoevers turn should be next and going in order of turns
        if that player can disprove the suggestion, change values of above 3 variables and break
    if was_disproved == 0:
        send everyone updates of who made the suggestion, what the suggestion was, and that it couldnt be disproved
    else:
        tell player who disproved their suggestion and with what card. tell everyone else who made the suggestion, what it was, and who disproved it

# Function handles accusations
def handle_accusation(accusation, game, piece, character_assignments, players, game_over, winner)
    # if accusation was wrong:
    if set(game.answer) != set(accusation):
        piece.has_guessed = 1
        send updates to everyone that this player made an incorrect accusation

    # if accusation was correct:
    else: 
        game_over == 1
        winner = piece.character 

# Function ends the game
def end_game(winner, game, character_assignments, players):
    tell all players who won the game and what the correct accusation was
    end game (what should players see on their screens?)



if __name__ == '__main__':
    game, character_assignments, players  = initialize_game()
    game_over = 0
    winner = ""
    while game_over == 0:
        for piece in game.pieces: # pieces are already in order of play
            # skip pieces not in play or who have made a wrong accusation
            if piece.is_in_play==0 or piece.has_guessed==1:
                continue
            handle_turn(game, piece, character_assignments, players, game_over, winner)
    end_game(winner, game, character_assignments, players)
    #close all connections
    for id in players:
        conn = players[id]
        conn.close()


