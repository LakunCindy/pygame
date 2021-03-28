from socket import socket
import threading
import re
import time

from AdaptaterGame import AdaptaterGame
from game import Game


class ClientListener(threading.Thread):

    def __init__(self, server, socket, address):
        super(ClientListener, self).__init__()
        self.server = server
        self.socket = socket
        self.address = address
        self.listening = True
        self.username = "No username"

    def run(self):
        while self.listening:
            data = ""
            try:
                data = self.socket.recv(1024).decode('UTF-8')
            except:
                print("Unable to receive data")
            self.handle_msg(data)
            time.sleep(0.1)
        print("Ending client thread for", self.address)

    def quit(self):
        self.listening = False
        self.socket.close()
        self.server.remove_socket(self.socket)

        print("UN JOUEUR S4EST BARRE WALILA")
    def handle_msg(self, data):
        if data is None or data == '':
            pass
        print("SEND BY SERVER COLLECTED : ",data)
        #username_result = re.search('^USERNAME (.*)$', data)
        game = AdaptaterGame.jsonToGame(data)
        if game is not None and game.connected():
            #DO SOMETHINg
            self.server.echo(game.toString())

