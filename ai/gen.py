import numpy as np
import multiprocessing as mp

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

# tup[0] -> boards np.array(8, 8, 2)
# tup[1] -> moves set of tuple {(x, y)}
# tup[2] -> posible moves np.array(8,8)
def cleans(tuples):
    boards = []
    labels = []
    while (len(tuples) > 0):
        elem = tuples.pop()
        for i in range(len(tuples)-1, -1, -1):
            tup = tuples[i]
            eq1 = np.array_equal(tup[0][:,:,0], elem[0][:,:,0])
            eq2 = np.array_equal(tup[0][:,:,1], elem[0][:,:,1]                    
            
            if eq1 == True and eq2 == True:
                tmp = elem[1]
                tmp.add(tup[1].pop())
                del tuples[i]
        
        matrix = elem[2].astype(float)
        for i in elem[1]:
           matrix[i[0], i[1]] = 4
        num = np.sum(matrix)
        vect = np.reshape(matrix, 64).astype(float)
        vect /= num

        boards.append(elem[0])
        labels.append(vect)
    
    return boards, labels


def main():
    #  1: black
    #  0: draw
    # -1: white
 
    dataset_csv = open('./dataset/othello_dataset.csv', 'r')
    header = dataset_csv.readline()

    cnt = 0
    es = 0

    print("Start reading kaggle dataset")
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
                move = set([(x,y)])
                
                idx = np.sum(boards[:,:,0])
                
                lista[idx].append((boards, move, posible))

            plansza.makeMove(x, y)
        
            turn = ~turn
        '''
        if es > 20:
            break

        es += 1
        '''
    print("")
    dataset_csv.close
    print("Reading kaggle dataset done")

    print("Start cleaning dataset...")
    boards   = []
    labels   = []

    pool = mp.Pool()

    for ret in pool.map(cleans, lista):
        b, l = ret
        boards += b
        labels += l
        print(".", end='')
    print("")
    pool.close()
    print("Cleaning done!")

    print("Creating numpy array from list")
    boards = np.array(boards)
    labels = np.array(labels)
    
    # (n, 1, 64) -> (n, 64)
    labels = np.reshape(labels, (labels.shape[0], 64))

    print(labels.shape)
    print(boards.shape)
    print("Creating done")

    print("Start permute the dataset")
    idx = np.random.permutation(labels.shape[0])
    boards  = boards[idx]
    labels  = labels[idx]
    print("Permute done")

    print("Start splitting dataset")
    split = int(labels.shape[0] * 0.8)

    x_train = boards[:split]
    y_train = labels[:split]

    x_test = boards[split:]
    y_test = labels[split:]
    print("Spliting done")
    
    if save == True:
        np.savez('./dataset.npz', x_train=x_train, y_train=y_train, x_test=x_test, y_test=y_test)
       
if __name__ == '__main__':
    save = True
    main()

