import pygame
import sys
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


# check for a win
def check_win(player):
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

player=1
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

            if available_square(clicked_row, clicked_col):
                mark_square(clicked_row, clicked_col, player)
                if check_win(player): 
                    game_over=True
                
                player = player%2 +1
                draw_symbols()
        
        if event.type==pygame.KEYDOWN:  # if keyboard pressed
            if event.key==pygame.K_r:   # if key 'r' pressed
                restart()
                game_over=False

    pygame.display.update() 
