import pygame
import numpy as np

from app.gui.disks import Disks
from app.utils import Utils
from app.logic.board import Board
from app.logic.player import Player

BLACK = (0, 0, 0)
WOOD = (202, 164, 114)
WHITE = (255, 255, 255)
GREEN = (105, 139, 105, 255) 
BLUE = (0, 0, 255, 255) 
COVER = (255, 139, 105, 0) 

class BoardGUI(Board, pygame.sprite.Sprite):
    def __init__(self, pos = (0, 0), blockSize = 60):
        Board.__init__(self)
        pygame.sprite.Sprite.__init__(self)

        self.board = np.zeros((8, 8), dtype=pygame.Rect)
        self.frame = np.zeros((2, 8), dtype=pygame.Rect)
        self.blockSize = blockSize  
        self.x, self.y = pos
        self.size = blockSize*8 + blockSize/2

        # frame
        for i in range(8):
            # x-labels
            self.frame[0,i] = pygame.Rect(
                    self.blockSize/2 + i*self.blockSize, 0, self.blockSize, self.blockSize/2)
            # y-labels
            self.frame[1,i] = pygame.Rect(
                    0, self.blockSize/2 + i*self.blockSize, self.blockSize/2, self.blockSize)
    
        for x in range(8):
            for y in range(8):
                self.board[x][y] = pygame.Rect(
                        self.blockSize/2 + x*self.blockSize, 
                        self.blockSize/2 + y*self.blockSize,
                        self.blockSize, self.blockSize)

        self.bg = pygame.Surface((self.size, self.size), pygame.SRCALPHA, 32)
        for x in range(8):
            for y in range(8):
                pygame.draw.rect(self.bg, GREEN,
                                     self.board[x][y], self.blockSize)
                pygame.draw.rect(self.bg, BLACK, self.board[x][y], 1)
 
        font = pygame.font.Font(Utils.getFontPath(), 26)
        
        for i in range(8):
                pygame.draw.rect(self.bg, (202, 164, 114),
                     self.frame[0,i], self.blockSize)
                pygame.draw.rect(self.bg, (0, 0, 0),
                     self.frame[0,i], width=1)
                text = font.render(chr(ord('a')+i), True, (0, 0, 0))
                w, h = text.get_size() 
                x, y = self.frame[0,i].center
                x = x - w/2
                y = y - h/2
                self.bg.blit(text, (x, y))

                pygame.draw.rect(self.bg, WOOD,
                     self.frame[1,i], self.blockSize)
                pygame.draw.rect(self.bg, (0, 0, 0),
                     self.frame[1,i], width=1)
                text = font.render(chr(ord('1')+i), False, (0, 0, 0))
                w, h = text.get_size() 
                x, y = self.frame[1,i].center
                x = x - w/2
                y = y - h/2
                self.bg.blit(text, (x, y))

        self.sprites_list = pygame.sprite.Group()
        self.disks = np.zeros((8, 8), dtype=Disks)

        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA, 32)
        self.image.blit(self.bg, (0,0))
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

        self.xy = None
        self.isActive = False

    def clean(self):
        Board.clean(self)
        self.disks.fill(None)
        self.sprites_list.empty()

        self.disks[3][3] = Disks(self.getCoordinate(3,3), Player.WHITE, 20)
        self.sprites_list.add(self.disks[3][3])
        
        self.disks[4][4] = Disks(self.getCoordinate(4,4), Player.WHITE, 20)
        self.sprites_list.add(self.disks[4][4])
        
        self.disks[3][4] = Disks(self.getCoordinate(3,4), Player.BLACK, 20)
        self.sprites_list.add(self.disks[3][4])
        
        self.disks[4][3] = Disks(self.getCoordinate(4,3), Player.BLACK, 20)
        self.sprites_list.add(self.disks[4][3])

    def getCoordinate(self, x, y):
        xi, yi = self.board[x][y].center
        return (xi, yi)

    def getHumanMove(self):
        while self.isActive == True:
            if self.xy is None:
                continue
            
            if self.isGoodMove(self.xy):
               self.isActive = False
               ret = self.xy
               self.xy == None
               return ret
            
            pygame.time.wait(200)
 
    def __putDisk(self, x, y, turn):
        to_flip = Board.makeMove(self, x, y)
        
        self.disks[x][y] = Disks(self.getCoordinate(x, y), turn, 20)
        self.sprites_list.add(self.disks[x][y])
        
        return to_flip
 
    def makeMove(self, x, y):
        self.last = (x, y)
          
        to_flip = self.__putDisk(x, y, self.turn)

        for xi, yi in to_flip:
            self.disks[xi][yi].flip()
        
        return to_flip
 
    def handle(self, event):
        if self.isActive == False:
            return False

        if event.type == pygame.MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
            
            if self.rect.collidepoint((x, y)):
                x -= self.x
                y -= self.y
                
                for xi in range(8):
                    for yi in range(8):
                        if self.board[xi][yi].collidepoint((x, y)):
                           self.xy = xi, yi
                    
        return True

    def setActive(self, isActive):
        self.isActive = isActive

    def stop(self):
        self.isActive = False
    
    def update(self):
        self.image.blit(self.bg, (0,0))
        for xi, yi in np.transpose(np.nonzero(self.highlighted)):
            if self.turn == Player.BLACK:
                color = (128, 128, 9)
            else:
                color = (189,183,107)
            
            pygame.draw.rect(self.image, color,
                                     self.board[xi][yi], self.blockSize)
            pygame.draw.rect(self.image, BLACK, self.board[xi][yi], 1)

        if hasattr(self, 'last'):
            xi, yi = self.last
            pygame.draw.rect(self.image, (128, 128, 129),
                                     self.board[xi][yi], self.blockSize)
            pygame.draw.rect(self.image, BLACK, self.board[xi][yi], 1)

        self.sprites_list.update()
        self.sprites_list.draw(self.image)
