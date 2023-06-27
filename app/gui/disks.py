import pygame
import math

from app.utils import Utils

class Disks(pygame.sprite.Sprite):
    def __init__(self, xy, player, size):
        pygame.sprite.Sprite.__init__(self)
        x, y = xy
        self.rect = pygame.Rect(x-size, y-size, size*2, size*2)
        self.image = pygame.Surface((size*2, size*2), pygame.SRCALPHA, 32)
        self.player = player
        self.size = size

        self.tick_max = 40
        self.tick_idx = self.tick_max
        self.tick_step = math.floor(2 * self.size / self.tick_max)

        self.redraw = True
        self.update()

    def flip(self):
        self.redraw = True
        self.tick_idx = 0
        self.prev = self.player
        self.player = ~self.player

    def update(self):
        if self.redraw:
            self.image = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA, 32)

            self.tick_idx += 3
            if self.tick_idx < self.tick_max / 2:
                x = self.size - self.tick_idx * self.tick_step
                pygame.draw.ellipse(
                        self.image, Utils.getPlayerColor(self.prev),
                        (0, self.size-x, self.size*2, x*2))
            elif self.tick_idx < self.tick_max:
                x = self.tick_idx * self.tick_step - self.size
                pygame.draw.ellipse(
                        self.image, Utils.getPlayerColor(self.player),
                        (0, self.size-x, self.size*2, x*2))
            else:
                self.redraw = False
                pygame.draw.circle(self.image, Utils.getPlayerColor(self.player),
                                   (self.size, self.size), self.size, self.size)
