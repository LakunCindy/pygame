import pygame
from sprite import Projectile

#creer une premier class qui represente le premier joueur
class Player(pygame.sprite.Sprite):
      def __init__(self):
         super().__init__()
         self.health = 100
         self.max_health = 100
         self.attack = 10
         self.velocity = 5
         self.image = pygame.image.load('assets/player.png')
         self.rect = self.image.get_rect()
         self.rect.x = 400
         self.rect.y = 500
         self.all_projectiles = pygame.sprite.Group()

      def launch_projectile(self):
         #creer une nouvelle instance de la classe projectile
         self.all_projectiles.add(Projectile(self))

      def move_right(self):
         self.rect.x += self.velocity

      def move_left(self):
         self.rect.x -= self.velocity