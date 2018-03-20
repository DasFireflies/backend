from components import Game, Piece

#handlers?

# Function sends updates to all players
def update_players():
    #send update to all players so that 
    #their board updates and
    #their activity log updates

# Function handles player's turn
def startNextTurn(game, piece): 
    #request move from player 
    #waits for update                               
    #updates game state/players
    #broadcast update to everyone

# Function ends the game
def end_game(winner):
    #how do we want to end the game?
    #send everyone updates?  

if __name__ == '__main__':
    #set up waiting room
    #wait for players to start game
    #initialize game
    game_over = 0
    while game_over == 0:
        for piece in game.pieces: # pieces are already in order of play
            # skip pieces not in play or who have made a wrong accusation
            if piece.is_in_play==0 or piece.has_guessed==1:
                continue
            start_next_turn(game, piece)
    end_game(player)
