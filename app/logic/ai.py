import numpy as np
import sys

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from tensorflow import keras
from enum import Flag, auto

from app.logic.board import *
from app.logic.player import Player

class AI_Type(Flag):
    conv_network = auto()
    minmax_algorithm = auto()
    human = auto()

class AIPlayer:
    def __init__(self, ai_type=AI_Type.conv_network, path='', search_deep=5):
        if isinstance(ai_type, AI_Type):
            self.ai_type = ai_type
        else:
            raise Exception("Please pass a proper ai type")
        
        if self.ai_type == AI_Type.conv_network:
            dir_path = os.path.abspath(os.path.dirname(__file__))
            self.model = keras.models.load_model(dir_path + '/model.h5')
        else:
            self.deep = search_deep

    def __minimax_value(self, player, opponent, turn, search_depth):
        if search_depth == 0:
            p = np.sum(player)
            o = np.sum(opponent)

            return p - o
        
        if turn == True:
            legal_moves = getPosibleMoves(player, opponent)
        else:
            legal_moves = getPosibleMoves(opponent, player)
    
        legal_moves = np.transpose(np.nonzero(legal_moves))
       
        if legal_moves.shape[0] == 0:
            value = self.__minimax_value(player, opponent, not turn, search_depth - 1)                

        if turn == True:
            value = float("-inf")
            
            for x, y in legal_moves:
                player_copy = np.copy(player)
                opponent_copy = np.copy(opponent)
                putDisks(x, y, player_copy, opponent_copy)
                score = self.__minimax_value(player_copy, opponent_copy, False, search_depth - 1)
                value = max(value, score)
        
        else:
            value = float("inf")
            
            for x, y in legal_moves:
                player_copy = np.copy(player)
                opponent_copy = np.copy(opponent)
                putDisks(x, y, opponent_copy, player_copy)
                score = self.__minimax_value(player_copy, opponent_copy, True, search_depth - 1)
                value = max(value, score)

        return value


    def getMove(self, board):
        best_move = None
        boards = board.getBoards()
        
        player = boards[:,:,0]
        opponent = boards[:,:,1]
        posible = getPosibleMoves(player, opponent)
        legal_moves = np.transpose(np.nonzero(posible))
      
        if self.ai_type == AI_Type.conv_network:
            boards = np.reshape(boards, (1, 8, 8, 2))
            predict = self.model.predict(boards, verbose=0)
            predict = np.reshape(predict, (8,8))
            
            ind = np.flip(
                    np.transpose(
                        np.unravel_index(
                            np.argsort(predict, axis=None), predict.shape
                        )
                    ), axis=0
            )

            for idx, value in enumerate(ind):
                if (legal_moves == value).all(1).any():
                    best_move = value
                    if idx != 0:
                        print("The prediction is not perfect. Posible move on ", idx+1, " position.")
                        debug_print(player, opponent, posible)
                        print(np.round(predict, decimals = 2))

                    break

        elif self.ai_type == AI_Type.minmax_algorithm:
            best_val = float("-inf")

            #ToDo: add threads for every move

            for x, y in legal_moves:
                player_copy = np.copy(player)
                opponent_copy = np.copy(opponent)
                
                putDisks(x, y, player_copy, opponent_copy)
                move_val = self.__minimax_value(player_copy, opponent_copy, False, self.deep)
        
                if move_val > best_val:
                    best_move = (x, y)
                    best_val = move_val
        
        return best_move
