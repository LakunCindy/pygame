import pygame
from projectile import Projectile
import animation

#creer une premier class qui represente le premier joueur
class Player(animation.AnimateSprite):
      def __init__(self,game,name):
         super().__init__(name)
         self.game = game
         self.health = 100
         self.max_health = 100
         self.attack = 100
         self.velocity = 5
         self.rect = self.image.get_rect()
         self.init_rect_x = 400
         self.rect.x = 400
         self.rect.y = 470
         self.all_projectiles = pygame.sprite.Group()
         self.shoot = False
         #CODE JUMP
         self.velocity_jump = 10    
         self.isJump = False
         self.canShoot = True
         # self.jumpCount = 8

      def damage(self,amount):
         if self.health - amount > amount:
            self.health -= amount
         else:
            #si le joueur n'a plus de point de vie
            if self.game.player2.health > 0 :
               self.rect.x = 2000
               self.health = -1
               self.game.all_players.remove(self)
               if len(self.game.all_players) == 0:
                  self.game.game_over()

            if self.game.player.health > 0 :
               self.rect.x = 2000
               self.health = -1
               self.game.all_players.remove(self)
               if len(self.game.all_players) == 0:
                  self.game.game_over()

   

      def update_animation(self):
         self.animate()

      def update_health_bar(self,surface):
        #définir une couleur pour une jauge de vie
        bar_color = (111,210,46)
        #définir une couleur pour l'arriere plan de la jauge (gris foncé)
        back_bar_color = (60, 63, 60)

        #definir la position de notre jauge de vie ainsi que sa largeur et son épaisseur
        bar_position = [self.rect.x + 50, self.rect.y + 20, self.health, 7]

        #definir la position de l'arrière plan de notre jauge de vie 
        back_bar_position = [self.rect.x + 50, self.rect.y + 20, self.max_health, 7]

        # dessiner notre barre de vie
        pygame.draw.rect(surface, back_bar_color, back_bar_position)
        pygame.draw.rect(surface, bar_color, bar_position)

      def launch_projectile(self):
         #creer une nouvelle instance de la classe projectile
         self.all_projectiles.add(Projectile(self))
         self.canShoot = False
         self.game.sound_manager.play('tir')

      def move_right(self):
         #demarrer l'animation 
         self.start_animation()
         # si le joueur n'est pas en collision avec un monstre
         if not self.game.check_collision(self, self.game.all_monsters):
            self.rect.x += self.velocity
         #if self.game.check_collision(self,self.game.all_monsters) and self.game.player.rect.y == self.game.all_monsters

      def move_left(self):
         #demarrer l'animation 
         self.start_animation()
         self.rect.x -= self.velocity

      #CODE JUMP
      def jump(self):
         keys = pygame.key.get_pressed()
         if self.isJump is True:
            self.rect.y -= self.velocity_jump * 3
            self.velocity_jump -= 1
            if self.velocity_jump < -10:
               self.isJump = False
               self.velocity_jump = 10 

         # if not (self.isJump):
         #    if keys[pygame.KEYDOWN] and self.rect.y >= 470 - self.velocity_jump:
         #          self.rect.y -= self.velocity_jump

         #    if keys[pygame.KEYDOWN] and self.rect.y <= 570 - self.velocity_jump:
         #          self.rect.y += self.velocity_jump

         #    if keys[pygame.K_UP]:
         #          self.isJump = True
         # else:
         #    if self.jumpCount >= -8:
         #          self.rect.y -= (self.jumpCount * abs(self.jumpCount)) * 0.5
         #          self.jumpCount -= 1
         #    else:
         #          self.jumpCount = 8
         #          self.isJump = False



             