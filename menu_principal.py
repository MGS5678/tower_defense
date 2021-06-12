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

    data = init_data()

    image_menu = pygame.image.load("images/menu_principal/menu.png")
    image_quit_popup = pygame.image.load("images/menu_principal/quit_popup.png")
    image_oui_quit_popup = pygame.image.load("images/menu_principal/oui_quit_popup.png")
    image_non_quit_popup = pygame.image.load("images/menu_principal/non_quit_popup.png")
    image_lvl_ico = pygame.image.load("images/menu_principal/lvl_ico.png")

    launch = True # variable de la boucle du menu
    popup = False # liste des choses supplémentaires à afficher (popup ou autres petits menu)
    back_position = 0 # position du fond qui permet de faire défiler les niveaux
    """
    Dès que les images sont chargées on lance le menu avec une boucle while qui se ferme quand on change de menu
    """
    while launch:

        for event in pygame.event.get():  # tout les évènements
            if event.type == pygame.QUIT:
                return "close" # fermeture du jeu
            elif event.type == pygame.KEYDOWN:  # Detection si le joueur appuye sur une touche
                if event.key == pygame.K_ESCAPE:
                    popup = image_quit_popup if popup == False else False # on change la valeur de popup en fonction de si il est déjà affiché
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x = event.pos[0]
                    y = event.pos[1]

                    if popup == image_quit_popup: # on va vérifier si il clic sur une réponse du popup quit
                        if 400 < x < 450 and 350 < y < 380:
                            return "close"
                        elif 850 < x < 900 and 350 < y < 380:
                            popup = False


        screen.blit(image_menu, (0, 0))

        for i in range(12): # nombre max de niveaux affichés
            try:
                lvl_y = data.get("lvl").get("lvl" + str(i+1)).get("y") # on prend le niveau et sa hauteur
            except AttributeError:
                break
            screen.blit(image_lvl_ico, (100-back_position+100*i, 200+100*lvl_y))

        if popup == image_quit_popup:
            screen.blit(image_quit_popup, (300, 200))
            screen.blit(image_oui_quit_popup, (400, 350))
            screen.blit(image_non_quit_popup, (850, 350))
        #il faut aussi afficher les différents boutons

        pygame.display.flip()