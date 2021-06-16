import pygame

def afficher_map(screen, map):
    colors = {0: (88, 88, 88), 1: (255, 0, 0), 2: (0, 168, 243), 3: (239, 184, 55)}
    for y in range(len(map)):
        for x in range(len(map[0])):
            pygame.draw.rect(screen, colors.get(map[y][x]), pygame.Rect(x*50, y*50, 50, 50))

def main(screen, lvl):
    chargement_menu = pygame.image.load("images/menu_principal/chargement_menu.png")  # on place l'image de chargement
    screen.blit(chargement_menu, (0, 0))
    pygame.display.flip()

    map = lvl.get("map")
    waves = lvl.get("waves")
    lives = lvl.get("lives")
    name = lvl.get("name")
    colors = {0: (88, 88, 88), 1: (255, 0, 0), 2: (0, 168, 243), 3: (239, 184, 55)}

    launch = True
    while launch:
        afficher_map(screen, map)
        pygame.display.flip()