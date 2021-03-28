import os
import threading
import socket
import time
import re
import math
from game import Game
import json

import pygame

pygame.init()

#définir une clock
clock = pygame.time.Clock()
FPS = 60

#générer la fenetre du jeu
pygame.display.set_caption("World War Worms")
width = 1080
height = 720
screen = pygame.display.set_mode((width, height))

#Charger l'arrière plan
background = pygame.image.load('assets/background.jpg')

#importer charger notre bannière
banner = pygame.image.load('assets/banner.png')
banner = pygame.transform.scale(banner,(400,400))
banner_rect = banner.get_rect()
banner_rect.x = math.ceil(screen.get_width() / 3.33)

#importer les inputs
#PSEUDO INPUT
pseudo_placeholder = 'Pseudo'
pseudo_text = ''
pseudo_input_rect = pygame.Rect(screen.get_width()/2.5,350,200,32)
pseudo_active = False

#SERVEUR INPUT
server_placeholder = 'Serveur'
server_text = 'localhost'
server_input_rect = pygame.Rect(screen.get_width()/2.5,420,200,32)
server_active = False

#PORT INPUT
port_placeholder = 'Port'
port_text = '59001'
port_input_rect = pygame.Rect(screen.get_width()/2.5,500,200,32)
port_active = False

base_font = pygame.font.Font("assets/font.ttf",20)
color_active = pygame.Color('orange')
color_passive = pygame.Color('gray15')
color = color_passive



#importer charger notre bouton pour lancer la partie
play_button = pygame.image.load('assets/button.png')
play_button = pygame.transform.scale(play_button, (400,150))
play_button_rect = play_button.get_rect()
play_button_rect.x = math.ceil(screen.get_width() / 3.33)
play_button_rect.y = math.ceil(screen.get_height() / 1.3)

class Client:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serv = os.environ["CONNECTIONIP"]
        port = 5555
        self.socket.connect((serv, port))
        self.listening = True
        self.game = Game()

    def listener(self):
        while self.listening:
            data = ""
            try:
                data = self.socket.recv(1024).decode('UTF-8')
            except socket.error:
                print("Unable to receive data")
            # return du message
            self.handle_msg(data)
            time.sleep(0.1)

    def listen(self):
        self.listen_thread = threading.Thread(target=self.listener)
        self.listen_thread.daemon = True
        self.listen_thread.start()

    def send(self, message):
        try:
            self.socket.sendall(message.encode("UTF-8"))
        except socket.error:
            print("unable to send message")

    def tidy_up(self):
        self.listening = False
        self.socket.close()

    def handle_msg(self, data):
        print("ALED ", data)
        jsonInstance = None
        if data is None or data == '':
            pass
        if data != "":
            jsonInstance = json.loads(data)
        if jsonInstance is not None:
            self.game.setId(jsonInstance.get("id"))
            self.game.is_ready = jsonInstance.get("is_ready")
            self.game.score = jsonInstance.get("score")
            play1 = jsonInstance.get("player")
            self.game.player.rect.x = play1.get("x")
            self.game.player.rect.y = play1.get("y")
            if play1.get("projectile"):
                print("PROJECTILE 1")
                self.game.player.launch_projectile()
                self.game.player.shoot = False
            play2 = jsonInstance.get("player2")
            self.game.player2.rect.x = play2.get("x")
            self.game.player2.rect.y = play2.get("y")
            if play2.get("projectile"):
                print("PROJECTILE 2")
                self.game.player2.launch_projectile()
                self.game.player2.shoot = False







        # if not self.game.is_ready:
        # print("DONE AVEC LA GAME")
        # self.tidy_up()
        # else:
        # print("HANDLE MSG ", data)

    def redrawWindow(self):
        screen.fill((128, 128, 128))
        if not (self.game.connected()):
            font = pygame.font.SysFont("comicsans", 80)
            text = font.render("Waiting for Player...", 1, (255, 0, 0), True)
            screen.blit(background, (0, 0))
            screen.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
            pygame.display.flip()
            self.game.is_host = 0
        elif self.game.is_playing:
            # change if
            screen.blit(background, (0, 0))
            self.game.update(screen)
        else:
            client.game.start()
            client.game.sound_manager.play('click')


def main(client):
    running = True

    client.redrawWindow()

    while running:
        # tant que le jeu est actif

        # arrière plan
        if client.game.is_ready:

            client.redrawWindow()

            # mettre à jour l'ecran
            pygame.display.flip()

            # si le joueur ferme la fenetre
            for event in pygame.event.get():
                client.send(client.game.toString())

                # si l'event est fermeture de fenetre
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    # détecter si un joueur lache une touche du clavier
                elif event.type == pygame.KEYDOWN:
                    client.game.pressed[event.key] = True

                    if event.key == pygame.K_UP:
                        if client.game.is_playing:
                            if client.game.is_host:
                                client.game.player.isJump = True
                            else:
                                client.game.player2.isJump = True

                    if event.key == pygame.K_SPACE:
                        if client.game.is_playing:
                            if client.game.is_host:
                                client.game.player.launch_projectile()
                                client.game.player.shoot = True
                            else :
                                client.game.player2.launch_projectile()
                                client.game.player2.shoot = True




                elif event.type == pygame.KEYUP:  # si la touche n'est plus utilisé
                    client.game.pressed[event.key] = False



            # fixer le nombre de fps
            clock.tick(FPS)


def menu_screen(client):
    run = True
    while run:
        clock.tick(60)
        screen.blit(background, (0, 0))
        screen.blit(play_button, play_button_rect)
        screen.blit(banner, banner_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
    main(client)


if __name__ == "__main__":
    client = Client()
    client.listen()
    menu_screen(client)
