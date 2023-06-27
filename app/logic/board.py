import numpy as np
import copy 

from app.logic.player import Player

def disksToFlip(x, y, player, opponent):
    to_flip = np.zeros((8, 8), dtype=bool)
    tmp = np.zeros((8, 8), dtype=bool)

    directions = [
        (lambda i: (    x, y-i-1), range(0, y)), # up
        (lambda i: (x+i+1, y-i-1), range(0, 7-x if 7-x < y else y)), # up - right
        (lambda i: (x+i+1,     y), range(0, 7-x)), # right
        (lambda i: (x+i+1, y+i+1), range(0, 7-x if x > y else 7-y)), # down - right
        (lambda i: (    x, y+i+1), range(0, 7-y)), # down
        (lambda i: (x-i-1, y+i+1), range(0, x if x < 7-y else 7-y)), # down - left
        (lambda i: (x-i-1,     y), range(0, x)), # left
        (lambda i: (x-i-1, y-i-1), range(0, x if x < y else y)) # up - left
    ]

    for f, r in directions:
        tmp.fill(False)
        for i in r:
            xi, yi = f(i)
            if opponent[xi][yi]:
                tmp[xi][yi] = True
            else:
                if player[xi][yi]:
                    to_flip = np.logical_or(to_flip, tmp)
                break

    return np.transpose(np.nonzero(to_flip))

def getPosibleMoves(player, opponent):
    current_board = np.logical_or(player, opponent)

    highlighted = np.zeros((8, 8), dtype=bool)

    for xi in range(8):
        for yi in range(8):
            if current_board[xi, yi] == False:
                count = disksToFlip(xi, yi, player, opponent).size
                if count >= 1:
                    highlighted[xi, yi] = True

    return highlighted

def putDisks(x, y, player, opponent):
    to_flip = disksToFlip(x, y, player, opponent)

    player[x][y] = True

    for xi, yi in to_flip:
        opponent[xi][yi] = False
        player[xi][yi] = True

    return to_flip

def debug_print(black, white, posible = np.zeros((8,8))):
    for x in range(0, 8):
        print('|', end='')
        for y in range(0, 8):
            if white[x][y]:
                print('W', end='')
            elif black[x][y]:
                print('B', end='')
            elif posible[x, y]:
                print('#', end='')
            else:
                print(' ', end='')
    
        print('|')
    print('')

class Board:
    def __init__(self):
        self.white_disks = np.zeros((8, 8), dtype=bool)
        self.black_disks = np.zeros((8, 8), dtype=bool)
        self.highlighted = np.zeros((8, 8), dtype=bool)
        
        self.white_disks[3, 3] = True
        self.white_disks[4, 4] = True

        self.black_disks[4, 3] = True
        self.black_disks[3, 4] = True

        self.isNotificationOn = True
        self.callbacks = []

    def clean(self):
        self.white_disks.fill(False)
        self.black_disks.fill(False)
        self.highlighted.fill(False)
        
        self.white_disks[3, 3] = True
        self.white_disks[4, 4] = True

        self.black_disks[4, 3] = True
        self.black_disks[3, 4] = True

        self.isNotificationOn = True
     
    def checkPosibleMoves(self):
        self.highlighted[:] = getPosibleMoves(self.player, self.opponent)
        return self.highlighted.any()

    def isGoodMove(self, xy):
        legal_moves = np.transpose(np.nonzero(self.highlighted))

        for move in legal_moves:
            if (move == xy).all():
                return True

        return False
    
    def getDisksToFlip(self, x, y):
        return disksToFlip(x, y, self.player, self.opponent)

    def makeMove(self, x, y):
        to_flip = putDisks(x, y, self.player, self.opponent)
        self.__notify()
        return to_flip

    def setTurn(self, turn):
        self.player = self.black_disks if turn is Player.BLACK else self.white_disks 
        self.opponent = self.white_disks if turn is Player.BLACK else self.black_disks 
        self.turn = turn
        self.__notify()
    
    def getTurn(self):
        return self.turn

    def getBoards(self):
         return np.dstack((self.player, self.opponent))

    def getBlack(self):
        return self.black_disks

    def getWhite(self):
        return self.white_disks

    def getPosibleMoves(self):
        return np.matrix(self.highlighted)

    def getCheckpoint(self):
        copy_b = copy.deepcopy(self.black_disks)
        copy_w = copy.deepcopy(self.white_disks)
        copy_h = copy.deepcopy(self.highlighted)

        return (self.turn, copy_b, copy_w, copy_h)

    def restore(self, checkpoint):
        self.black_disks = copy.deepcopy(checkpoint[1])
        self.white_disks = copy.deepcopy(checkpoint[2])
        self.highlighted = copy.deepcopy(checkpoint[3])
        
        self.setTurn(checkpoint[0])

    def __notify(self):
        if self.isNotificationOn == False:
            return

        black = np.sum(self.black_disks)
        white = np.sum(self.white_disks)

        for callback in self.callbacks:
            callback(self.turn, black, white)

    def addNotifyCallback(self, callback):
        self.callbacks.append(callback)

    def turnOnNotification(self):
        self.isNotificationOn = True

    def turnOffNotification(self):
        self.isNotificationOn = False

    def result(self):
        return (np.sum(self.black_disks), np.sum(self.white_disks))
    
