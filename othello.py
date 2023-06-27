import pygame
import threading
import numpy as np

from app.gui.board_gui import BoardGUI
from app.gui.disks import Disks
from app.gui.menu import Menu, PopUp, Button
from app.gui.textBox import TextBox
from app.gui.turnBox import TurnBox
from app.logic.ai import AIPlayer, AI_Type
from app.logic.player import Player, PlayerType
from app.utils import Utils

background_colour = (128, 128, 128)
(width, height) = (5+510+5+200+5, 520)

class Game:
    def __init__(self):
        self.sprites_list = pygame.sprite.Group()
        self.callbacs = []

        self.gui_board = BoardGUI(pos = (5,5))
        self.sprites_list.add(self.gui_board)
        self.callbacs.append(self.gui_board)
 
        self.ai_network = AIPlayer(AI_Type.conv_network)
        
        self.gui_move_list = TextBox(pos = (520, 150), size = (200, 510-145))
        self.sprites_list.add(self.gui_move_list)
        
        self.callbacs.append(self.gui_move_list)
 
        self.gui_turn_box = TurnBox((520, 5), (200, 140))
        self.gui_turn_box.set(Player.BLACK, 2, 2)
        self.gui_board.addNotifyCallback(self.gui_turn_box.set)
 
        self.sprites_list.add(self.gui_turn_box)

        self.menu = Menu((width/2, height/2), "Othello", exit_func=self.exit_othello)
        self.callbacs.append(self.menu)
        self.sprites_list.add(self.menu)
        
        stuck_rect = pygame.Rect(width/2 - 130, height/2 - 80, 300, 160) 
        self.stuck = PopUp(stuck_rect, "Stuck")
        self.stuck.addOkButton()
        self.stuck.setActive(False)
        self.callbacs.append(self.stuck)
        self.sprites_list.add(self.stuck)

        self.is_running = True
        
        self.event = threading.Event()

        self.display_thread = threading.Thread(target = self.__display, args=(self.event, self.sprites_list))
        self.display_thread.daemon = True
        self.display_thread.start()

        self.event_thread = threading.Thread(target = self.__handle_events, args=(self.event, self.callbacs))
        self.event_thread.daemon = True
        self.event_thread.start()

    def __display(self, event, sprites_list):
        screen = pygame.display.set_mode((width, height))
    
        while not event.is_set():
            sprites_list.update()
            sprites_list.draw(screen)
            pygame.display.flip()
            pygame.time.delay(100)
            screen.fill(background_colour)

    def __handle_events(self, event, callbacs):
        while not event.is_set():
            e = pygame.event.wait()
            if e.type == pygame.QUIT:
                self.exit_othello()

            for c in callbacs:
                if c.handle(e) == True:
                    continue

    def exit_othello(self):
        self.is_running = False
        self.event.set()

        for sprite in self.sprites_list:
            if hasattr(sprite, 'stop'):
                sprite.stop()

        #self.display_thread.join()  
        #self.event_thread.join()
        print("Bye Bye!")

    def main_loop(self):
        while not self.event.is_set():
            self.menu.setActive(True)
            self.menu.wait()
            
            if self.event.is_set():
                break
            
            self.p_black, self.p_white = self.menu.get_game_settings()

            self.__game_loop()
            self.gui_move_list.setActive(False)

            b, w = self.gui_board.result()
            if b > w:
                self.menu.addText("Black wins")
            elif w > b:
                self.menu.addText("White wins")
            else:
                self.menu.addText("Draw")

    def __game_loop(self):
        self.gui_board.clean()
        self.gui_move_list.clean()

        self.turn = Player.BLACK
        self.gui_turn_box.set(self.turn, 2, 2)
        self.gui_board.setTurn(self.turn)
        self.gui_move_list.setActive(True)
    
        last_player_stuck = False
        in_progress = True
        while in_progress == True:
            if self.gui_board.checkPosibleMoves() == True:
                last_player_stuck = False
                
                if self.turn == Player.WHITE and self.p_white == PlayerType.human:
                    self.gui_board.setActive(True)
                    xy = self.gui_board.getHumanMove()
                    self.gui_board.setActive(False)
                elif self.turn == Player.BLACK and self.p_black == PlayerType.human:
                    self.gui_board.setActive(True)
                    xy = self.gui_board.getHumanMove()
                    self.gui_board.setActive(False)
                else:
                    xy = self.ai_network.getMove(self.gui_board)
                    pygame.time.wait(1024)
                
                if xy is None:
                    in_progress = False
                    continue

                x, y = xy
                
                self.gui_move_list.addMove(self.turn, chr(x + ord('1')) + chr(y + ord('a')))
                _ = self.gui_board.makeMove(x, y)
           
            else:
                in_progress = not last_player_stuck
                last_player_stuck = True

                if in_progress == True:
                    self.stuck.setActive(True)
                    self.stuck.wait()

            b, w = self.gui_board.result()
            if (b + w) >= 64:
                in_progress = False
            
            if in_progress == True:
                self.turn = ~self.turn
                self.gui_board.setTurn(self.turn)

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Othello')
    
    othello = Game()
    othello.main_loop()

    pygame.quit()
