# Créé par Prof, le 10/04/2014
from __future__ import division
from lycee import *
import pygame, random, time
from pygame.locals import *


pygame.init()
pygame.font.init()


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def pause_temps(temps): # Temps en s
    t0 = time.clock()
    while time.clock()-t0 < temps:
        pass

##############################

def pause():
    pause_fond = pygame.image.load("graphs/fonds/fond_pause.jpg").convert_alpha()
    pause_fond = pygame.transform.smoothscale(pause_fond, (taille_ecran_x, taille_ecran_y))

    continuer_pause = 1
    while continuer_pause:

        for event in pygame.event.get():

            if event.type == QUIT: # Permet de quitter avec la croix de la fenêtre windows.
                continuer_pause = 0
                continuer = 0
            if event.type == KEYDOWN: # Permet de quitter avec la touche escape du clavier.
                if event.key == K_p:
                    continuer_pause = 0

        fenetre.blit(pause_fond, (0,0)) # On blit le fond invisible, avec les contours.

        pygame.display.flip()

##############################

def modifier_matrice(forme, matrice, piece): # On ajoute dans la matrice, à la position des cubes de la pièce, le nombre correspondant à la pièce.
    for i in range(len(forme)):
        for j in range(len(forme[i])):
            if forme[i][j] == 1:
                matrice_principale[objet_piece_pos_y+i][objet_piece_pos_x+j] = piece

##############################

def rotater(forme): # On change de forme, sans dépasser 4.
    if forme<3:
        forme += 1
    else:
        forme = 0
    return forme

##############################

def rotation_possible(forme, matrice, fonc, piece):
    tourner = 1 # Au départ tous différent de 0.
    gauche = 2
    droite = 3
    haut = 4

    if fonc == 1:  # Si on veut effectuer une simple rotation.

        for i in range(len(forme)):
            for j in range(len(forme[i])):
                if objet_piece_pos_x+j < largeur and objet_piece_pos_y+i < hauteur: # Vérifie qu'on ne dépasse pas la matrice.
                    if forme[i][j] == 1 and matrice_principale[objet_piece_pos_y+i][objet_piece_pos_x+j] != 0:# Si la rotation mène à un conflit
                        tourner = 0 # Tourner est à 0, et on sait qu'on ne peut pas tourner.
                else:
                    tourner = 0 # De même on ne peut pas tourner si on est en dehors de la matrice.
        return tourner # On retourne la variable tourner. Si elle est à 0 on effectue pas la rotation, si elle est à 1 on l'effectue.

    elif fonc == 2: # On test en allant à gauche
        if piece != 2:
            for i in range(len(forme)):
                for j in range(len(forme[i])):
                    if objet_piece_pos_x-1 < largeur and objet_piece_pos_y+i < hauteur:
                        if forme[i][j] == 1 and matrice_principale[objet_piece_pos_y+i][objet_piece_pos_x-1] != 0:
                            gauche = 0
                    else:
                        gauche = 0
        else:
            for i in range(len(forme)):
                for j in range(len(forme[i])):
                    if objet_piece_pos_x-2 < largeur and objet_piece_pos_y+i < hauteur:
                        if forme[i][j] == 1 and matrice_principale[objet_piece_pos_y+i][objet_piece_pos_x-2] != 0:
                            gauche = 0
                    else:
                        gauche = 0

        return gauche

    elif fonc == 3: # On test en allant à droite
        for i in range(len(forme)):
            for j in range(len(forme[i])):
                if objet_piece_pos_x+1+j < largeur and objet_piece_pos_y+i < hauteur:
                    if forme[i][j] == 1 and matrice_principale[objet_piece_pos_y+i][objet_piece_pos_x+j+1] != 0:
                        droite = 0
                else:
                    droite = 0

        return droite

    elif fonc == 4: # On test en allant en haut, en différenciant la pièce 2 qui est plus haute.
        if piece != 2:
            for i in range(len(forme)):
                for j in range(len(forme[i])):
                    if forme[i][j] == 1 and (matrice_principale[objet_piece_pos_y-1][objet_piece_pos_x+j] != 0 or matrice_principale[objet_piece_pos_y-1][objet_piece_pos_x+j] != 8):
                        haut = 0
        else:
            for i in range(len(forme)):
                for j in range(len(forme[i])):
                    if objet_piece_pos_x+j < largeur and objet_piece_pos_y-2 < hauteur:
                        if forme[i][j] == 1 and (matrice_principale[objet_piece_pos_y-2][objet_piece_pos_x+j] != 0 or matrice_principale[objet_piece_pos_y-1][objet_piece_pos_x+j] != 8):
                            haut = 0
                    else:
                        haut = 0

        return haut

##############################

def perdu_fonction(forme, matrice): # Si quand on fait apparaitre un pièce tout en haut, elle se superpose avec une autre, ça veut dire qu'on a perdu.
    perdu = 0

    for i in range(len(forme)):
        for j in range(len(forme[i])):
            if objet_piece_pos_y+i+3 < hauteur and objet_piece_pos_x+j < largeur:
                if forme[i][j] == 1 and matrice_principale[i+3][objet_piece_pos_x+j] != 0:
                    perdu = 1

    return perdu

##############################


def bouger_possible_bas(forme, matrice): # S'il n'y a pas de conflit en allant en bas.
    bouger = 1

    for i in range(len(forme)):
        for j in range(len(forme[i])):
            if forme[i][j] == 1 and matrice_principale[objet_piece_pos_y+i+1][objet_piece_pos_x+j] != 0:
                bouger = 0

    return bouger

##############################

def bouger_possible_gauche(forme, matrice): # S'il n'y a pas de conflit en allant à gauche.
    bouger = 1

    for i in range(len(forme)):
        for j in range(len(forme[i])):
            if forme[i][j] == 1 and matrice_principale[objet_piece_pos_y+i][objet_piece_pos_x-1+j] != 0:
                bouger = 0

    return bouger

##############################

def bouger_possible_droite(forme, matrice): # S'il n'y a pas de conflit en allant à droite.
    bouger = 1

    for i in range(len(forme)):
        for j in range(len(forme[i])):
            if forme[i][j] == 1 and matrice_principale[objet_piece_pos_y+i][objet_piece_pos_x+1+j] != 0:
                bouger = 0
    return bouger

##############################

def changer_piece(num_piece):
    global piece # On utilise global sinon les variables ne sont valable que dans la fonction.
    global objet_piece_forme
    global objet_piece_taille
    global objet_piece_pos_x
    global objet_piece_pos_y

    if num_piece == 1: # Pour chaque piece on applique a la piece actuelle les variables de la piece que l'on veut.
        piece = cube

        objet_piece_forme = objet_cube_forme
        objet_piece_taille = objet_cube_taille
        objet_piece_pos_x = objet_cube_pos_x
        objet_piece_pos_y = objet_cube_pos_y
    elif num_piece == 2:
        piece = barre

        objet_piece_forme = objet_barre_forme
        objet_piece_taille = objet_barre_taille
        objet_piece_pos_x = objet_barre_pos_x
        objet_piece_pos_y = objet_barre_pos_y
    elif num_piece == 3:
        piece = t

        objet_piece_forme = objet_t_forme
        objet_piece_taille = objet_t_taille
        objet_piece_pos_x = objet_t_pos_x
        objet_piece_pos_y = objet_t_pos_y
    elif num_piece == 4:
        piece = CarreD

        objet_piece_forme = objet_CarreD_forme
        objet_piece_taille = objet_CarreD_taille
        objet_piece_pos_x = objet_CarreD_pos_x
        objet_piece_pos_y = objet_CarreD_pos_y
    elif num_piece == 5:
        piece = CarreG

        objet_piece_forme = objet_CarreG_forme
        objet_piece_taille = objet_CarreG_taille
        objet_piece_pos_x = objet_CarreG_pos_x
        objet_piece_pos_y = objet_CarreG_pos_y
    elif num_piece == 6:
        piece = Lg

        objet_piece_forme = objet_Lg_forme
        objet_piece_taille = objet_Lg_taille
        objet_piece_pos_x = objet_Lg_pos_x
        objet_piece_pos_y = objet_Lg_pos_y
    elif num_piece == 7:
        piece = Ld

        objet_piece_forme = objet_Ld_forme
        objet_piece_taille = objet_Ld_taille
        objet_piece_pos_x = objet_Ld_pos_x
        objet_piece_pos_y = objet_Ld_pos_y

##############################

# Fonction permettant de créer une matrice, prise sur internet.......
def make_matrice(l, h):
    return [range(l) for i in xrange(h)]

##############################

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

infos_ecran = pygame.display.Info()

taille_ecran_x = infos_ecran.current_w
taille_ecran_y = infos_ecran.current_h

taille_cube = (taille_ecran_y//21) # On récupère la partie entière de la division. On divise la taille de l'écran par le nombre de cubes à afficher.

position_x_jeu = (taille_ecran_x-12*taille_cube)/2

pygame.display.set_icon(pygame.image.load("graphs/icone.png")) # Donne une icône à la fenêtre.
pygame.display.set_caption("Tetris") # Permet de changer le nom de la fenêtre. Doit généralement être avant la ligne suivante.
fenetre = pygame.display.set_mode((taille_ecran_x,taille_ecran_y), FULLSCREEN)

fond_chargement = pygame.image.load("graphs/fonds/fond_chargement.jpg").convert()
fond_chargement = pygame.transform.smoothscale(fond_chargement, (taille_ecran_x, taille_ecran_y))
fenetre.blit(fond_chargement, (0,0))
pygame.display.flip()

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

fond_Original = pygame.image.load("graphs/menu/back_menu.jpg").convert() # On garde l'original en cas de resize +petit -> +grand.
fond_Originale_rec = fond_Original.get_rect()

fond = fond_Original
fond = pygame.transform.smoothscale(fond, (taille_ecran_x, taille_ecran_y))
position_fond = (0,0)
fenetre.blit(fond, position_fond)

ratio_y = taille_ecran_y/fond_Originale_rec.bottom

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

fond_regles = pygame.image.load("graphs/menu/ISN_regles.png").convert()
fond_regles = pygame.transform.smoothscale(fond_regles, (taille_ecran_x, taille_ecran_y))

fond_credit = pygame.image.load("graphs/menu/credit.png").convert()
position_fond_credit = fond_credit.get_rect()

merci = pygame.image.load("graphs/menu/merci.png").convert()
position_fond_merci = merci.get_rect()
merci_rec = merci.get_rect()


fond_noir = pygame.image.load("graphs/menu/ISN_credit_vierge.png").convert()
fond_noir = pygame.transform.smoothscale(fond_noir, (taille_ecran_x, taille_ecran_y))

# Fond perdu
perdu_fond = pygame.image.load("graphs/fonds/fond_perdu.jpg").convert_alpha()
perdu_fond = pygame.transform.smoothscale(perdu_fond, (taille_ecran_x, taille_ecran_y))

# Brique
brique = pygame.image.load("graphs/cubes/brique.png").convert_alpha() # On charge le cube qui va être blitter comme limite de la zone de jeu.
brique = pygame.transform.smoothscale(brique, (taille_cube, taille_cube)) # On le met à l'échelle de l'écran.


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# Cube : Pièce 1
# OO
# OO
cube = pygame.image.load("graphs/cubes/jaune.png").convert_alpha() # Chargement du cube.
cube = pygame.transform.smoothscale(cube, (taille_cube, taille_cube)) # Mise à l'échelle.

objet_cube_forme = (    (  (1,1), (1,1) ) , (  (1,1), (1,1) ) , (  (1,1), (1,1) ) , (  (1,1), (1,1) )     ) # Voir dossier.

objet_cube_taille = ((2, 2), (2, 2), (2, 2), (2, 2)) # Première valeur = large/deuxième = haut.
objet_cube_pos_x = 5 # Position originale des pièces.
objet_cube_pos_y = 2


##############################

# Barre : Pièce 2
# OOOO
barre = pygame.image.load("graphs/cubes/violet.png").convert_alpha()
barre = pygame.transform.smoothscale(barre, (taille_cube, taille_cube))

objet_barre_forme = (    (  (0,1,0), (0,1,0), (0,1,0), (0,1,0) ) , (  (0,0,0,0), (1,1,1,1) ) , ( (0,1,0), (0,1,0), (0,1,0), (0,1,0) ), (  (0,0,0,0), (1,1,1,1) )     )
objet_barre_taille = ((1, 4), (4, 1), (1,4), (4,1)) # Première valeur = large/deuxième = haut.
objet_barre_pos_x = 5
objet_barre_pos_y = 0


##############################

# T : Pièce 3
#   O
#  OOO

t = pygame.image.load("graphs/cubes/ciel.png").convert_alpha()
t = pygame.transform.smoothscale(t, (taille_cube, taille_cube))

objet_t_forme = (    (  (0,1), (1,1,1) ) , (  (0,1), (0,1,1), (0,1) ) , ( (0,0), (1,1,1), (0,1) ), (  (0, 1), (1,1), (0, 1) )     )
objet_t_taille = ((3, 2), (2, 3), (3,2), (2,3)) # Première valeur = large/deuxième = haut.
objet_t_pos_x = 5
objet_t_pos_y = 2



##############################

# CarreD : Pièce 4
#  OO
# OO
CarreD = pygame.image.load("graphs/cubes/vert.png").convert_alpha()
CarreD = pygame.transform.smoothscale(CarreD, (taille_cube, taille_cube))

objet_CarreD_forme = (    (  (0,1,1), (1,1) ) , (  (0,1), (0,1,1), (0,0,1) ) , ( (0,1,1), (1,1) ), (  (0,1), (0,1,1), (0,0,1) )     )
objet_CarreD_taille = ((3, 2), (2, 3), (3,2), (2,3)) # Première valeur = large/deuxième = haut.
objet_CarreD_pos_x = 5
objet_CarreD_pos_y = 2



##############################

# CarreG : Pièce 5
# OO
#  OO
CarreG = pygame.image.load("graphs/cubes/rouge.png").convert_alpha()
CarreG = pygame.transform.smoothscale(CarreG, (taille_cube, taille_cube))

objet_CarreG_forme = (    (  (1,1), (0,1,1) ) , (  (0, 1), (1,1), (1,0) ) , ( (1,1), (0,1,1) ), (  (0, 1), (1,1), (1,0) )     )
objet_CarreG_taille = ((3, 2), (2, 3), (3,2), (2,3)) # Première valeur = large/deuxième = haut.
objet_CarreG_pos_x = 5
objet_CarreG_pos_y = 2

##############################

# Lg : Pièce 6
# O
# OOO
Lg = pygame.image.load("graphs/cubes/bleu.png").convert_alpha()
Lg = pygame.transform.smoothscale(Lg, (taille_cube, taille_cube))

objet_Lg_forme = (    (  (1,0), (1,1,1) ) , (  (0,1, 1), (0,1,0), (0,1,0) ) , ( (0,0),(1,1,1), (0,0,1) ), (  (0, 1), (0,1), (1,1) )     )
objet_Lg_taille = ((3, 2), (2, 3), (3,2), (2,3)) # Première valeur = large/deuxième = haut.
objet_Lg_pos_x = 5
objet_Lg_pos_y = 2

##############################

# Ld : Pièce 7
#   O
# OOO
Ld = pygame.image.load("graphs/cubes/orange.png").convert_alpha()
Ld = pygame.transform.smoothscale(Ld, (taille_cube, taille_cube))

objet_Ld_forme = (    (  (0,0,1), (1,1,1) ) , (  (0,1, 0), (0,1,0), (0,1,1) ) , ( (0,0),(1,1,1), (1,0) ), (  (1, 1), (0,1), (0,1) )     )
objet_Ld_taille = ((3, 2), (2, 3), (3,2), (2,3)) # Première valeur = large/deuxième = haut.
objet_Ld_pos_x = 5
objet_Ld_pos_y = 2

##############################

# Piece actuelle

piece = cube
objet_piece_forme = (    (  (1,0), (1,0), (1,0), (1,0) ) , (  (1, 1, 1, 1), (0,0) ) , ( (1,0), (1,0), (1,0), (1,0) ), (  (1, 1, 1, 1), (0,0) )     )
objet_piece_taille = ((1, 4), (4, 1), (1,4), (4,1)) # Première valeur = large/deuxième = haut.
objet_piece_pos_x = 5
objet_piece_pos_y = 0


##############################

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

#Bouton 1 jouer
bouton = pygame.image.load("graphs/menu/jouer_brumeN.png").convert_alpha() # Ici j'importe le bouton normal
bouton_sepia = pygame.image.load("graphs/menu/jouer_couleur.png").convert_alpha() # Ici j'importe le bouton changer lorsque l'on passe dessus avec la souris
bouton_rec = bouton.get_rect()
bouton = pygame.transform.smoothscale(bouton, (0.7*bouton_rec.right*ratio_y, 0.7*bouton_rec.bottom*ratio_y))
bouton_sepia = pygame.transform.smoothscale(bouton_sepia, (0.7*bouton_rec.right*ratio_y, 0.7*bouton_rec.bottom*ratio_y))

fenetre.blit(bouton,( (taille_ecran_x/2)-(0.7*bouton_rec.right*ratio_y)/2,(taille_ecran_y/2-100*ratio_y)*ratio_y)) # on prend la largeur de la fenetre qu'on divise par 2 pour trouver le milieu on soustrait par la taille du bouton qui a été agrandit de 0.7 fois multiplié par le ratio pour le resize donc on place le bouton au milieu


##############################


#bouton 3 regles
bouton3 = pygame.image.load("graphs/menu/regles_brumeN.png").convert_alpha()
bouton3_sepia = pygame.image.load("graphs/menu/regles_couleur.png").convert_alpha()
bouton3_rec = bouton3.get_rect()
bouton3 = pygame.transform.smoothscale(bouton3, (0.7*bouton3_rec.right*ratio_y, 0.7*bouton3_rec.bottom*ratio_y))
bouton3_sepia = pygame.transform.smoothscale(bouton3_sepia, (0.7*bouton_rec.right*ratio_y, 0.7*bouton_rec.bottom*ratio_y))

fenetre.blit(bouton3,((taille_ecran_x/2)-(0.7*bouton3_rec.right*ratio_y)/2,(taille_ecran_y/2)*ratio_y))


##############################


#bouton 4 credit
bouton4 = pygame.image.load("graphs/menu/credit_brumeN.png").convert_alpha()
bouton4_sepia = pygame.image.load("graphs/menu/credit_couleur.png").convert_alpha()
bouton4_rec = bouton4.get_rect()
bouton4 = pygame.transform.smoothscale(bouton4, (0.7*bouton3_rec.right*ratio_y, 0.7*bouton3_rec.bottom*ratio_y))
bouton4_sepia = pygame.transform.smoothscale(bouton4_sepia, (0.7*bouton_rec.right*ratio_y, 0.7*bouton_rec.bottom*ratio_y))

fenetre.blit(bouton4,((taille_ecran_x/2)-(0.7*bouton3_rec.right*ratio_y)/2,(taille_ecran_y/2+100*ratio_y)*ratio_y))


##############################


#bouton quit
bouton_quit1 = pygame.image.load("graphs/menu/quit_1.png").convert_alpha()
bouton_quit1_rec = bouton_quit1.get_rect()
bouton_quit1 = pygame.transform.smoothscale(bouton_quit1, (0.5*bouton_quit1_rec.right*ratio_y, 0.5*bouton_quit1_rec.bottom*ratio_y))
fenetre.blit(bouton_quit1,(taille_ecran_x-80,30))


##############################


#bouton quit
bouton_quit2 = pygame.image.load("graphs/menu/quit_2.png").convert_alpha()
bouton_quit2_rec = bouton_quit2.get_rect()
bouton_quit2 = pygame.transform.smoothscale(bouton_quit2, (0.5*bouton_quit2_rec.right*ratio_y, 0.5*bouton_quit2_rec.bottom*ratio_y))
fenetre.blit(bouton_quit2,(taille_ecran_x-80,30))


##############################


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

bouton1_afficher = 0  # Il faut initialiser une nouvelle variable.
bouton3_afficher = 0
bouton4_afficher = 0

jeu = 0
credit = 0
reglage = 0
regles = 0
quitt = 0

tempo_credit = 1
tempo_credit1 = 1

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

tetris_classique_musique = pygame.mixer.Sound("sons/tetris_classique.ogg") # On charge les musiques.
tetris_survival_musique = pygame.mixer.Sound("sons/tetris_survival.ogg")
tetris_classique_alex_musique = pygame.mixer.Sound("sons/tetris_classique_alex.ogg")
tetris_classique_musique.play(-1) # Joue la musique en boucle.
tetris_choix = 1 # Stock la chanson actuelle.

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

font = pygame.font.Font("font.ttf", 50) # Charge les fonts TTF.
font_big = pygame.font.Font("font.ttf", 150)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


# Fond visible
fond_visible = pygame.image.load("graphs/fonds/fond_visible.png").convert_alpha() # Charge un fond transparent, sur lequel on va blitter les contours. La transparence va permettre de ne pas cacher les pièces en train de tomber.
fond_visible = pygame.transform.smoothscale(fond_visible, (taille_ecran_x,taille_ecran_y)) # On le resize.


# Fond des bords de la zone de jeu
fond_bords = pygame.image.load("graphs/fonds/fond_bords.jpg").convert_alpha() # Charge un fond transparent, sur lequel on va blitter les contours. La transparence va permettre de ne pas cacher les pièces en train de tomber.
fond_bords = pygame.transform.smoothscale(fond_bords, (taille_ecran_x,taille_ecran_y)) # On le resize.

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

quitter = 0
jouer = 0
continuer = 1
while quitter == 0:
    while continuer and quitter == 0:
        pygame.mouse.set_visible(True)


        for event in pygame.event.get():

            if event.type == QUIT:
                continuer = 0
                quitter = 1

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    continuer = 0
                    quitter = 1
                if event.key == K_RSHIFT or event.key == K_LSHIFT: # So on appuie sur Shift (gauche ou droit).
                    if tetris_choix == 1: # On switch entre les trois musiques, en arrêtant la première, en démarrant la suivante, et en changean la valeur de la variable.
                        tetris_classique_musique.stop()
                        tetris_survival_musique.play(-1)
                        tetris_choix = 2
                    elif tetris_choix == 2:
                        tetris_survival_musique.stop()
                        tetris_classique_alex_musique.play(-1)
                        tetris_choix = 3
                    elif tetris_choix == 3:
                        tetris_classique_alex_musique.stop()
                        tetris_classique_musique.play(-1)
                        tetris_choix = 1

            if event.type == MOUSEBUTTONUP:
                if event.button == 1 and taille_ecran_x-80 < event.pos[0] < (taille_ecran_x-80)+(0.5*bouton_quit1_rec.right*ratio_y) and 30 < event.pos[1] < 30+(0.5*bouton_quit1_rec.bottom*ratio_y):
                    if regles == 0 and credit == 0:
                        continuer = 0
                        quitter = 1


    #bouton 1 : mousemotion

            if event.type == MOUSEMOTION:                                                                                                   #le mousemotion permet de detecter la souris. event.pos[1] c'est l'axe varticale dons tu l'encadre par la position de ton bouton.
                if (taille_ecran_y/2-100*ratio_y) < event.pos[1] < (taille_ecran_y/2-100*ratio_y)+0.7*75*ratio_y and (taille_ecran_x/2)-(0.7*bouton_rec.right*ratio_y)/2 < event.pos[0] < ((taille_ecran_x/2)-(0.7*bouton_rec.right*ratio_y)/2)+0.7*250*ratio_y:     #event.pos[0] pareil pour l'axe horizontal
                    bouton1_afficher = 0      #si la souris est sur le bouton tu met ta variable à 0
                else:                         #sinon tu la met à 1
                    bouton1_afficher = 1



    #bouton 3 : mousemotion

                if (taille_ecran_y/2) < event.pos[1] < (taille_ecran_y/2)+0.7*75*ratio_y and (taille_ecran_x/2)-(0.7*bouton_rec.right*ratio_y)/2 < event.pos[0] < ((taille_ecran_x/2)-(0.7*bouton_rec.right*ratio_y)/2)+0.7*250*ratio_y:
                    bouton3_afficher = 0
                else:
                    bouton3_afficher = 1

    #bouton 4 : mousemotion

                if (taille_ecran_y/2+100*ratio_y) < event.pos[1] < (taille_ecran_y/2+100*ratio_y)+0.7*75*ratio_y and (taille_ecran_x/2)-(0.7*bouton_rec.right*ratio_y)/2 < event.pos[0] < ((taille_ecran_x/2)-(0.7*bouton_rec.right*ratio_y)/2)+0.7*250*ratio_y:
                    bouton4_afficher = 0
                else:
                    bouton4_afficher = 1


    #bouton quit: mousemotion

                if taille_ecran_x-80 < event.pos[0] < (taille_ecran_x-80)+(0.5*bouton_quit1_rec.right*ratio_y) and 30 < event.pos[1] < 30+(0.5*bouton_quit1_rec.right*ratio_y):
                    quitt = 0
                else:
                    quitt = 1


    #bouton 1

            if event.type == MOUSEBUTTONUP:                 #le mousebuttonup detecte le relachement du click souris (enfoncement+relachement) sinon tu peut utiliser le mousebuttondown juste pour l'enfoncement. event.button ==1 cest pour le click gauche et tu remet les memes position du bouton que tu as mis avant.
                if event.button == 1 and (taille_ecran_y/2-100*ratio_y) < event.pos[1] < (taille_ecran_y/2-100*ratio_y)+0.7*75*ratio_y and (taille_ecran_x/2)-(0.7*bouton_rec.right*ratio_y)/2 < event.pos[0] < ((taille_ecran_x/2)-(0.7*bouton_rec.right*ratio_y)/2)+0.7*250*ratio_y:
                    jeu = 1
                else:
                    jeu = 0



    #bouton 3

            if event.type == MOUSEBUTTONUP:
                if event.button == 1 and (taille_ecran_y/2) < event.pos[1] < (taille_ecran_y/2)+0.7*75*ratio_y and (taille_ecran_x/2)-(0.7*bouton_rec.right*ratio_y)/2 < event.pos[0] < ((taille_ecran_x/2)-(0.7*bouton_rec.right*ratio_y)/2)+0.7*250*ratio_y:
                    regles = 1
                else:
                    regles = 0

    #bouton 4

            if event.type == MOUSEBUTTONUP:
                if event.button == 1 and (taille_ecran_y/2+100*ratio_y) < event.pos[1] < (taille_ecran_y/2+100*ratio_y)+0.7*75*ratio_y and (taille_ecran_x/2)-(0.7*bouton_rec.right*ratio_y)/2 < event.pos[0] < ((taille_ecran_x/2)-(0.7*bouton_rec.right*ratio_y)/2)+0.7*250*ratio_y:
                    credit = 1
                else:
                    credit = 0





    #affichage bouton

            fenetre.blit(fond, position_fond)
            if bouton1_afficher:
                fenetre.blit(bouton,(taille_ecran_x/2-0.7*bouton_rec.right*ratio_y/2,(taille_ecran_y/2-100*ratio_y)))
            elif bouton1_afficher == 0:
                fenetre.blit(bouton_sepia,(taille_ecran_x/2-0.7*bouton_rec.right*ratio_y/2,(taille_ecran_y/2-100*ratio_y)))

            if bouton3_afficher:
                fenetre.blit(bouton3,(taille_ecran_x/2-0.7*bouton_rec.right*ratio_y/2,(taille_ecran_y/2)))
            elif bouton3_afficher == 0:
               fenetre.blit(bouton3_sepia,(taille_ecran_x/2-0.7*bouton_rec.right*ratio_y/2,(taille_ecran_y/2)))

            if bouton4_afficher:
                fenetre.blit(bouton4,(taille_ecran_x/2-0.7*bouton_rec.right*ratio_y/2,(taille_ecran_y/2+100*ratio_y)))
            elif bouton4_afficher == 0:
               fenetre.blit(bouton4_sepia,(taille_ecran_x/2-0.7*bouton_rec.right*ratio_y/2,(taille_ecran_y/2+100*ratio_y)))

            if quitt:
                fenetre.blit(bouton_quit1,(taille_ecran_x-80,30))
            elif quitt == 0:
               fenetre.blit(bouton_quit2,(taille_ecran_x-80,30))

            if jeu:
                jeu = 0
                continuer = 0
                jouer = 1

            if regles:
                fenetre.blit(fond_regles,(0,0))
                fenetre.blit(bouton_quit1,(taille_ecran_x-80,30))

                #quitter le jeu sur la page des regles. si on appui sur la croix: retour a la page d'accueil, si on fait echape quitte le jeu.

                if event.type == MOUSEMOTION:
                    if taille_ecran_x-80 < event.pos[0] < (taille_ecran_x-80)+(0.5*bouton_quit1_rec.right*ratio_y) and 30 < event.pos[1] < 30+(0.5*bouton_quit1_rec.bottom*ratio_y):
                        quitt = 0
                    else:
                        quitt = 1

                    if quitt:
                        fenetre.blit(bouton_quit1,(taille_ecran_x-80,30))
                    elif quitt == 0:
                        fenetre.blit(bouton_quit2,(taille_ecran_x-80,30))

                    if event.type == MOUSEBUTTONUP:
                        if event.button == 1 and taille_ecran_x-80 < event.pos[0] < (taille_ecran_x-80)+(0.5*bouton_quit1_rec.right*ratio_y) and 30 < event.pos[1] < 30+(0.5*bouton_quit1_rec.bottom*ratio_y):
                            regles = 0
                            continuer = 1
                        if event.type == KEYDOWN:
                            if event.key == K_ESCAPE:
                                continuer = 0

            if credit == 1:

                position_fond_credit = fond_credit.get_rect()
                pygame.display.flip()
                position_fond_credit = position_fond_credit.move(taille_ecran_x/2-300,taille_ecran_y)
                position_fond_merci = position_fond_merci.move(taille_ecran_x/2-300,taille_ecran_y)
                fenetre.blit(bouton_quit1,(taille_ecran_x-80,30))

                while tempo_credit:
    #Limitation de vitesse de la boucle
    #30 frames par secondes suffisent
                    pygame.time.Clock().tick(30)
                    fenetre.blit(fond_noir,(0,0))

                    pause_temps(0.01)
                    position_fond_credit = position_fond_credit.move(0,-5)
                    fenetre.blit(fond_credit, position_fond_credit)
                    #fenetre.blit(bouton_quit1,(taille_ecran_x-80,30))
                    pygame.display.flip()



    #quitter le jeu sur la page des credits. si on appui sur la croix: retour a la page d'accueil, si on fait echape quitte le jeu.

                    for event in pygame.event.get():

                        if event.type == QUIT:
                            tempo_credit = 0

                        if event.type == KEYDOWN:
                            if event.key == K_ESCAPE:
                                tempo_credit = 0
                                credit = 0

                        if event.type == MOUSEMOTION:
                            if taille_ecran_x-80 < event.pos[0] < (taille_ecran_x-80)+(0.5*bouton_quit2_rec.right*ratio_y) and 30 < event.pos[1] < 30+(0.5*bouton_quit2_rec.right*ratio_y):
                                quitt = 0
                            else:
                                quitt = 1



                    if quitt:
                        fenetre.blit(bouton_quit1,(taille_ecran_x-80,30))
                    elif quitt == 0:
                        fenetre.blit(bouton_quit2,(taille_ecran_x-80,30))



                        if event.type == MOUSEBUTTONUP:
                            if event.button == 1 and taille_ecran_x-80 < event.pos[0] < (taille_ecran_x-80)+(0.5*bouton_quit1_rec.right*ratio_y) and 30 < event.pos[1] < 30+(0.5*bouton_quit1_rec.bottom*ratio_y):
                                credit = 0
                                continuer = 1
                                tempo_credit = 0



                    if position_fond_credit.bottom < 0:
                        while position_fond_merci.bottom > taille_ecran_y/2+100 and tempo_credit1 == 1:
                            pygame.time.Clock().tick(30)
                            fenetre.blit(fond_noir,(0,0))
                            pause_temps(0.01)
                            position_fond_merci = position_fond_merci.move(0,-10)
                            fenetre.blit(merci, position_fond_merci)
                            fenetre.blit(bouton_quit1,(taille_ecran_x-80,30))
                            pygame.display.flip()

                            for event in pygame.event.get():

                                if event.type == QUIT:

                                    tempo_credit1 = 0

                                if event.type == KEYDOWN:
                                    if event.key == K_ESCAPE:

                                        credit = 0
                                        tempo_credit1 = 0
                                if event.type == MOUSEMOTION:
                                    if taille_ecran_x-80 < event.pos[0] < (taille_ecran_x-80)+(0.5*bouton_quit1_rec.right*ratio_y) and 30 < event.pos[1] < 30+(0.5*bouton_quit1_rec.bottom*ratio_y):
                                        quitt = 0
                                    else:
                                        quitt = 1

                                if event.type == MOUSEMOTION:
                                    if taille_ecran_x-80 < event.pos[0] < (taille_ecran_x-80)+(0.5*bouton_quit2_rec.right*ratio_y) and 30 < event.pos[1] < 30+(0.5*bouton_quit2_rec.right*ratio_y):
                                        quitt = 0
                                    else:
                                        quitt = 1



                                if quitt:
                                    fenetre.blit(bouton_quit1,(taille_ecran_x-80,30))
                                elif quitt == 0:
                                    fenetre.blit(bouton_quit2,(taille_ecran_x-80,30))



                                if event.type == MOUSEBUTTONUP:
                                    if event.button == 1 and taille_ecran_x-80 < event.pos[0] < (taille_ecran_x-80)+(0.5*bouton_quit1_rec.right*ratio_y) and 30 < event.pos[1] < 30+(0.5*bouton_quit1_rec.bottom*ratio_y):
                                        credit = 0
                                        continuer = 1

                                        tempo_credit1 = 0
                        pause_temps (2)
                        credit = 0
                        continuer = 1
                        tempo_credit = 0
                        tempo_credit1 = 0
                        pygame.display.flip()
                    pygame.display.flip()
                tempo_credit1 = 1
                position_fond_merci = merci.get_rect()

            tempo_credit = 1
            pygame.display.flip()

        pygame.display.flip()

    # Contient la hauteur et la largeur des matrices "12x25"
    hauteur = 25
    largeur = 12
    partie_non_visible = hauteur-21

    # Matrice principale, qui va contenir les 0 et 1
    matrice_principale = make_matrice(largeur,hauteur)

    # On initialise la matrice, en mettant à 1 les contours, et à 0 le reste.
    for i in range(hauteur):
        for j in range(largeur):
            if j == 0 or j == (largeur-1) or i == (hauteur-1):
                matrice_principale[i][j] = 8
            else:
                matrice_principale[i][j] = 0

    for i in range(hauteur): # On colle les contours pour j = 0 ou j = 11.
    	fond_visible.blit(brique, (position_x_jeu, (i*taille_cube)-partie_non_visible*taille_cube))
    	fond_visible.blit(brique, ((largeur-1)*taille_cube+position_x_jeu, (i*taille_cube)-partie_non_visible*taille_cube))

    for j in range(largeur): # On colle les contours pour i = 20.
        fond_visible.blit(brique, (j*taille_cube+position_x_jeu, 20*taille_cube))


    perdu = 0 # Boucle au cas où on a perdu.
    ligne_a_retirer = 0 # Contient la valeur de la ligne à retirer.

    forme_actuelle = 0 # Permet de switcher entre les formes.
    piece_pose = 0 # Permet d'autoriser ou non les déplacements, et savoir la pièce est posée ou pas.

    t0 = 0 # Temps initial.
    t_attente = 0.8 # Délai pour que les pièces tombent.
    niveau = 0
    score = 0

    s1_ok = 1 # Va permettre dans le jeu de n'exécuter qu'un fois l'ajout de 1 niveau.
    s2_ok = 0
    s3_ok = 0
    s4_ok = 0
    s5_ok = 0
    s6_ok = 0

    piece_actuelle = random.randint(1,7)# Permet de savoir quelle est la pièce actuelle. Généré de manière aléatoire.
    changer_piece(piece_actuelle) # Permet de changer de piece.

    text_score = font.render("Score : ", 1, (255,255,255)) # Permet d'afficher "score" et l"niveau", avant leur valeur.
    text_niveau = font.render("Niveau : ", 1, (255,255,255))

    t0 = time.clock() # On commence la timer.

    regles = 0
    afficher_bouton_quitter = 0

    souris_x = 0 # Stock les coordonnées de la position du curseur de la souris.
    souris_y = 0

    while jouer and quitter == 0:
        score_font = font.render(str(score), 1, (255,255,255)) # Stock le score/niveau. Se raffraichie à chaque tour de boucle.
        niveau_font = font.render(str(niveau), 1, (255,255,255))

        for event in pygame.event.get():

            if event.type == QUIT: # Permet de quitter avec la croix de la fenêtre windows.
                jouer = 0
                continuer = 1
            if event.type == KEYDOWN: # Permet de quitter avec la touche escape du clavier.
                if event.key == K_ESCAPE:
                    jouer = 0
                    continuer = 1
                if event.key == K_UP: # On va tout en bas, tant que l'on peut.
                    while bouger_possible_bas(objet_piece_forme[forme_actuelle], matrice_principale) == 1:
                        objet_piece_pos_y += 1
                    piece_pose = 1
                    score += 5
                if not piece_pose:
                    if event.key == K_SPACE: # Permet d'effectuer une rotation.

                        forme_TMP = forme_actuelle # Forme_TMP est la forme après la forme actuelle.
                        if forme_TMP == 3:
                            forme_TMP = 0
                        else:
                            forme_TMP += 1

                        if rotation_possible(objet_piece_forme[forme_TMP], matrice_principale, 1, piece_actuelle) != 0: # Si il n'y a pas e conflit si on effectue la rotation, on pivote.
                            forme_actuelle = rotater(forme_actuelle)
                        elif rotation_possible(objet_piece_forme[forme_TMP], matrice_principale, 3, piece_actuelle) == 3: # Si la rotation d'avant n'est pas possible, on regarde si en se déplaçant à droite on peut.
                            objet_piece_pos_x += 1
                            forme_actuelle = rotater(forme_actuelle)
                        elif rotation_possible(objet_piece_forme[forme_TMP], matrice_principale, 2, piece_actuelle) == 2: # Sinon, on regarde à gauche.
                            if piece_actuelle != 2:
                                objet_piece_pos_x -= 1
                            else:
                                objet_piece_pos_x -= 2
                            forme_actuelle = rotater(forme_actuelle)
                        elif rotation_possible(objet_piece_forme[forme_TMP], matrice_principale, 4, piece_actuelle) == 4: # Sinon on vérifie si on est pas tout en bas, et on remonte un peu pour pouvoir effectuer la rotation, que l'on bloque ensuite.
                            if piece_actuelle != 2: # La pièce 2 est plu shaute que les autres, donc on doit lui donner un déplacement plus important.
                                objet_piece_pos_y -= 1
                            else:
                                objet_piece_pos_y -= 2
                            forme_actuelle = rotater(forme_actuelle)
                            piece_pose = 1

                    if event.key == K_DOWN: # On descend si on peut.
                        if bouger_possible_bas(objet_piece_forme[forme_actuelle], matrice_principale) == 1:
                            objet_piece_pos_y += 1
                        else:
                            piece_pose = 1
                        t0 = time.clock() # On réinitialise la tempo.

                    if event.key == K_LEFT: # On va à gauche si on peut.
                        if bouger_possible_gauche(objet_piece_forme[forme_actuelle], matrice_principale):
                            objet_piece_pos_x -= 1

                    if event.key == K_RIGHT: # On va à droite si on peut.
                        if bouger_possible_droite(objet_piece_forme[forme_actuelle], matrice_principale):
                            objet_piece_pos_x += 1

                    if event.key == K_p:
                        pause() # On met le jeu en pause.
                    if event.key == K_RSHIFT or event.key == K_LSHIFT: # So on appuie sur Shift (gauche ou droit).
                        if tetris_choix == 1: # On switch entre les trois musiques, en arrêtant la première, en démarrant la suivante, et en changean la valeur de la variable.
                            tetris_classique_musique.stop()
                            tetris_survival_musique.play(-1)
                            tetris_choix = 2
                        elif tetris_choix == 2:
                            tetris_survival_musique.stop()
                            tetris_classique_alex_musique.play(-1)
                            tetris_choix = 3
                        elif tetris_choix == 3:
                            tetris_classique_alex_musique.stop()
                            tetris_classique_musique.play(-1)
                            tetris_choix = 1

                    if event.key == 270 or event.key == 61: # Si on appuie sur +, on augmente le niveau. Sachant que 270 correspond au plus du clavier numérique, et le 61 à celui du clavier "normal".
                        if t_attente>0.17 and niveau <7:
    						niveau += 1
    						t_attente -= 0.1
                    if event.key == 269 or event.key == 54: # Si on appuie sur -, on le baisse si on peut. De même que pour le plus au sujet des valeurs.
                        if niveau > 0:
                            niveau -= 1
                            t_attente += 0.1
            if event.type == MOUSEBUTTONUP: # Si on clique et que l'on est sur le bouton, on arrête
                if event.button == 1 and taille_ecran_x-80 < event.pos[0] < (taille_ecran_x-80)+(int(0.5*bouton_quit1_rec.right*ratio_y)) and 30 < event.pos[1] < 30+(int(0.5*bouton_quit1_rec.bottom*ratio_y)):
                    jouer = 0
                    continuer = 1


        souris_x, souris_y = pygame.mouse.get_pos() # On récupère les coordonnées du curseur de la souris.


        # Si la souris est sur le bouton quitter, on change al valeur de la variable qui va permettre de changer l'affichage du bouton.
        if taille_ecran_x-80 < souris_x < (taille_ecran_x-80)+(0.5*bouton_quit1_rec.right*ratio_y) and 30 < souris_y < 30+(0.5*bouton_quit1_rec.right*ratio_y):
            afficher_bouton_quitter = 0
        else:
            afficher_bouton_quitter = 1

        if t_attente < 0.17: # Au cas où on est en dessous de cette aleur (ça devient trop difficile)
            t_attente = 0.17
        if niveau > 7:
            niveau = 7

        if (time.clock()-t0) > t_attente: # Si on dépasse un certain temps, on fait descendre la pièce si possible et on réinitialise le temps.
            if bouger_possible_bas(objet_piece_forme[forme_actuelle], matrice_principale) == 1:
                objet_piece_pos_y += 1
            else:
                piece_pose = 1
            t0 = time.clock()



        if score >= 300 and s1_ok != 1: # Si le score dépasse 300, on ajoute un niveau.
    		s1_ok = 1
    		if t_attente>0.17 and niveau < 7:
    			t_attente -= 0.1
            	niveau += 1
        elif score > 500 and s2_ok != 1:
    		s2_ok = 1
    		if t_attente>0.17 and niveau < 7:
    			t_attente -= 0.1
            	niveau += 1
        elif score > 800 and s3_ok != 1:
    		s3_ok = 1
    		if t_attente>0.17 and niveau < 7:
    			t_attente -= 0.1
            	niveau += 1
        elif score > 1200 and s4_ok != 1:
    		s4_ok = 1
    		if t_attente>0.17 and niveau < 7:
    			t_attente -= 0.1
            	niveau += 1
        elif score > 1700 and s5_ok != 1:
    		s5_ok = 1
    		if t_attente>0.17 and niveau < 7:
    			t_attente -= 0.1
            	niveau += 1
        elif score > 2300 and s6_ok != 1:
    		s6_ok = 1
    		if t_attente>0.17 and niveau < 7:
    			t_attente -= 0.1
            	niveau += 1

        fenetre.blit(fond_bords, (0,0)) # On colle les bords.

        for i in range(len(objet_piece_forme[forme_actuelle])): # On blit la pièce en train de descendre.
    		for j in range(len(objet_piece_forme[forme_actuelle][i])):
    			if objet_piece_forme[forme_actuelle][i][j] == 1:
    				fenetre.blit(piece, (taille_cube*(objet_piece_pos_x+j)+position_x_jeu,((objet_piece_pos_y*taille_cube)+i*taille_cube)-partie_non_visible*taille_cube))

        for i in range(4,hauteur): # On blit les pièces de la matrice déjà posées.
            for j in range(largeur):
                if matrice_principale[i][j] == 1:
                    fenetre.blit(cube, (j*taille_cube+position_x_jeu,(i-4)*taille_cube))
                elif matrice_principale[i][j] == 2:
                    fenetre.blit(barre, (j*taille_cube+position_x_jeu,(i-4)*taille_cube))
                elif matrice_principale[i][j] == 3:
                    fenetre.blit(t, (j*taille_cube+position_x_jeu,(i-4)*taille_cube))
                elif matrice_principale[i][j] == 4:
                    fenetre.blit(CarreD, (j*taille_cube+position_x_jeu,(i-4)*taille_cube))
                elif matrice_principale[i][j] == 5:
                    fenetre.blit(CarreG, (j*taille_cube+position_x_jeu,(i-4)*taille_cube))
                elif matrice_principale[i][j] == 6:
                    fenetre.blit(Lg, (j*taille_cube+position_x_jeu,(i-4)*taille_cube))
                elif matrice_principale[i][j] == 7:
                    fenetre.blit(Ld, (j*taille_cube+position_x_jeu,(i-4)*taille_cube))


        nb_ligne_supprimee = 0 # On remet toujours cette variable à 0.
        for i in range(hauteur-1): # On va tester toute la matrice.
            line = 1 # Au départ à 1 pour dire qu'il faut supprimer une ligne.
            for j in range(largeur):
                if matrice_principale[i][j] == 0: # Si une seule des valeur de la ligne est à 0
                    line = 0 # On passe à 0.
            if line: # Si après avoir tester la ligne, ligne est toujours à 1.
                nb_ligne_supprimee += 1 # On ajoute 1 au nombre de ligne. Cele av permettre de savoir combien de ligne on supprime d'un coup.
                ligne_a_retirer = i # On ne veut pas toucher à la valeur de i, donc on stock sa valeur dans une autre variable.
                while ligne_a_retirer != 0: # Tant qu'on a pas parcouru toute la matrice,
                    for j in range(largeur): # On décale tous les cubes vers le bas.
                        matrice_principale[ligne_a_retirer][j] = matrice_principale[ligne_a_retirer-1][j]
                    ligne_a_retirer -= 1 # A chaque fois on diminue la valeur de cette variable, pour changer de ligne.

                ligne_a_retirer = 0 # On réinitialise la variable.
                score += 60+((nb_ligne_supprimee-1)*10) # On met à jour le score.



        fenetre.blit(fond_visible, (0,0)) # On blit le fond invisible, avec les contours.
        fenetre.blit(text_score, (10,0)) # On blit "Score :"
        fenetre.blit(text_niveau, (10,font.size("Niveau : ")[1])) # On blit "Niveau :"
        fenetre.blit(score_font, (font.size("Score : ")[0]+10,0)) # On blit le score, après le "Score:"
        fenetre.blit(niveau_font, (font.size("Niveau : ")[0]+10,font.size("Niveau : ")[1])) ; # On blit le niveau.

        if afficher_bouton_quitter: # On affiche la bouton quitter, selon la position de la souris, ça ne sera pas le même.
            fenetre.blit(bouton_quit1,(taille_ecran_x-80,30))
        elif afficher_bouton_quitter == 0:
           fenetre.blit(bouton_quit2,(taille_ecran_x-80,30))



        pygame.display.flip()

        if piece_pose == 1: # Détecte si la pièce est tout enbas.
            score += 20
            modifier_matrice(objet_piece_forme[forme_actuelle], matrice_principale, piece_actuelle) # On met à jour la matrice.

            piece_actuelle = random.randint(1,7) # On choisit une pièce au hasard.
            changer_piece(piece_actuelle) # On met à jour la piece actuelle.

            if perdu_fonction(objet_piece_forme[forme_actuelle], matrice_principale): # Si on a perdu.

                perdu = 1 # On entre dans une oucle qui va afficher "perdu !", ainsi que notre score.
                while perdu:
                    for event in pygame.event.get():

                        if event.type == QUIT: # Permet de quitter avec la croix de la fenêtre windows, ou en faisant clique droit -> fermer sur l'icone du jeu. Sachant que la croix n'est normalement pas disponible comme on est en plein écran.
                            perdu = 0
                            jouer = 0
                            continuer = 1

                        if event.type == MOUSEBUTTONUP: # Permet de quitter avec le bouton quitter.
                            if event.button == 1 and taille_ecran_x-80 < event.pos[0] < (taille_ecran_x-80)+(0.5*bouton_quit1_rec.right*ratio_y) and 30 < event.pos[1] < 30+(0.5*bouton_quit1_rec.bottom*ratio_y):
                                perdu = 0
                                jouer = 0
                                continuer = 1

                        if event.type == KEYDOWN: # Permet de quitter avec la touche escape du clavier.
                            if event.key == K_ESCAPE:
                                jouer = 0
                                perdu = 0
                                continuer = 1

                    souris_x, souris_y = pygame.mouse.get_pos()

                    if taille_ecran_x-80 < souris_x < (taille_ecran_x-80)+(0.5*bouton_quit1_rec.right*ratio_y) and 30 < souris_y < 30+(0.5*bouton_quit1_rec.right*ratio_y):
                        afficher_bouton_quitter = 0
                    else:
                        afficher_bouton_quitter = 1

                    fenetre.blit(perdu_fond, (0,0)) # On colle le fond perdu.

                    if afficher_bouton_quitter: # Puis on blit le bouton quitter.
                        fenetre.blit(bouton_quit1,(taille_ecran_x-80,30))
                    elif afficher_bouton_quitter == 0:
                       fenetre.blit(bouton_quit2,(taille_ecran_x-80,30))


                    # Et on affiche les différents textes.
                    perdu_font = font_big.render("Perdu !", 1, (200,0,0)) # Texte Perdu en rouge.
                    votre_score = font.render("Votre score est : ", 1, (9,157,255)) # En bleu.
                    score_font = font_big.render(str(score), 1, (255,255,255))

                    fenetre.blit(perdu_font, ((taille_ecran_x/2)-(font_big.size("Perdu !")[0])/2,30))
                    fenetre.blit(votre_score, ((taille_ecran_x/2)-(font.size("Votre score est : ")[0])-50,(taille_ecran_y/2)+50))
                    fenetre.blit(score_font, ((taille_ecran_x/2)-50,(taille_ecran_y/2)-20)) # Affiche le score.

                    pygame.display.flip() # On raffraichit l'écran.

            piece_pose = 0 # Si a pas perdu, on dis au logiciel que la pièce n'est plus posé puis on recommence.


pygame.display.quit()
pygame.font.quit()
pygame.quit()
