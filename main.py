# A Simple Tic Tac Toe by KyleGogglezMonroe@yahoo.com
import random

# Our Game Board
TTTBoard = [0] * 9
# Actual Positions are as follows, for efficient checking of win condition and List to track that
# 1 | 2 | 3
# 8 | 0 | 4
# 7 | 6 | 5
PositionNum = [7, 6, 5, 8, 0, 4, 1, 2, 3]
# List tracking what spots are open to play on
PlacesLeft = [0, 1, 2, 3, 4, 5, 6, 7, 8]
# Enum List to mark spot value in visualization
XnOs = [' ', 'X', 'O']
# Randomly choose who plays first and tell Player
PlaysFirst = random.randrange(1, 3)
if PlaysFirst == 1:
    print("Player is X and plays first.")
else:
    print("Player is O and plays second.")
# Track the number of turns taken for optimization of win check and learning AI
NumTurnsTaken = 0


# Reset back to starting over
def reset_board():
    global PlaysFirst, NumTurnsTaken
    TTTBoard[:] = [0] * 9
    PlaysFirst = random.randrange(1, 3)
    if PlaysFirst == 1:
        print("Player is X and plays first.")
    else:
        print("Player is O and plays second.")
    PlacesLeft[:] = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    NumTurnsTaken = 0


# See the current state of the board
def print_board():
    print(" " + XnOs[TTTBoard[1]] + " | " + XnOs[TTTBoard[2]] + " | " + XnOs[TTTBoard[3]])
    print('___|___|___')
    print(" " + XnOs[TTTBoard[8]] + " | " + XnOs[TTTBoard[0]] + " | " + XnOs[TTTBoard[4]])
    print('___|___|___')
    print(" " + XnOs[TTTBoard[7]] + " | " + XnOs[TTTBoard[6]] + " | " + XnOs[TTTBoard[5]])
    print('   |   |   ')


# In case you forget your Numpad, could change this to phone style
def print_positions():
    print("Board positions are as follows:")
    print(' 7 | 8 | 9 ')
    print('___|___|___')
    print(' 4 | 5 | 6 ')
    print('___|___|___')
    print(' 1 | 2 | 3 ')
    print('   |   |   ')


# Function for checking if the current move wins
# Would do this differently for custom board sizes
# Returns 1 if win state
def check_win(who):
    # Check Diagonals and Across Mid
    if TTTBoard[0] == who:
        possible = 1
        while possible <= 4:
            if TTTBoard[possible] == who and TTTBoard[possible + 4] == who:
                return 1
            possible += 1
    # Check Top and Left lines
    if TTTBoard[1] == who:
        if (TTTBoard[2] == who and TTTBoard[3]) == who or (TTTBoard[8] == who and TTTBoard[7] == who):
            return 1
    # Check Right and Bottom lines
    if TTTBoard[5] == who:
        if (TTTBoard[4] == who and TTTBoard[3] == who) or (TTTBoard[6] == who and TTTBoard[7] == who):
            return 1
    return 0


# AI Logic
# Returns actual position of choice
def random_ai_turn():
    pick = PlacesLeft[random.randrange(0, len(PlacesLeft))]
    if 1 == PlaysFirst:
        TTTBoard[pick] = 2
    else:
        TTTBoard[pick] = 1
    PlacesLeft.remove(pick)
    return pick


def learning_ai_turn():
    # TODO: Write Learning AI and choice at start to pick AI
    random_ai_turn()
    # List of 2 Lists for who goes first, then Lists all the way down...
    # List of 3 for 1st pick (Corner, Side, Middle) Attempts and Wins "The AI will remember this..."
    # List of 5 for 2nd pick (3 side, 2 middle) If middle was first only 2 used for Side and Corner
    # List of 7 for additional picks (rotated by 1st and 2nd picks)
    # Lists start with 1 win(so 100% chance to pick) and will first try to go each place additionally once
    # Fuzzy Logic on where to go after all have 1 attempt
    # Print AI state om which Lists are base trained
    # Probably 3 then 7 since it can get multiple from one game, followed by 5
    # Technically this method can let you train it bad habits... but if you abuse them it will break them
    # Could also utilize the turns needed to win to get a further heuristic of optimal plays
    # TODO: Add a save to file and load file logic


def blocker_ai_turn():
    # TODO: Write simple AI that chooses the first blocking move it sees otherwise runs random.
    random_ai_turn()
    # check_win Logic but if it finds 2 true, plays in 3rd spot if open


# Main Starts Here
if __name__ == '__main__':
    print_positions()
    # Main Loop
    while True:
        # Going second is the same as skipping the first player turn.
        if PlaysFirst == 1 or NumTurnsTaken > 0:
            move = input("Choose position of your " + XnOs[PlaysFirst] +
                         " ('r' will reset, 'p' for positions reminder, 'q' to quit): ")
            # Non-numerical options
            if move == 'p':
                print_positions()
                continue
            elif move == 'r':
                print("Resetting...")
                reset_board()
                print_board()
                continue
            elif move == 'q':
                break
            # Check valid input
            elif not move.strip().isdigit() or move == "0":
                print('This is not a valid input')
                continue
            # Check valid spot
            elif PositionNum[int(move) - 1] not in PlacesLeft:
                print('This is not a valid move.')
                continue
            # All Good, do the rest of the round logic
            else:
                NumTurnsTaken += 1
                # Mark the board with the player's symbol
                TTTBoard[PositionNum[int(move) - 1]] = PlaysFirst
                # Make sure no one takes that spot again
                PlacesLeft.remove(PositionNum[int(move) - 1])
                # Let us see it
                print_board()
                # Check if player won
                # Can't win without 3 symbols
                if NumTurnsTaken >= 5:
                    if check_win(PlaysFirst):
                        print('Player won!  Board is reset.')
                        reset_board()
                        continue
                    # Make sure we aren't out of moves
                    elif len(PlacesLeft) == 0:
                        print('Draw Game... too bad.  Board is reset.')
                        reset_board()
                        continue
        # If the game isn't over, let the AI take a turn
        NumTurnsTaken += 1
        # Logic in the Print Statement... but we have no further use for it.
        print('AI chose ' + str(PositionNum.index(random_ai_turn()) + 1))
        print_board()
        # Check if AI won
        # Can't win without 3 symbols
        if NumTurnsTaken >= 3:
            # If player is X, AI must be O
            if PlaysFirst == 1:
                if check_win(2):
                    print('AI won!  Board is reset.')
                    reset_board()
                    continue
            else:
                if check_win(1):
                    print('AI won!  Board is reset.')
                    reset_board()
                    continue
            # Make sure we aren't out of moves
            if 0 == len(PlacesLeft):
                print('Draw Game... too bad.  Board is reset.')
                reset_board()
