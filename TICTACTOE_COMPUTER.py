import pygame
import sys
import copy
import numpy as np

# initialize all the modules so we can use
pygame.init()

# WIDTH=HEIGHT AND CELL IS 1/3 OF THAT , YOU CAN CHANGE WIDTH AS YOU WANT
WIDTH=600
HEIGHT=WIDTH
CELL_SIZE=WIDTH/3
LINE_WIDTH=10
BOARD_SIZE=3
CIRCLE_RADIUS= WIDTH/10
CIRCLE_WIDTH=17

# STD COLORS
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
ORANGE=(255, 165, 0) 
YELLOW=(255, 255, 0)
MAGENTA=(255, 0, 255)
PURPLE=(128, 0, 128)
MUTE_GREEN=(150, 200, 150)
DEEP_BURGUNDY=(128, 0, 32)
GREY=(66,66,66)
LIGHT_GREY=(240,240,240)
BLACK=(0,0,0)
WHITE=(255,255,255)


LINE_COLOR=(40,150,150)
BGCOLOR=(0, 191, 255) # light blue (173, 216, 230)


# set window height and width  color
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("TIC TAC TOE")
screen.fill(BGCOLOR)


# create a grid of 3 by 3
board = np.zeros((BOARD_SIZE,BOARD_SIZE))

def next_turn(current_player):
    if current_player== 1:
        return 2

    return 1


# calculates the total possible number of wins out of all possible combinations of moves for player from this grid position
def calc_num_of_wins_possible(grid, current_player, arr, computer_player):   # we use a list so we  can pass by reference
    # player is the one we calculate wins for
    if check_win(grid) == computer_player:
        arr[0] += 1
        return arr
    if check_win(grid) == next_turn(computer_player):
        arr[0] -= 1
        return arr
    if check_win(grid) == "DRAW":
        return arr

    for i in range(0, 3):
        for j in range(0, 3):
            if grid[i][j] == 0:
                grid[i][j] = current_player
                calc_num_of_wins_possible(grid, next_turn(current_player), arr, computer_player)
                grid[i][j] = 0

    return arr


# checks if player has a win in immediate next move and blocks it
def next_move_opponent_win(grid, opponent_player):    
    for row in range(0, 3):
        for col in range(0, 3):
            
            if grid[row][col] == 0:   # if tile empty
                grid[row][col] = opponent_player # fill player in the tile
                
                if check_win(grid) == opponent_player: 
                    grid[row][col] = 0    # make tile empty again
                    return (row, col)# if the player has a win then return this position
                
                grid[row][col] = 0    # make tile empty again

    return None # if no immediate win for opponent return NULL

                                        
def best_move_grid(grid, computer_player):

    max_win = 0
    max_win_grid = []

    for i in range(0, 3):
        for j in range(0, 3):

            human_player = next_turn(computer_player)
            row_col = next_move_opponent_win(grid, human_player)   # check if opponent has a win next move
            
            if row_col:
                row = row_col[0]
                col = row_col[1]
                
                grid[row][col] = computer_player    # if opponent has a win next move,just block that move and return 
                return grid

            # check all possibilties to find max wins and min losses
            if grid[i][j] == 0:
                grid[i][j] = computer_player
                
                arr = [0]
                wins_possible_with_this_grid = calc_num_of_wins_possible(grid, next_turn(computer_player), arr, computer_player)
                if wins_possible_with_this_grid[0] > max_win:
                    max_win = wins_possible_with_this_grid[0]
                    max_win_grid = copy.deepcopy(grid)

                grid[i][j] = 0


    if max_win > 0: return max_win_grid # check if there is even a possibility of win in position


    # if reached here means all combinations lead to draw so just fill the first blank you see 
    for row in range(0, 3):
        for col in range(0, 3):
            if grid[row][col] == 0:
                grid[row][col] = computer_player
                return grid
    
    return grid


# draw the lines in grid
def draw_lines():
    # draw line from (x,y) to (x',y')
    pygame.draw.line(screen, LINE_COLOR, (CELL_SIZE,0), (CELL_SIZE,HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2*CELL_SIZE,0), (2*CELL_SIZE,HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0,CELL_SIZE), (WIDTH,CELL_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0,2*CELL_SIZE), (WIDTH,2*CELL_SIZE), LINE_WIDTH)
 

# marks the tile with the players symbol
def mark_square(row, col, player):
    board[row][col] = player


# check if the square is empty/available return true/false
def available_square(row, col):
    return board[row][col] == 0
    

# check if board is completely filled
def is_board_full():
    if any(0 in row for row in board):
        return False
    
    return True


# checks for a win IN GRID
def check_win(grid):
    for i in range(0,3):
        if grid[i][0] == grid[i][1] == grid[i][2] != " " : # if 3 in  a column then win
            return grid[i][0]
    for j in range(0,3):
        if grid[0][j] == grid[1][j] == grid[2][j] != " " : # if 3 in  a row then win
            return grid[0][j]
    
    if grid[0][0]==grid[1][1] and grid[1][1]==grid[2][2] and grid[1][1] != " ":   # if 3 in  a diag then win
        return grid[0][0]
    
    if grid[0][2]==grid[1][1] and grid[1][1]==grid[2][0]  and grid[1][1] != " ":   # if 3 in  a diag then win
        return grid[0][2]

    else:
        if not any(" " in row for row in grid):
            return "DRAW"   #if NOTA then drawn game
        

        

# check for a win
def check_win_draw_line(board):
    for row in range(0,3):
        if board[row][0]==board[row][1]==board[row][2]==player:
            draw_horizontal_line(row,player)
            return True
    
    for col in range(0,3):
        if board[0][col]==board[1][col]==board[2][col]==player:
            draw_vertical_line(col,player)
            return True
        
    if board[0][0]==board[1][1]==board[2][2]==player:
        draw_primary_diagonal_line(player)
        return True
    
    if board[2][0]==board[1][1]==board[0][2]==player:
        draw_secondary_diagonal_line(player)
        return True

    return False



def draw_vertical_line(column, player):
    if player==1:
        color=LIGHT_GREY
    else:
        color=GREY

    pygame.draw.line(screen, color, (CELL_SIZE * (column+1) - CELL_SIZE/2 , CELL_SIZE/8), ( CELL_SIZE * (column+1) - CELL_SIZE/2, WIDTH-CELL_SIZE/8), LINE_WIDTH)

def draw_horizontal_line(row, player):
    if player==1:
        color=LIGHT_GREY
    else:
        color=GREY

    pygame.draw.line(screen, color, (CELL_SIZE/8 , CELL_SIZE * (row+1) - CELL_SIZE/2), (WIDTH-CELL_SIZE/8,  CELL_SIZE * (row+1) - CELL_SIZE/2), LINE_WIDTH)

def draw_primary_diagonal_line(player):
    if player==1:
        color=LIGHT_GREY
    else:
        color=GREY

    pygame.draw.line(screen, color, (CELL_SIZE/8, CELL_SIZE/8), (WIDTH-CELL_SIZE/8, HEIGHT-CELL_SIZE/8), LINE_WIDTH)

def draw_secondary_diagonal_line(player):
    if player==1:
        color=LIGHT_GREY
    else:
        color=GREY

    pygame.draw.line(screen, color, (CELL_SIZE/8, HEIGHT-CELL_SIZE/8), (WIDTH-CELL_SIZE/8, CELL_SIZE/8), LINE_WIDTH)

def restart():
    screen.fill(BGCOLOR)    # recreate the board from scratch
    draw_lines()
    player=1    

    for i in range(0,3):
        for j in range(0,3):
            board[i][j]=0

    game_over=False


# draw the corresponding symbols
def draw_symbols():
    for row in range(0,3):
        for col in range(0,3):
            if board[row][col] == 1:
                x = int(col*CELL_SIZE + CELL_SIZE/2)
                y = int(row*CELL_SIZE + CELL_SIZE/2)
                
                pygame.draw.circle(screen, LIGHT_GREY, (x,y), CIRCLE_RADIUS, CIRCLE_WIDTH)

            elif board[row][col] == 2:
                # draw two intersecting lines
                x = int(col*CELL_SIZE + CELL_SIZE/4)
                x_= int((col+1)*CELL_SIZE - CELL_SIZE/4)

                y = int(row*CELL_SIZE + CELL_SIZE/4)
                y_= int((row+1)*CELL_SIZE - CELL_SIZE/4)

                pygame.draw.line(screen, GREY, (x,y), (x_,y_), LINE_WIDTH+15)
                pygame.draw.line(screen, GREY, (x_,y), (x,y_), LINE_WIDTH+15)
                
               

                
# call the draw lines function
draw_lines()

human_player = 1
computer_player = 2
player = 1    # human is 1 computer is 2
game_over= False


# mainloop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type==pygame.MOUSEBUTTONDOWN and not game_over: 
            mouse_x = event.pos[0]
            mouse_y = event.pos[1]
            
            clicked_row = int(mouse_y//CELL_SIZE) # get floor of y/cell_size
            clicked_col = int(mouse_x//CELL_SIZE) # get floor of x/cell_size

            if player == human_player and available_square(clicked_row, clicked_col):

                mark_square(clicked_row, clicked_col, player)
                if check_win_draw_line(board): 
                    game_over=True
                
                player = next_turn(player)
                draw_symbols()
        
                board = best_move_grid(board, computer_player)
                if check_win_draw_line(board): 
                    game_over=True
                print(board)
                draw_symbols()
                player = next_turn(player)

        
        if event.type==pygame.KEYDOWN:  # if keyboard pressed
            if event.key==pygame.K_r:   # if key 'r' pressed
                restart()
                game_over=False

    pygame.display.update() 
