import pygame

from app.utils import Utils
from app.logic.player import PlayerType

class Button(pygame.sprite.Sprite):
    def __init__(self, rect, label):
        pygame.sprite.Sprite.__init__(self)
 
        _, _, self.w, self.h = rect
        self.image = pygame.Surface((self.w, self.h))
        self.rect = rect

        pygame.draw.rect(self.image, (0, 0, 0), (0, 0, self.w, self.h), width=1)
        pygame.draw.rect(self.image, (123, 151, 0), (1, 1, self.w, self.h))

        font = pygame.font.Font(Utils.getFontPath(), 16)
        self.label = font.render(label, True, (0, 0, 0))
        x = self.image.get_width() / 2 - self.label.get_width() / 2
        y = self.image.get_height() / 2 - self.label.get_height() / 2
        self.label_pos = (x, y)
        self.image.blit(self.label, self.label_pos)

    def addCallback(self, func):
        self.on_click = func
    
    def click(self):
        if hasattr(self, 'on_click'):
            self.on_click()

    def highlight(self, isH):
        if isH:
            pygame.draw.rect(self.image, (0, 0, 0), (0, 0, self.w, self.h), width=1)
            pygame.draw.rect(self.image, (0, 151, 0), (0, 0,  self.w - 1, self.h - 1))
            self.image.blit(self.label, self.label_pos)
        else:
            pygame.draw.rect(self.image, (0, 0, 0), (0, 0, self.w, self.h), width=1)
            pygame.draw.rect(self.image, (123, 151, 0), (1, 1, self.w, self.h))
            self.image.blit(self.label, self.label_pos)


class RoundButton(pygame.sprite.Sprite):
    def __init__(self, rect, color):
        pygame.sprite.Sprite.__init__(self)
 
        _, _, self.w, self.h = rect
        self.image = pygame.Surface((self.w, self.h), pygame.SRCALPHA, 32)
        self.image.fill((0, 0, 0, 0))
        
        self.rect = rect
        self.color = color

        pygame.draw.ellipse(self.image, color, (0,0, self.w, self.h))

    def addCallback(self, func):
        self.on_click = func
    
    def click(self):
        if hasattr(self, 'on_click'):
            self.on_click()

    def highlight(self, isH):
        if isH:
            self.image.fill((0, 0, 0, 0))
            pygame.draw.ellipse(self.image, self.color, (4, 4, self.w-8, self.h-8))
        else:
            pygame.draw.ellipse(self.image, self.color, (0, 0, self.w, self.h))


class PopUp(pygame.sprite.Sprite):
    def __init__(self, rect, caption):
        pygame.sprite.Sprite.__init__(self)

        _, _, w, h = rect

        self.image = pygame.Surface((w, h), pygame.SRCALPHA, 32)

        self.rect = rect

        self.bg = pygame.Surface(self.image.get_size())
        self.bg.fill((122,122,122))
        pygame.draw.rect(self.bg, (0, 0, 0),
                         (0, 0, 
                          self.image.get_width(),
                          self.image.get_height(), 
                          ),  border_radius=0, width=1)

        pygame.draw.rect(self.bg, (0,0,0),
                         (7, 7, 
                          self.image.get_width()-14,
                          self.image.get_height()-14, 
                          ),  border_radius=0, width=1)
 
        pygame.draw.rect(self.bg, (123, 151, 0),
                         (1, 1, 
                          self.image.get_width() - 2,
                          self.image.get_height() - 2, 
                          ),  border_radius=0, width=6)

        font = pygame.font.Font(Utils.getFontPath(), 56)
        text = font.render(caption, True, (0, 0, 0))
        x = self.image.get_width() / 2 - text.get_width() / 2
        self.bg.blit(text, (x, 20))

        self.btn_list = pygame.sprite.Group()
        self.setActive(True)

    def addText(self, text):
        font = pygame.font.Font(Utils.getFontPath(), 26)
        text = font.render(text, True, (0, 0, 0))
        x = self.image.get_width() / 2 - text.get_width() / 2
        mask = pygame.Surface((self.bg.get_width()-40, text.get_height())) 
        mask.fill((122,122,122))
        self.bg.blit(mask, (20, 80))
        self.bg.blit(text, (x, 80))

    def addBtn(self, btn):
        self.btn_list.add(btn)

    def ok_callback(self):
        self.setActive(False)

    def addOkButton(self):
        x = self.rect.w - 140 - 20
        y = self.rect.h - 40 - 20

        btn_ok = Button(pygame.Rect(x, y, 140, 40), "ok")
        btn_ok.addCallback(self.ok_callback)
        self.btn_list.add(btn_ok)

    def wait(self):
        while self.isActive == True:
            pygame.time.wait(2)

    def setActive(self, isActive):
        self.isActive = isActive
        if self.isActive == False:
            self.stop()

    def handle(self, event):
        if self.isActive == True:
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                
                if self.rect.collidepoint((x, y)):
                    x -= self.rect.x
                    y -= self.rect.y
            
                    mouse_pos = (x, y)
                
                    for btn in self.btn_list:
                        if btn.rect.collidepoint(mouse_pos):
                            btn.click()

            return True

    def stop(self):
        self.image.fill((0, 0, 0, 0))
        self.isActive = False

    def update(self):
        if self.isActive == False:
            return

        self.image.blit(self.bg, (0, 0))
        
        if self.btn_list:
            x, y = pygame.mouse.get_pos()
            if self.rect.collidepoint((x, y)):
                x -= self.rect.x
                y -= self.rect.y
        
                mouse_pos = (x, y)
            
                for btn in self.btn_list:
                    if btn.rect.collidepoint(mouse_pos):
                        btn.highlight(True)
                    else:
                        btn.highlight(False)

            self.btn_list.update()
            self.btn_list.draw(self.image)

class Menu(PopUp):
    def __init__(self, screen_center, caption, exit_func):
        self.x, self.y = screen_center
        self.x -= 500 / 2
        self.y -= 300 / 2

        rect = pygame.Rect(
                self.x, self.y,
                500, 300
        )

        PopUp.__init__(self, rect, caption)

        self.exit_func = exit_func
 
        bx = 50
 
        btn_hot_seat = Button(pygame.Rect(bx, 120, 140, 40), "Hot Seat")
        btn_hot_seat.addCallback(self.hot_seat)
        self.btn_list.add(btn_hot_seat)
        
        btn_ai = Button(pygame.Rect(bx, 170, 140, 40), "AI")
        btn_ai.addCallback(self.ai)
        self.btn_list.add(btn_ai)
 
        btn_exit = Button(pygame.Rect(bx, 220, 140, 40), "Exit")
        btn_exit.addCallback(self.exit_func)
        self.btn_list.add(btn_exit)

        self.black = RoundButton(pygame.Rect(250, 150, 60, 60), (0, 0, 0))
        self.black.addCallback(self.play_black)

        self.white = RoundButton(pygame.Rect(350, 150, 60, 60), (255, 255, 255))
        self.white.addCallback(self.play_white)
        
        font = pygame.font.Font(Utils.getFontPath(), 26)
        self.text = font.render("Choose your color", True, (0, 0, 0))

        self.ai_submenu = False
 
    def hot_seat(self):
        self.p_black = PlayerType.human
        self.p_white = PlayerType.human

        self.setActive(False)

    def play_black(self):
        self.p_black = PlayerType.human
        self.p_white = PlayerType.conv_network

        self.setActive(False)

    def play_white(self):
        self.p_black = PlayerType.conv_network
        self.p_white = PlayerType.human

        self.setActive(False)

    def ai(self):
        self.ai_submenu = True
       
        self.btn_list.add(self.black)
        self.btn_list.add(self.white)

    def get_game_settings(self):
        return (self.p_black, self.p_white)

    def wait(self):
        PopUp.wait(self)

        self.ai_submenu = False
        self.btn_list.remove(self.white)
        self.btn_list.remove(self.black)

    def update(self):
        PopUp.update(self)

        if self.ai_submenu == True:
            self.image.blit(self.text, (200, 120))
