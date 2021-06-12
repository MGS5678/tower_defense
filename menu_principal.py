import pygame
import yaml

def init_data():
    yaml_file = open("player_dat.yml", 'r')
    yaml_content = yaml.load(yaml_file, Loader=yaml.FullLoader)
    return yaml_content

def main(screen):
    """
    Ici on initialise les variables du menu (en mettant pendant ce temps une image de chargement de menu
    """
    chargement_menu = pygame.image.load("images/menu_principal/chargement_menu.png") # on place l'image de chargement
    screen.blit(chargement_menu, (0, 0))
    pygame.display.flip()
    myfont = pygame.font.SysFont('Liberation Serif', 20)

    data = init_data()

    image_menu = pygame.image.load("images/menu_principal/menu.png")
    image_quit_popup = pygame.image.load("images/menu_principal/quit_popup.png")
    image_oui_quit_popup = pygame.image.load("images/menu_principal/oui_quit_popup.png")
    image_non_quit_popup = pygame.image.load("images/menu_principal/non_quit_popup.png")
    image_lvl_ico = pygame.image.load("images/menu_principal/lvl_ico.png")
    image_lvl_info = pygame.image.load("images/menu_principal/lvl_info.png")

    launch = True # variable de la boucle du menu
    popup = {"quit":False, "lvl":[]} # liste des choses supplémentaires à afficher (popup ou autres petits menu)
    back_position = 0 # position du fond qui permet de faire défiler les niveaux
    mouse_pos = [0, 0] # permet de stocker la dernière position de la souris quand elle a bougée
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
                    if 400 < x < 450 and 350 < y < 380:
                        return "close"
                    elif 850 < x < 900 and 350 < y < 380:
                        popup["quit"] = False


        screen.blit(image_menu, (-back_position, 0)) # normalement le fond ne fait que 300 de haut

        for i in range(len(data.get("lvl"))): # nombre max de niveaux affichés
            lvl_y = data.get("lvl").get("lvl" + str(i+1)).get("y") # on prend le niveau et sa hauteur
            screen.blit(image_lvl_ico, (50-back_position+100*i, 200+100*lvl_y))

        if popup.get("quit"):
            screen.blit(image_quit_popup, (300, 200))
            screen.blit(image_oui_quit_popup, (400, 350))
            screen.blit(image_non_quit_popup, (850, 350))
        elif popup.get("lvl"): #elif car on veut ça seulement si le popup quit n'est pas ouvert
            pop = popup.get("lvl")
            lvl = data.get("lvl").get("lvl" + str(pop[0]))
            screen.blit(image_lvl_info, (pop[1], pop[2]-150))
            ligne1 = "Lvl" + str(pop[0]) + ": " + lvl.get("name")
            ligne2 = "Waves: " + str(lvl.get("waves"))
            ligne3 = "Lives: " + str(lvl.get("lives"))
            ligne4 = "High score: " + str(lvl.get("high_score"))
            ligne1_surface = myfont.render(ligne1, False, (255, 0, 0))
            ligne2_surface = myfont.render(ligne2, False, (255, 0, 0))
            ligne3_surface = myfont.render(ligne3, False, (255, 0, 0))
            ligne4_surface = myfont.render(ligne4, False, (255, 0, 0))
            screen.blit(ligne1_surface, (pop[1]+40, pop[2]-145))
            screen.blit(ligne2_surface, (pop[1]+40, pop[2]-115))
            screen.blit(ligne3_surface, (pop[1]+40, pop[2]-85))
            screen.blit(ligne4_surface, (pop[1]+40, pop[2]-55))


        #on regarde la position de la souris pour les niveaux et le reste
        if mouse_pos[0] > 1250 and back_position < 100 * len(data.get("lvl")) - 1200: #on fait bouger les niveaux
            back_position += 2
        elif mouse_pos[0] < 50 and back_position > 0:
            back_position -= 2

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