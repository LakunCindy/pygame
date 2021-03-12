import pygame
from game import Game

pygame.init()

#générer la fenetre du jeu
pygame.display.set_caption("Comet fall Game")
screen = pygame.display.set_mode((1080,720))

#Charger l'arrière plan
background = pygame.image.load('assets/bg.jpg')

game = Game()

#boucle tant que cette condition est vrai
running = True
while running:
    #tant que le jeu est actif

    #arrière plan
    screen.blit(background,(0,-200))

    #appliquer image du joueur
    screen.blit(game.player.image,game.player.rect)

    #verfier si le joueur souhaite aller à gauche ou à droite
    if game.pressed.get(pygame.K_RIGHT) and game.player.rect.x + game.player.rect.width < screen.get_width():
        game.player.move_right()
    if game.pressed.get(pygame.K_LEFT) and game.player.rect.x > 0:
        game.player.move_left()

    #mettre à jour l'ecran
    pygame.display.flip()

    #si le joueur ferme la fenetre
    for event in pygame.event.get():
        #si l'event est fermeture de fenetre
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            #détecter si un joueur lache une touche du clavier
        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True
        elif event.type == pygame.KEYUP: #si la touche n'est plus utilisé
            game.pressed[event.key] = False
            # #quelle touche a été utilisée
            # if event.key == pygame.K_RIGHT:
            #     #Déplacement vers la droite"
            #     game.player.move_right()
            # elif event.key == pygame.K_LEFT:
            #     game.player.move_left()
