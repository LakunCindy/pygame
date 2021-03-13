import pygame
from player import Player
from monster import Monster
class Game: 
    def __init__(self):
        #definir si le jeu a commencé
        self.is_playing = False
        #générer le joueur
        self.all_players = pygame.sprite.Group()
        self.player = Player(self)
        self.all_players.add(self.player)
        #groupe de monstre
        self.all_monsters = pygame.sprite.Group()
        self.pressed = {}
        self.spawn_monster()
        self.spawn_monster()

    def start(self):
        self.is_playing = True
        self.spawn_monster()
        self.spawn_monster()

    def game_over(self):
        #remettre le jeu à neuf, retirer les monstres, remettre le joeueur à 100 vie, jeu en attente
        self.all_monsters = pygame.sprite.Group()
        self.player.health = self.player.max_health
        self.is_playing = False

    def update(self,screen):
        #appliquer image du joueur
        screen.blit(self.player.image,self.player.rect)

        #actualiser la barre de vie du joueur
        self.player.update_health_bar(screen)

        #recup les projectiles du joueur
        for projectile in self.player.all_projectiles:
            projectile.move()

        #recup les monstres du jeu
        for monster in self.all_monsters:
            monster.forward()
            monster.update_health_bar(screen)

        #appliquer les projectiles
        self.player.all_projectiles.draw(screen)

        #appliquer l'ensemble des images de mon groupe de monstre
        self.all_monsters.draw(screen)

        #verfier si le joueur souhaite aller à gauche ou à droite
        if self.pressed.get(pygame.K_RIGHT) and self.player.rect.x + self.player.rect.width < screen.get_width():
            self.player.move_right()
        if self.pressed.get(pygame.K_LEFT) and self.player.rect.x > 0:
            self.player.move_left()
    
    def check_collision(self,sprite,group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)

    def spawn_monster(self):
        monster = Monster(self)
        self.all_monsters.add(monster)