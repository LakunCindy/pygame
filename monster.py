import pygame
import random
import animation 
class Monster(animation.AnimateSprite):
    def __init__(self,game):
        super().__init__("mummy")
        self.game = game
        self.health = 100
        self.max_health = 100
        self.attack = 0.3
        self.rect = self.image.get_rect()
        self.rect.x = 1000 + random.randint(0,300)
        self.rect.y = 540
        self.velocity = random.randint(1,2)
        self.start_animation()

    def damage(self,amount):
        #infliger les degats
        self.health -= amount
        #vérifier si le nb de points de vie est inférieur ou égal à 0
        if self.health <= 0:
            self.rect.x = 1000 + random.randint(0,300)
            self.velocity = random.randint(1,2)
            self.health = self.max_health

            #si la barre d'event est chargé à son maxi on ne fait pas repop les monstres
            if self.game.comet_event.is_full_loaded():
                #retirer du jeu
                self.game.all_monsters.remove(self)

                #appel de la méthode pour essayer de déclencher la pluie de cometes
                self.game.comet_event.attempt_fall()

    def update_health_bar(self,surface):
        #définir une couleur pour une jauge de vie
        bar_color = (111,210,46)
        #définir une couleur pour l'arriere plan de la jauge (gris foncé)
        back_bar_color = (60, 63, 60)

        #definir la position de notre jauge de vie ainsi que sa largeur et son épaisseur
        bar_position = [self.rect.x + 10, self.rect.y - 20, self.health, 5]

        #definir la position de l'arrière plan de notre jauge de vie 
        back_bar_position = [self.rect.x + 10, self.rect.y - 20, self.max_health, 5]

        # dessiner notre barre de vie
        pygame.draw.rect(surface, back_bar_color, back_bar_position)
        pygame.draw.rect(surface, bar_color, bar_position)

    def update_animation(self):
        self.animate(loop=True)
        
    def forward(self):
        #le deplacement ne se fait que si il ny'a pas de collision avec un groupe de joueur
        if not self.game.check_collision(self, self.game.all_players):
            self.rect.x -= self.velocity
        #si le monstre est en collision avec le joueur
        else:
            #infliger des degats
            self.game.player.damage(self.attack)