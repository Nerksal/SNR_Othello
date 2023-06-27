import pygame
import math
import os

from app.utils import Utils

class TextBox(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        pygame.sprite.Sprite.__init__(self)
        self.x, self.y = pos
        self.w, self.h = size
        
        self.h_space = 5
        self.v_space = 14
 
        self.font = pygame.font.Font(Utils.getFontPath(), 16)
        w, h = self.font.size(" 1: b2")
        self.col_w = w + self.v_space
        self.col_h = h 

        self.bg = pygame.Surface((self.w, self.h))
        self.color = (210, 180, 140)
        self.bg.fill(self.color)
        
        caption = self.font.render("Game Moves History", True, (0, 0, 0))
        x = self.w / 2 - caption.get_width() / 2
        self.bg.blit(caption, (x, 2))
        
        self.caption_box = pygame.Rect((0, 0, self.w, caption.get_height() + 4))
        pygame.draw.rect(self.bg, (0,0,0), self.caption_box, 1)
        
        self.scroll_box = pygame.Rect((
                    2 * (self.col_w + self.v_space),  
                    self.caption_box.h + self.h_space,
                    20,
                    self.h - self.caption_box.h - 2 * self.h_space
        ))
        pygame.draw.rect(self.bg, (0,0,0), self.scroll_box)

        self.scroll_box_in = pygame.Rect((
                    self.scroll_box.x + 1,
                    self.scroll_box.y + 1,
                    self.scroll_box.w - 2,
                    self.scroll_box.h - 2
        ))

        self.moves = []
        self.max_lines = math.floor( (self.h - self.caption_box.h - self.h_space) / self.col_h )
        self.top_lines = 0

        self.image = pygame.Surface((self.w, self.h))
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

        self.hited = False
        self.redraw = True
        
        self.isActive = False

    def update(self):
        if self.redraw:
            self.image.blit(self.bg, (0, 0))

            pygame.draw.rect(self.image, (211, 123, 12), self.scroll_box_in)

            start = self.top_lines*2 + self.top_lines%1
            idx = 0
            for player, move in self.moves[start:]:
                text = self.font.render(str( idx+start + 1).rjust(2)+ ": " + move,
                        True, Utils.getPlayerColor(player)
                )
                xi = ( math.floor(idx / 2) * self.col_h) + self.caption_box.h + self.h_space
                yi = self.v_space + (idx%2 * (self.col_w + self.v_space))
                self.image.blit(text, (yi, xi))
                idx += 1

            self.redraw = False

    def setActive(self, isActive):
        self.isActive = isActive

    def handle(self, event):
        if self.isActive == False:
            return

        if event.type == pygame.MOUSEBUTTONUP:
            self.hited = False
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if self.scroll_box.collidepoint((x - self.x, y - self.y)):
                self.hited = True

        if self.hited == True and event.type == pygame.MOUSEMOTION:
            _, dy = pygame.mouse.get_rel()
            self.scroll_box_in.y += dy
            print(self.scroll_box_in.y, " ", self.scroll_box.y)
            if self.scroll_box_in.y < self.scroll_box.y + 1:
                self.scroll_box_in.y = self.scroll_box.y + 1
            elif self.scroll_box_in.y + self.scroll_box_in.h >= self.scroll_box.h + self.scroll_box.y:
                self.scroll_box_in.y = self.scroll_box.y + self.scroll_box.h - self.scroll_box_in.h - 1
            
            self.top_lines = math.floor((self.scroll_box_in.y -  self.scroll_box.y) / (self.scroll_box.h / len(self.moves)))
            self.top_lines = math.floor(self.top_lines / 2)

            self.redraw = True

    def clean(self):
        self.moves.clear()
        self.top_lines = 0
        self.scroll_box_in = pygame.Rect((
                    self.scroll_box.x + 1,
                    self.scroll_box.y + 1,
                    self.scroll_box.w - 2,
                    self.scroll_box.h - 2
        ))

    def addMove(self, player, txt):
        self.moves.append((player, txt))

        lines = math.ceil( len(self.moves) / 2 )
        if lines > self.max_lines:
            self.top_lines = lines - self.max_lines  
 
            x, y, w, h = self.scroll_box
            h = math.floor(h * self.max_lines / (self.max_lines + self.top_lines)) - 2
            y = y + self.scroll_box.h - h - 1

            self.scroll_box_in.h = h
            self.scroll_box_in.y = y

        self.redraw = True
