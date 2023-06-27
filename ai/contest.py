import numpy as np
import multiprocessing as mp

import sys
sys.path.append('../source/')

from board import Board
from player import Player

from ai import AIPlayer, AI_Type

def debug_print(step, black, white, posible):
    print("step: " + str(step))
    for x in range(0, 8):
        for y in range(0, 8):
            if white[x][y]:
                print('W', end='')
            elif black[x][y]:
                print('B', end='')
            elif posible[x, y]:
                print('#', end='')
            else:
                print(' ', end='')
    
        print('')
    print('')


 
if __name__ == '__main__':
    print("Start")
    minmax = AIPlayer(AI_Type.minmax_algorithm, search_deep=6)
    print("Start")
    network = AIPlayer(AI_Type.conv_network)
    print("Start")



    plansza = Board()
    turn = Player.BLACK
    plansza.setTurn(turn)

    last_player_stuck = False
    in_progress = True
 
    print("Start")

    

    while(in_progress == True):
        if plansza.checkPosibleMoves() == True:
            last_player_stuck = False
            
            if turn == Player.WHITE:
                xy = minmax.getMove(plansza)
            else:
                xy = network.getMove(plansza)

            x, y = xy
        
            to_flip = plansza.makeMove(x, y)
        
        else:
            print("STUCK!")
            in_progres = not last_player_stuck
            last_player_stuck = True
        
        b, w = plansza.result()
        if (b + w) >= 64:
            in_progress = False
        
        if in_progress == True:
            turn = ~turn
            plansza.setTurn(turn)

    print(plansza.result())

    print("END")



