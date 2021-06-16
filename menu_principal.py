import pygame
import yaml

def init_data():
    yaml_file = open("player_dat.yml", 'r')
    yaml_content = yaml.load(yaml_file, Loader=yaml.FullLoader)
    return yaml_content

def lvl_popup(pop, lvl, image, screen, myfont, back_position):
    flip = -40
    x = -13-back_position+100*(lvl.get("number"))
    if pop[1] > 500:
        image = pygame.transform.flip(image, True, False) #50-back_position+100*i, 100+100*lvl_y
        screen.blit(image, (x-300, 100+100*lvl.get("y") - 103))
        flip = 290
    else:
        screen.blit(image, (x, 100+100*lvl.get("y") - 103))
    ligne1_surface = myfont.render("Niveau " + str(pop[0]) + ": ", False, (255, 0, 0))
    ligne2_surface = myfont.render(lvl.get("name"), False, (255, 0, 0))
    ligne3_surface = myfont.render("Vagues: " + str(lvl.get("waves")), False, (255, 0, 0))
    ligne4_surface = myfont.render("Vies: " + str(lvl.get("lives")), False, (255, 0, 0))
    screen.blit(ligne1_surface, (x - flip, 100*lvl.get("y")))
    screen.blit(ligne2_surface, (x - flip, 30+100*lvl.get("y")))
    screen.blit(ligne3_surface, (x - flip, 60+100*lvl.get("y")))
    screen.blit(ligne4_surface, (x - flip, 90+100*lvl.get("y")))

def afficher_map(map, screen):
    val = len(map) if len(map) > len(map[0]) else len(map[0])
    ecart = 30//val
    taille = 180//val
    distance_y = 400 + ecart + (200 - (len(map)*taille) - ecart) // 2
    distance_x = ecart + (200 - (len(map[0])*taille) - ecart) // 2
    colors = {0:(88, 88, 88), 1:(255, 0, 0), 2:(0, 168, 243), 3:(239, 184, 55)}
    for y in range(len(map)):
        for x in range(len(map[0])):
            pygame.draw.rect(screen, colors.get(map[y][x]), pygame.Rect(distance_x + taille * x, distance_y + taille * y, taille - ecart, taille - ecart))
    return distance_x*2 + len(map[0]*taille)

def afficher_lvl(lvl, screen, image_start_button, data, myfont):
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 400, 800, 200))
    last_x = afficher_map(lvl.get("map"), screen)
    if lvl.get("number") <= data.get("player").get("actual_lvl"):
        screen.blit(image_start_button, (690, 540))

    lvl_name = myfont.render("Niveau " + str(lvl.get("number")) + ": " + lvl.get("name"), False, (255, 0, 0))
    waves = myfont.render("Vagues: " + str(lvl.get("waves")), False, (255, 0, 0))
    lives = myfont.render("Vies: " + str(lvl.get("lives")), False, (255, 0, 0))
    highscore = myfont.render("Highscore: " + str(lvl.get("high_score")), False, (255, 0, 0))
    screen.blit(lvl_name, (last_x, 410))
    screen.blit(waves, (last_x, 450))
    screen.blit(lives, (last_x, 490))
    screen.blit(highscore, (540, 410))

def main(screen):
    """
    Ici on initialise les variables du menu (en mettant pendant ce temps une image de chargement de menu car init_data() prend beaucoup de temps)
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
    choose_lvl = [data.get("lvl").get("lvl" + str(data.get("player").get("actual_lvl"))), 0]
    myfont = pygame.font.SysFont('Liberation Serif', 20)
    clock = pygame.time.Clock()

    """
    Dès que les images sont chargées on lance le menu avec une boucle while qui se ferme quand on change de menu
    """
    while launch:
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
                        if 300 < x < 350 and 325 < y < 355:
                            return "close"
                        elif 450 < x < 500 and 325 < y < 355:
                            popup["quit"] = False
                    elif popup.get("lvl"):
                        choose_lvl[0] = data.get("lvl").get("lvl" + str(popup.get("lvl")[0]))
                    elif choose_lvl[0].get("number") <= data.get("player").get("actual_lvl") and 690 < x < 790 and 540 < y < 590:
                        return choose_lvl[0]

        screen.blit(image_menu, (-back_position, 0)) # normalement le fond ne fait que 300 de haut

        for i in range(len(data.get("lvl"))): # nombre max de niveaux affichés
            lvl_y = data.get("lvl").get("lvl" + str(i+1)).get("y") # on prend le niveau et sa hauteur
            if i < len(data.get("lvl")) - 1 and -75 < 87-back_position+100*i < 1300:
                pygame.draw.line(screen, (255, 0, 255), (87-back_position+100*i, 137+100*lvl_y), (87-back_position+100*(i+1), 137+100*data.get("lvl").get("lvl" + str(i+2)).get("y")), 5)
            screen.blit(image_lvl_ico, (50-back_position+100*i, 100+100*lvl_y))
            if i+1 > data.get("player").get("actual_lvl"):
                screen.blit(image_cadenas_lvl, (75-back_position+100*i, 125+100*lvl_y))
            elif i+1 == data.get("player").get("actual_lvl"):
                screen.blit(image_actual_lvl, (70-back_position+100*i, 125+100*lvl_y))

        if popup.get("quit"):
            screen.blit(image_quit_popup, (266, 200))
            screen.blit(image_oui_quit_popup, (300, 325))
            screen.blit(image_non_quit_popup, (450, 325))
        elif popup.get("lvl"): #elif car on veut ça seulement si le popup quit n'est pas ouvert
            pop = popup.get("lvl")
            lvl = data.get("lvl").get("lvl" + str(pop[0]))
            lvl_popup(pop, lvl, image_lvl_info, screen, myfont, back_position)

        #on regarde la position de la souris pour les niveaux et le reste
        if not popup.get("quit"):
            if mouse_pos[0] > 750 and back_position < 100 * len(data.get("lvl")) - 700: #on fait bouger les niveaux
                back_position += 3
            elif mouse_pos[0] < 25 and back_position > 0:
                back_position -= 3

        #affichage du niveau sélectionné
        if choose_lvl[0] != choose_lvl[1]: # ce if permet d'afficher le popup seulement si il change ce qui économise du temps
            afficher_lvl(choose_lvl[0], screen, image_start_button, data, myfont)
            choose_lvl[1] = choose_lvl[0]

        popup["lvl"] = []
        if 50 < mouse_pos[0] < 750 and 100 < mouse_pos[1] < 400:
            compteur_zone = 0
            pos = mouse_pos[0] - 25 + back_position
            while pos > 0:
                pos -= 25 if compteur_zone%2 == 0 else 75 # ceci permet de différencier les zones dans la map ce qui permet de voir si on clic sur un lvl
                compteur_zone += 1
            if compteur_zone%2 == 0:
                lvl = compteur_zone//2
                y = data.get("lvl").get("lvl" + str(lvl)).get("y")
                if 100+100*y < mouse_pos[1] < 175 + 100*y:
                    popup["lvl"] = [lvl, mouse_pos[0], mouse_pos[1]]
        pygame.display.update()
        clock.tick(100)