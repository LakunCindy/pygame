import json

import pygame

from messagerie import Messagerie
from player import Player
from monster import Monster, BadWorm, Boss
from comet_event import CometFallEvent
from sound import SoundManager

class Game: 
    def __init__(self):
        self.id = None
        #definir si le jeu a commencé
        self.is_host = -1
        self.is_playing = False
        self.is_ready = False
        #générer le joueur
        self.all_players = pygame.sprite.Group()
        self.player = Player(self, 'worms')
        self.player2 = Player(self,'player')
        self.all_players.add(self.player)
        self.all_players.add(self.player2)
        #gérer l'event
        self.comet_event = CometFallEvent(self)
        #groupe de monstre
        self.all_monsters = pygame.sprite.Group()

        self.score = 0
        self.pressed = {}
        self.font = pygame.font.Font("assets/font.ttf", 25)
        self.sound_manager = SoundManager()
        #APPEL MESSAGE
        self.message = Messagerie(self)

    def setId(self, id):
        self.id = id
    def connected(self):
        return self.is_ready

    def start(self):
        self.is_playing = True
        self.spawn_monster(BadWorm)
        self.spawn_monster(BadWorm)
        self.spawn_monster(Boss)

    def game_over(self):
        #remettre le jeu à neuf, retirer les monstres, remettre le joeueur à 100 vie, jeu en attente
        self.all_monsters = pygame.sprite.Group()
        self.comet_event.all_comets = pygame.sprite.Group()
        self.player.health = self.player.max_health
        self.player2.health = self.player2.max_health
        self.player.rect.x = self.player.init_rect_x
        self.player2.rect.x = self.player2.init_rect_x
        self.all_players.add(self.player)
        self.all_players.add(self.player2)
        self.comet_event.reset_percent()
        self.score = 0
        self.sound_manager.play('game_over')

    def add_score(self,points=10):
        self.score += points

    def update(self,screen):
        #afficher le score sur l'ecran
        score_text = self.font.render(f"Score: {self.score}", 1, (0,0,0))
        screen.blit(score_text,(20,20))
        self.message.init_messagerie(screen)

        #appliquer image du joueur
        screen.blit(self.player.image, self.player.rect)
        screen.blit(self.player2.image,self.player2.rect)

        #actualiser la barre de vie du joueur
        self.player.update_health_bar(screen)
        self.player2.update_health_bar(screen)

        #actualiser la barre d'event
        self.comet_event.update_bar(screen)

        #actualiser l'animation du joueur
        self.player.update_animation()
        self.player2.update_animation()

        #recup les projectiles du joueur
        for projectile in self.player.all_projectiles:
            projectile.move()

        for projectile in self.player2.all_projectiles:
            projectile.move()

        #recup les monstres du jeu
        for monster in self.all_monsters:
            monster.forward()
            monster.update_health_bar(screen)
            monster.update_animation()

        #recup les comets
        for comet in self.comet_event.all_comets:
            comet.fall()

        #gestion platform collision
        # hits = pygame.sprite.spritecollide(self.player,self.platforms,False)
        # if hits:
        #     self.player.rect.y = hits[0].rect.top
        #     self.player.velocity = 0

        #appliquer les projectiles
        self.player.all_projectiles.draw(screen)
        self.player2.all_projectiles.draw(screen)

        #appliquer l'ensemble des images de mon groupe de monstre
        self.all_monsters.draw(screen)

        #appliquer l'ensemble des images de mon groupe de comettes
        self.comet_event.all_comets.draw(screen)

        #appliquer l'ensemble des images de mon groupe de platforme
        # self.platforms.draw(screen)

        #verfier si le joueur souhaite aller à gauche ou à droite ou sauter
        if self.pressed.get(pygame.K_RIGHT) and self.player.rect.x + self.player.rect.width < screen.get_width():
            if self.is_host:
                self.player.move_right()
            else:
                self.player2.move_right()
        if self.pressed.get(pygame.K_LEFT) and self.player.rect.x > 0:
            if self.is_host:
                self.player.move_left()
            else:
                self.player2.move_left()
        
        self.player.jump()
        self.player2.jump()

            
    def check_collision(self,sprite,group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)

    def spawn_monster(self,monster_class_name):
        self.all_monsters.add(monster_class_name.__call__(self))

    def toString(self):
        retour = {
            "isGame": True,
            "id": self.id,
            "is_host": self.is_host,
            "is_ready": self.is_ready,
            "score": self.score,
            "player": {
                "health": self.player.health,
                "x": self.player.rect.x,
                "y": self.player.rect.y,
                "projectile": self.player.shoot
            },
            "player2": {
                "health": self.player2.health,
                "x": self.player2.rect.x,
                "y": self.player2.rect.y,
                "projectile": self.player2.shoot
            }
        }
        return json.dumps(retour)

