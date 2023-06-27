import pygame
import os

from app.logic.player import Player

class Utils():
    font = None
    dir_path = os.path.abspath(os.path.dirname(__file__))
 
    color_p1 = (  0,   0,   0)
    color_p2 = (255, 255, 255)

    @classmethod
    def getPlayerColor(self, player):
        if player == Player.BLACK:
            return self.color_p1
        else:
            return self.color_p2

    @classmethod
    def getFontPath(self):
        if self.font == None:
            self.font = self.dir_path + "/courier-prime.regular.ttf"

        return self.font
