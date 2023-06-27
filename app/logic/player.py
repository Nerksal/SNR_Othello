from enum import Flag, auto

class Player(Flag):
    BLACK = auto()
    WHITE = auto()

class PlayerType(Flag):
    conv_network = auto()
    minmax_algorithm = auto()
    human = auto()


