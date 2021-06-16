import pygame
import menu_principal
import in_game

"""
Initialisation de pygame
"""
pygame.display.init()
pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((800, 600)) # création de la fenêtre*



"""
Création des variables du jeu
"""
size = (pygame.display.Info().current_w, pygame.display.Info().current_h) # variable qui stock la taille de l'écran
game = 0 # variable qui permet de se situer dans le jeu entre les différents menus et le jeu
launch = True # variable qui fait tourner le jeu, quand elle est à 0 la fenêtre se ferme
lvl = ""

"""
Boucle du jeu qui permet de lancer les fonctions du jeu en fonction de l'endroit où le joueur se trouve (menu, jeu, ...)
"""
while launch:
    if game == 0:
        retour = menu_principal.main(screen) # on lance le menu et on récupère la valeur de retour ce qui permet de faire passer des infos ici
        if retour == "close":
            launch = False
        else:
            game = 1
            lvl = retour

    elif game == 1:
        in_game.main(screen, lvl)
        game = 0

pygame.quit()