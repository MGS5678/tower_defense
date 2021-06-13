import pygame
import yaml
import time

def init_data():
    yaml_file = open("player_dat.yml", 'r')
    yaml_content = yaml.load(yaml_file, Loader=yaml.FullLoader)
    return yaml_content

def lvl_popup(pop, lvl, image, screen):
    myfont = pygame.font.SysFont('Liberation Serif', 20)
    flip = 0
    if pop[1] > 1000:
        image = pygame.transform.flip(image, True, False)
        screen.blit(image, (pop[1]-300, pop[2] - 150))
        flip = 1
    else:
        screen.blit(image, (pop[1], pop[2] - 150))
    ligne1 = "Niveau " + str(pop[0]) + ": "  # on est obligé de faire les lignes séparément...
    ligne2 = lvl.get("name")
    ligne3 = "Waves: " + str(lvl.get("waves"))
    ligne4 = "Lives: " + str(lvl.get("lives"))
    ligne1_surface = myfont.render(ligne1, False, (255, 0, 0))
    ligne2_surface = myfont.render(ligne2, False, (255, 0, 0))
    ligne3_surface = myfont.render(ligne3, False, (255, 0, 0))
    ligne4_surface = myfont.render(ligne4, False, (255, 0, 0))
    screen.blit(ligne1_surface, (pop[1] + 40 - flip*330, pop[2] - 145))
    screen.blit(ligne2_surface, (pop[1] + 40 - flip*330, pop[2] - 115))
    screen.blit(ligne3_surface, (pop[1] + 40 - flip*330, pop[2] - 85))
    screen.blit(ligne4_surface, (pop[1] + 40 - flip*330, pop[2] - 55))

def afficher_map(map, screen):
    ecart = 30//len(map)
    taille = 180//len(map)
    distance = 10-ecart
    for y in range(len(map)):
        for x in range(len(map[0])):
            color = (88, 88, 88)
            if map[y][x] == 1:
                color = (255, 0, 0)
            elif map[y][x] == 2:
                color = (0, 168, 243)
            elif map[y][x] == 3:
                color = (239, 184, 55)
            pygame.draw.rect(screen, color, pygame.Rect(distance + (taille * x + ecart), 500 + distance + (taille * y + ecart), taille - ecart, taille - ecart))

def main(screen):
    """
    Ici on initialise les variables du menu (en mettant pendant ce temps une image de chargement de menu
    """
    chargement_menu = pygame.image.load("images/menu_principal/chargement_menu.png") # on place l'image de chargement
    screen.blit(chargement_menu, (0, 0))
    pygame.display.flip()

    image_menu = pygame.image.load("images/menu_principal/menu.png")
    image_quit_popup = pygame.image.load("images/menu_principal/quit_popup.png")
    image_oui_quit_popup = pygame.image.load("images/menu_principal/oui_quit_popup.png")
    image_non_quit_popup = pygame.image.load("images/menu_principal/non_quit_popup.png")
    image_lvl_ico = pygame.image.load("images/menu_principal/lvl_ico.png")
    image_lvl_info = pygame.image.load("images/menu_principal/lvl_info.png")
    image_cadenas_lvl = pygame.image.load("images/menu_principal/cadenas_lvl.png")
    image_actual_lvl = pygame.image.load("images/menu_principal/actual_lvl.png")
    image_start_button = pygame.image.load("images/menu_principal/start_button.png")

    data = init_data()
    launch = True # variable de la boucle du menu
    popup = {"quit":False, "lvl":[]} # liste des choses supplémentaires à afficher (popup ou autres petits menu)
    back_position = 0 # position du fond qui permet de faire défiler les niveaux
    mouse_pos = [0, 0] # permet de stocker la dernière position de la souris quand elle a bougée
    choose_lvl = data.get("lvl").get("lvl" + str(data.get("player").get("actual_lvl")))

    """
    Dès que les images sont chargées on lance le menu avec une boucle while qui se ferme quand on change de menu
    """
    while launch:
        a = time.clock()
        for event in pygame.event.get():  # tout les évènements
            if event.type == pygame.QUIT:
                return "close" # fermeture du jeu
            elif event.type == pygame.KEYDOWN:  # Detection si le joueur appuye sur une touche
                if event.key == pygame.K_ESCAPE:
                    popup["quit"] = True if popup.get("quit") == False else False # on change la valeur de popup en fonction de si il est déjà affiché
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = [event.pos[0], event.pos[1]] # on note la dernière position de la souris
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x = event.pos[0]
                    y = event.pos[1]
                    if popup.get("quit"):
                        if 400 < x < 450 and 350 < y < 380:
                            return "close"
                        elif 850 < x < 900 and 350 < y < 380:
                            popup["quit"] = False
                    elif popup.get("lvl"):
                        choose_lvl = data.get("lvl").get("lvl" + str(popup.get("lvl")[0]))
                    elif choose_lvl.get("number") <= data.get("player").get("actual_lvl") and 1190 < x < 1290 and 640 < y < 690:
                        return "lvl" + str(choose_lvl.get("number"))


        screen.blit(image_menu, (-back_position, 0)) # normalement le fond ne fait que 300 de haut

        for i in range(len(data.get("lvl"))): # nombre max de niveaux affichés
            lvl_y = data.get("lvl").get("lvl" + str(i+1)).get("y") # on prend le niveau et sa hauteur
            if i < len(data.get("lvl")) - 1:
                pygame.draw.line(screen, (255, 0, 255), (50-back_position+100*i + 75//2, 200+100*lvl_y + 75//2), (50-back_position+100*(i+1) + 75//2, 200+100*data.get("lvl").get("lvl" + str(i+2)).get("y") + 75//2), 5)
            screen.blit(image_lvl_ico, (50-back_position+100*i, 200+100*lvl_y))
            if i+1 > data.get("player").get("actual_lvl"):
                screen.blit(image_cadenas_lvl, (75-back_position+100*i, 225+100*lvl_y))
            elif i+1 == data.get("player").get("actual_lvl"):
                screen.blit(image_actual_lvl, (70 - back_position + 100 * i, 225 + 100 * lvl_y))

        if popup.get("quit"):
            screen.blit(image_quit_popup, (300, 200))
            screen.blit(image_oui_quit_popup, (400, 350))
            screen.blit(image_non_quit_popup, (850, 350))
        elif popup.get("lvl"): #elif car on veut ça seulement si le popup quit n'est pas ouvert
            pop = popup.get("lvl")
            lvl = data.get("lvl").get("lvl" + str(pop[0]))
            lvl_popup(pop, lvl, image_lvl_info, screen)


        #on regarde la position de la souris pour les niveaux et le reste
        if not popup.get("quit"):
            if mouse_pos[0] > 1250 and back_position < 100 * len(data.get("lvl")) - 1200: #on fait bouger les niveaux
                back_position += 2
            elif mouse_pos[0] < 50 and back_position > 0:
                back_position -= 2

        #affichage du niveau sélectionné
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 500, 1300, 900))
        afficher_map(choose_lvl.get("map"), screen)
        if choose_lvl.get("number") <= data.get("player").get("actual_lvl"):
            screen.blit(image_start_button, (1190, 640))


        popup["lvl"] = []
        if 50 < mouse_pos[0] < 1250 and 200 < mouse_pos[1] < 500:
            compteur_zone = 0
            pos = mouse_pos[0] - 25 + back_position
            while pos > 0:
                pos -= 25 if compteur_zone%2 == 0 else 75 # ceci permet de différencier les zones dans la map ce qui permet de voir si on clic sur un lvl
                compteur_zone += 1
            if compteur_zone%2 == 0:
                lvl = compteur_zone//2
                y = data.get("lvl").get("lvl" + str(lvl)).get("y")
                if 200+100*y < mouse_pos[1] < 275 + 100*y:
                    popup["lvl"] = [lvl, mouse_pos[0], mouse_pos[1]]
        pygame.display.flip()
        print(time.clock()-a)