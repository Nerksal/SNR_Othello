import pygame

from app.logic.player import Player

GREEN = (105, 139, 105, 255) 
RED = (235, 139, 105, 255) 
BLACK = (0, 0, 0, 255) 

class TurnBox(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        pygame.sprite.Sprite.__init__(self)
        self.x, self.y = pos
        self.w, self.h = size

        self.redraw = True
        self.font = pygame.font.Font(pygame.font.get_default_font(), 26)

        self.turn = Player.BLACK

        self.bg_color = GREEN
        self.image = pygame.Surface((self.w, self.h))
        self.image.fill(self.bg_color)
        
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def update(self):
        if self.redraw == False:
            return 

        self.image.fill(self.bg_color)
        pygame.draw.rect(self.image, (0,0,0), (0,0, self.w-1, self.h-1), 1)

        if self.turn == Player.BLACK:
            pygame.draw.circle(self.image, BLACK, (50, 50), 36)
            pygame.draw.circle(self.image, RED, (50, 50), 35)
            pygame.draw.circle(self.image, BLACK, (50, 50), 31)
        else:
            pygame.draw.circle(self.image, BLACK, (150, 50), 36)
            pygame.draw.circle(self.image, RED, (150, 50), 35)
            pygame.draw.circle(self.image, BLACK, (150, 50), 31)

        color = (0, 0, 0)
        x = self.w / 4 
        pygame.draw.circle(self.image, color, (x, 50), 30)
        text = self.font.render(str(self.black), True, (0, 0, 0))
        w, _ = text.get_size() 
        x = x - w/2
        self.image.blit(text, (x, 100))

        color = (255, 255, 255)
        x = self.w / 4  + self.w / 2
        pygame.draw.circle(self.image, color, (x, 50), 30)
        text = self.font.render(str(self.white), True, (0, 0, 0))
        w, _ = text.get_size() 
        x = x - w/2
        self.image.blit(text, (x, 100))
        
        self.redraw = False

    def set(self, turn, black, white):
        self.black = black
        self.white = white
        self.turn = turn
        self.redraw = True
