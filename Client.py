import os
import threading
import socket
import time
import re
import math
from json import JSONDecodeError

from game import Game
import json

import pygame

pygame.init()

# définir une clock
clock = pygame.time.Clock()
FPS = 60

# générer la fenetre du jeu
pygame.display.set_caption("World War Worms")
width = 1080
height = 720
screen = pygame.display.set_mode((width, height))

# Charger l'arrière plan
background = pygame.image.load('assets/background.jpg')

# importer charger notre bannière
banner = pygame.image.load('assets/banner.png')
banner = pygame.transform.scale(banner, (400, 400))
banner_rect = banner.get_rect()
banner_rect.x = math.ceil(screen.get_width() / 3.33)

# importer les inputs
# PSEUDO INPUT
pseudo_placeholder = 'Pseudo'

pseudo_input_rect = pygame.Rect(screen.get_width() / 2.5, 350, 200, 32)

base_font = pygame.font.Font("assets/font.ttf", 20)
color_active = pygame.Color('orange')
color_passive = pygame.Color('gray15')
color = color_passive

# importer charger notre bouton pour lancer la partie
play_button = pygame.image.load('assets/button.png')
play_button = pygame.transform.scale(play_button, (400, 150))
play_button_rect = play_button.get_rect()
play_button_rect.x = math.ceil(screen.get_width() / 3.33)
play_button_rect.y = math.ceil(screen.get_height() / 1.3)

# Chat
user_text = ''
input_rect = pygame.Rect(25, 350, 600, 32)
active = False


class Client:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serv = os.environ["CONNECTIONIP"]
        port = 5555
        self.socket.connect((serv, port))
        self.listening = True
        self.username = 'No Name No Gain'
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
            try:
                jsonInstance = json.loads(data)
            except JSONDecodeError:
                print("Error Getting json : ", jsonInstance)

        if jsonInstance is not None:
            # IF is game
            self.game.setId(jsonInstance.get("id"))
            self.game.is_ready = jsonInstance.get("is_ready")
            self.game.score = jsonInstance.get("score")
            play1 = jsonInstance.get("player")
            self.game.player.rect.x = play1.get("x")
            self.game.player.rect.y = play1.get("y")
            self.game.player.health = play1.get("health")
            if play1.get("projectile"):
                print("PROJECTILE 1")
                self.game.player.launch_projectile()
                self.game.player.shoot = False
            play2 = jsonInstance.get("player2")
            self.game.player2.rect.x = play2.get("x")
            self.game.player2.rect.y = play2.get("y")
            self.game.player2.health = play2.get("health")
            if play2.get("projectile"):
                print("PROJECTILE 2")
                self.game.player2.launch_projectile()
                self.game.player2.shoot = False
            # else CHAT

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
            pygame.draw.rect(screen, color, input_rect, 2)
            text_surface = base_font.render(user_text, True, (255, 255, 255))
            screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        else:
            client.game.start()
            client.game.sound_manager.play('click')


def sendMessageChat(event, user_text, active):
    if input_rect.collidepoint(event.pos):
        active = True
    while active:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not input_rect.collidepoint(event.pos):
                    active = False
            if event.type == pygame.KEYDOWN:
                # Remove leter
                if user_text != '' and event.key == pygame.K_RETURN:
                    data = json.dumps({"isGame": False, "msg": client.username + ": "+ user_text})
                    client.send(data)
                    active = False
                if active:
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode
            if active:
                color = color_active
            else:
                color = color_passive
            screen.blit(background, (0, 0))
            pygame.draw.rect(screen, color, input_rect, 2)
            text_surface = base_font.render(user_text, True, (255, 255, 255))
            screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

            pygame.display.update()


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

                # si l'event est fermeture de fenetre
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    # RESET MESSAGERIE
                    data_message = {}
                    data_message['message'] = []
                    data_message['message'].append({
                        'isGame': False,
                        'text_message': "Bienvenue sur worms"
                    })
                    with open('message.txt', 'w') as outfile:
                        json.dump(data_message, outfile)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    sendMessageChat(event, user_text, active)

                    # détecter si un joueur lache une touche du clavier
                elif event.type == pygame.KEYDOWN:
                    client.game.pressed[event.key] = True
                    client.send(client.game.toString())

                    if event.key == pygame.K_UP:
                        if client.game.is_playing:
                            if client.game.is_host:
                                client.game.player.isJump = True
                            else:
                                client.game.player2.isJump = True

                    if event.key == pygame.K_SPACE:
                        if client.game.is_playing:
                            if client.game.is_host:
                                if client.game.player.canShoot:
                                    client.game.player.shoot = True
                            else:
                                if client.game.player2.canShoot:
                                    client.game.player2.shoot = True




                elif event.type == pygame.KEYUP:  # si la touche n'est plus utilisé
                    client.game.pressed[event.key] = False

            # fixer le nombre de fps
            clock.tick(FPS)


def menu_screen(client):
    run = True
    pseudo_text = ''
    pseudo_active = False
    while run:
        clock.tick(60)
        screen.blit(background, (0, 0))
        screen.blit(play_button, play_button_rect)

        # Form
        if pseudo_active:
            color = color_active
        else:
            color = color_passive
            # PSEUDO
        pygame.draw.rect(screen, color, pseudo_input_rect)
        pseudo_placeholder_surface = base_font.render(pseudo_placeholder, True, (0, 0, 0))
        pseudo_text_surface = base_font.render(pseudo_text, True, (255, 255, 255))
        pseudo_input_rect.w = max(200, pseudo_text_surface.get_width() + 10)
        screen.blit(pseudo_text_surface, (pseudo_input_rect.x + 5, pseudo_input_rect.y + 5))
        screen.blit(pseudo_placeholder_surface, (pseudo_input_rect.x + 5, pseudo_input_rect.y - 30))
        screen.blit(banner, banner_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pseudo_input_rect.collidepoint(event.pos):
                    pseudo_active = True
                else:
                    pseudo_active = False

                if play_button_rect.collidepoint(event.pos):
                    if pseudo_text != '':
                        client.username = pseudo_text
                    run = False
            if event.type == pygame.KEYDOWN:
                if pseudo_active:
                    if event.key == pygame.K_RETURN:
                        pseudo_text = pseudo_text[:-1]
                    else:
                        pseudo_text += event.unicode

    main(client)


if __name__ == "__main__":
    client = Client()
    client.listen()
    menu_screen(client)
