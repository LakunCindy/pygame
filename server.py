import os
import socket
import signal  # identifie les signaux pour kill le programme
import sys  # utilisé pour sortir du programme
import time

import pygame

from AdaptaterGame import AdaptaterGame
from ClientThread import ClientListener
from game import Game

pygame.init()


class Server:

    def __init__(self):
        serv = os.environ["CONNECTIONIP"]
        port = 5555
        self.connected = set()
        self.games = {}
        self.idCount = 0
        self.gameId = None
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.bind((serv, port))
        self.listener.listen(2)
        print("Listening on port", port)
        self.clients_sockets = []
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def signal_handler(self, signal, frame):
        self.listener.close()
        self.echo("QUIT")

    def run(self):
        while True:
            print("listening new customers")
            try:
                (client_socket, client_adress) = self.listener.accept()
                print("Connected to:", client_adress)
                self.idCount += 1
                #p = 0
                self.gameId = (self.idCount - 1) // 2
                if self.idCount % 2 == 1:
                    game = Game()
                    game.setId(self.gameId)
                    self.games[self.gameId] = game
                    print("Creating a new game...")
                else:
                    self.games[self.gameId].is_ready = True
                    #p = 1
                game = self.games[self.gameId]
                #socket.socket.sendall(AdaptaterGame.gameToJson(game))
            except socket.error:
                sys.exit("Cannot connect clients")
            self.clients_sockets.append(client_socket)
            #Send echo
            print("Start the thread for client:", client_adress)
            print("GAME : ", game.toString())
            client_thread = ClientListener(self, client_socket, client_adress)
            client_thread.start()
            self.echo(game.toString())

            time.sleep(0.1)

    def remove_socket(self, socket):
        self.clients_sockets.remove(socket)

    def echo(self, data):
        for sock in self.clients_sockets:
            try:
                sock.sendall(data.encode("UTF-8"))
            except socket.error:
                print("Cannot send the message")


if __name__ == "__main__":
    server = Server()
    server.run()
