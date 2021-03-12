import pygame
from player import Player
class Game: 
    def __init__(self):
        #générer le joueur
        self.player = Player()
        self.pressed = {} #touche active