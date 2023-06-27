import numpy as np

import sys
sys.path.append('../source/')

from board import Board
from player import Player

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


def main():
    #  1: black
    #  0: draw
    # -1: white
 
    dataset_csv = open('./dataset/othello_dataset.csv', 'r')
    header = dataset_csv.readline()

    player_list = []
    opponent_list = []
    move_x_list = []
    move_y_list = []

    move_list = []
    boards = []
    labels = []
    posibles = []

    cnt = 0

    es = 0

    lista = [[] for i in range(64)]

    while True:
        game = dataset_csv.readline().strip()
    
        if not game:
            break

        (idx, won, moves) = game.split(',')

        won = int(won)
        if won == 1:
            print("b", end='')
            blackWins = True
        elif won == -1:
            print("w", end='')
            blackWins = False
        else:
            print("_", end='')
            continue
        
        if cnt % 64 == 0:
            print("")

        cnt = cnt + 1

        continue

        plansza = Board()

        turn = Player.FIRST
        for i in range(0, len(moves), 2):
            (x, y) = moves[i:i+2]
            x = ord(x)-ord('a')
            y = ord(y)-ord('1')
  
            plansza.setTurn(turn)
            if plansza.checkPosibleMoves() == False:
                turn = ~turn
                plansza.setTurn(turn)
                if plansza.checkPosibleMoves() == False:
                    break

            # Save the move
            if (blackWins == True and turn == Player.FIRST) or (blackWins == False and turn == Player.SECOND):
                boards = plansza.getBoards()
                posible = plansza.getPosibleMoves()

                idx = np.sum(boards[:,:,0])
                
                added = False
                if len(lista[idx]) > 0:
                    for tup in lista[idx]:
                        eq1 = np.array_equal(tup[0][:,:,0], boards[:,:,0])
                        eq2 = np.array_equal(tup[0][:,:,1], boards[:,:,1])
                        eq3 = np.array_equal(tup[2], posible)
                        
                        if eq1 == True and eq2 == True and eq3 == True:
                            added = True
                            m = tup[1]
                            m.add((x,y))
                            break

                if added == False:
                    m = (x,y)
                    move = set([m])
                    lista[idx].append((boards, move, posible))

            plansza.makeMove(x, y)
        
            turn = ~turn
        
        '''
        if es > 20:
            break

        es += 1
        '''
   

    dataset_csv.close

    '''
    boards   = []
    labels   = []

    # tup[0] -> boards np.array(8, 8, 2)
    # tup[1] -> moves set of tuple {(x, y)}
    # tup[2] -> posible moves np.array(8,8)

    for l in lista:
        for tup in l:
            matrix = tup[2].astype(float)
            for i in tup[1]:
                matrix[i[0], i[1]] = 4
            num = np.sum(matrix)
            b = np.reshape(matrix, 64).astype(float)
            b /= num

            boards.append(tup[0])
            labels.append(b)

    boards = np.array(boards)
    labels = np.array(labels)

    idx = np.random.permutation(labels.shape[0])
    boards  = boards[idx]
    labels  = labels[idx]

    # (n, 1, 64) -> (n, 64)
    labels = np.reshape(labels, (labels.shape[0], 64))

    split = int(labels.shape[0] * 0.8)

    print(labels.shape)
    print(boards.shape)

    x_train = boards[:split]
    y_train = labels[:split]

    x_test = boards[split:]
    y_test = labels[split:]

    np.savez('./dataset.npz', x_train, y_train, x_test, y_test)
    '''
   
    if save == True:
        boards   = np.array(boards)
        moves    = np.array(move_list)
        labels   = np.array(labels)
        posibles = np.array(posibles)
    
        # add removes duplicates

        np.savez('./outfile.npz', examples=boards, labels=labels, moves=moves, posibles=posibles)

        idx = np.random.permutation(labels.shape[0])
        boards  = boards[idx]
        labels  = labels[idx]

        np.savez('./permuted.npz', examples=boards, labels=labels)


if __name__ == '__main__':
    save = False
    main()

