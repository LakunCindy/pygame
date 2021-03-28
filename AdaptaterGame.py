import json
from json import JSONDecodeError

from game import Game


class AdaptaterGame:

    @staticmethod
    def jsonToGame(data):
        if data is None:
            return Game()
        if data == '':
            return Game()
        else:
            try:
                jsonParsed = json.loads(data)
            except JSONDecodeError:
                return Game()
            #GAME
            game = Game()
            game.id = jsonParsed["id"]
            game.is_ready = jsonParsed["is_ready"]
            game.score = jsonParsed["score"]
            game.is_host = jsonParsed["is_host"]
            #PLAYER 1
            player1Parse = jsonParsed["player"]
            game.player.rect.x = player1Parse["x"]
            game.player.rect.y = player1Parse["y"]
            game.player.health = player1Parse["health"]
            game.player.shoot = player1Parse["projectile"]

            #PLAYER 2
            player2Parse = jsonParsed["player2"]
            game.player2.rect.x = player2Parse["x"]
            game.player2.rect.y = player2Parse["y"]
            game.player2.health = player2Parse["health"]
            game.player2.shoot = player2Parse["projectile"]

            return game


