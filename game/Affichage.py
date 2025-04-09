#Cette page gere tout l'affichage en temps reel du jeu

import pygame
#La bibliotheque pygame sert a affichage le jeu
from time import *
#La bibliotheque time permet de faire des moments de pause
import Outil as Outil
#Cela sert a recuperer toutes les classes secondaires dont on aura besoin ici

pygame.init()
size = width, height = 1600, 820
screen = pygame.display.set_mode(size)
#Creation d'une fenêtre d'une taille de 1600 pixels sur 820 pixels
  
class Affichage:
    def __init__(self, grille_texte, index, score, creature, depart, objectif, eaux, leviers, temps, compteur, mort):
        self.grille = []
        for ligne in grille_texte:
            Ligne = []
            for colonne in ligne:
                Ligne.append(colonne)
            self.grille.append(Ligne)

        self.set_creature(creature)
        self.set_index(index)
        self.set_score(score)
        self.set_reference_lemming(len(creature))
        self.set_depart(depart)
        self.set_objectif(objectif)
        self.set_compteur(compteur)
        self.set_eaux(eaux)
        self.set_leviers(leviers)
        self.set_temps(temps)
        self.set_mort(mort)
    """
    Cette classe recupere toute les donnees du jeu et s'en sert pour afficher ce qu'il y a besoin d'afficher
    """

    def get_creature(self):
        """
        Creature comprend chaqu'une des creatures presentes sur le terrain
        """
        return self.creature

    def get_index(self):
        """
        Index permet de stocke des donnees indispensable pour que le terrain soit bien centre sur l'ecran
        """
        return self.index

    def get_grille(self):
        """
        Grille correspond a la grille de caractere representative du terrain
        """
        return self.grille

    def get_score(self):
        """
        Score permet d'arrêter le niveau ou bien le recommencer si besoin
        Tant que le score est a 0 le niveau continue, quand il est a 1 le niveau
        s'arrête et s'il est a 2 le niveau recommence
        """
        return self.score

    def get_reference_lemming(self):
        """
        Reference lemming permet de donner a chaque lemming une reference qui lui est propre
        """
        return self.reference_lemming

    def get_depart(self):
        """
        Depart correspond au coordonnees auquelles se situe Olimar
        """
        return self.depart

    def get_objectif(self):
        """
        Objectif correspond a l'objectif que l'on doit ramener au depart
        """
        return self.objectif

    def get_compteur(self):
        """
        Compteur permet le bon fonctionnement de certaines choses dans le jeu
        """
        return self.compteur

    def get_eaux(self):
        """
        Eaux comprend chaque source d'eau presente sur le terrain
        """
        return self.eaux

    def get_leviers(self):
        """
        Leviers comprend chaque levier present sur le terrain
        """
        return self.leviers

    def get_temps(self):
        """
        Temps permet de gerer la vitesse du jeu
        """
        return self.temps
    
    def get_mort(self):
        """
        Mort comprend chaque lemming mort
        """
        return self.mort

    def set_creature(self, nouveaux_creature):
        self.creature = nouveaux_creature

    def set_index(self, nouvelle_index):
        self.index = nouvelle_index

    def set_grille(self, ligne, colonne, symbole):
        self.grille[ligne][colonne] = symbole

    def set_score(self, nouveaux_score):
        self.score = nouveaux_score

    def set_reference_lemming(self, nouvelle_reference_lemming):
        self.reference_lemming = nouvelle_reference_lemming

    def set_depart(self, nouveau_depart):
        self.depart = nouveau_depart

    def set_objectif(self, nouvelle_objectif):
        self.objectif = nouvelle_objectif

    def set_compteur(self, nouveau_compteur):
        self.compteur = nouveau_compteur

    def set_eaux(self, nouvelles_eaux):
        self.eaux = nouvelles_eaux

    def set_leviers(self, nouveaux_leviers):
        self.leviers = nouveaux_leviers

    def set_temps(self, nouveau_temps):
        self.temps = nouveau_temps
        
    def set_mort(self, nouvelle_mort):
        self.mort = nouvelle_mort
        
    def initialisation(self):
        """
        Determine les coordonnees du depart et de l'objectif grâce au plan de depart
        """
        cpt_ligne = 0
        for ligne in self.get_grille():
            cpt_colonne = 0
            for colonne in ligne:
                if colonne.get_Terrain() == "I":
                    #"I" correspond au depart sur le plan
                    ligne_depart = cpt_ligne
                    colonne_depart = cpt_colonne
                    
                elif colonne.get_Terrain() == "O":
                    #"O" correspond a l'objectif sur le plan
                    ligne_objectif = cpt_ligne
                    colonne_objectif = cpt_colonne
                    
                cpt_colonne += 1
            cpt_ligne += 1
            
        #Recherche sur le plan de la case exact ou se situe l'objectif et le depart
        self.set_depart([ligne_depart, colonne_depart])
        objectif = Outil.Objectif(ligne_objectif, colonne_objectif)
        self.set_objectif(objectif)

    def avec_creature(self, ligne, colonne):
        """
        Verifie si une case donnee contient une creature
        La fonction renvoie True si la case contient une creature
        """
        rslt = False
        for crea in self.get_creature():
            if (crea.get_ligne(), crea.get_colonne()) == (ligne, colonne):
                rslt = True
        return rslt
    
    def actualisation(self):
        """
        Actualise tout ce qui n'est pas fait dans la classe jeu comme les leviers
        et l'eau
        """
        #On commence par l'actualisation des portes
        for levier in self.get_leviers():
            for porte in levier.get_portes():
                sens = porte.orientation() #sens permet de manipuler plus facilement les coordonnees des portes
                #On commence par supprimer toutes les anciennes portes
                for i in range(porte.get_etape()):
                    ligne = porte.get_ligne() + ((i + 1) * sens[0])
                    colonne = porte.get_colonne() + ((i + 1) * sens[1])
                    self.set_grille(ligne, colonne, Outil.Case(" "))
                #On fait ensuite fonctionnner le minuteur une fois
                if porte.get_minuteur() is not None and levier.get_mode() == "On":
                    porte.temps()
                #Puis on active fait bouger la porte en fonction des conditions
                porte.mouvement()
                sens = porte.orientation()
                #On passe maintenant a l'affichage des portes sur le plan
                for i in range(porte.get_etape()):
                    ligne = porte.get_ligne() + ((i + 1) * sens[0])
                    colonne = porte.get_colonne() + ((i + 1) * sens[1])
                    ligne_suivant = ligne + sens[0]
                    colonne_suivant = colonne + sens[1]
                    
                    #On cherche tout d'abord si une creature n'est pas la ou la porte veut s'afficher
                    if self.avec_creature(ligne, colonne):
                        #Si une creature est presente on cherche si la case ou la creature est cense aller est libre ou pas
                        if self.get_grille()[ligne_suivant][colonne_suivant].est_plein():
                            #Si elle n'est pas libre on fait mourir la creature
                            nouveaux_creature = []
                            for lem in self.get_creature():
                                if lem is not None:
                                    if lem.get_colonne() != colonne or lem.get_ligne() != ligne:
                                        nouveaux_creature.append(lem)
                                    else:
                                        if lem.get_forme() != "Monstre":
                                            transition = self.get_mort()
                                            transition.append(lem)
                                            self.set_mort(transition)
                                            test = pygame.mixer.Sound("Musique/Mort_Lemming.wav")
                                            test.set_volume(1)
                                            test.play()
                                        self.set_grille(lem.get_ligne(), lem.get_colonne(), Outil.Case(" "))
                                        self.afficher_terrain(lem.get_ligne() * 40, lem.get_colonne() * 40)
                            self.set_creature(nouveaux_creature)
                        else:
                            #Si elle est libre on fait monter la creature avec l'ascenseur
                            for lem in self.get_creature():
                                if lem.get_ligne() == ligne and lem.get_colonne() == colonne:
                                    lem.set_ligne(ligne_suivant)
                                    lem.set_colonne(colonne_suivant)
                                    lem.set_deplacement(f"Ascenseur{lem.get_deplacement()}")
                                    if lem.get_direction() == 1:
                                        self.set_grille(lem.get_ligne(), lem.get_colonne(), Outil.Case(">", lem))
                                    elif lem.get_direction() == -1:
                                        self.set_grille(lem.get_ligne(), lem.get_colonne(), Outil.Case("<", lem))
                                    objectif = self.get_objectif()
                                    #On cherche ensuite si la creature porte l'objectif
                                    if lem == objectif.get_porteur():
                                        #Si la creature porte l'objectif alors on cherche si l'objectif, lui, va arriver sur une case libre
                                        if self.get_grille()[ligne_suivant + sens[0]][colonne_suivant + sens[1]].est_plein():
                                            #S'il n'arrive pas sur une case libre, alors l'objectif se casse et le niveau recommence
                                            self.set_score(2)
                                        else:
                                            #Sinon il monte tout comme le lemming qui le porte
                                            objectif.set_ligne(objectif.get_ligne() + sens[0])
                                            objectif.set_ligne(objectif.get_ligne() + sens[1])
                                            objectif.set_deplacement("Ascenseur" + objectif.get_deplacement())
                     
                    #On regarde maintenant si l'objectif seul n'est la ou la porte veut s'afficher               
                    if self.get_grille()[ligne][colonne].get_Terrain() == "O":
                        #On regarde ensuite une nouvelle fois si la case ou l'objectif est cense arrive est vide
                        if self.get_grille()[ligne_suivant][colonne_suivant].est_plein():
                            self.set_score(2)
                        else:
                            objectif = self.get_objectif()
                            objectif.set_ligne(objectif.get_ligne() + sens[0])
                            objectif.set_ligne(objectif.get_ligne() + sens[1])
                            objectif.set_deplacement("Ascenseur" + objectif.get_deplacement())
                    #Et on fini ensuite par afficher la porte
                    self.set_grille(ligne, colonne, Outil.Case("C"))
                if levier.get_forme() == "Levier":
                    if levier.get_mode() == "On":
                        self.set_grille(levier.get_ligne(), levier.get_colonne(), Outil.Case("N"))
                    else:
                        self.set_grille(levier.get_ligne(), levier.get_colonne(), Outil.Case("F"))

                elif levier.get_forme() == "Bouton":
                    if levier.get_mode() == "On":
                        self.set_grille(levier.get_ligne(), levier.get_colonne(), Outil.Case("B"))
                    else:
                        self.set_grille(levier.get_ligne(), levier.get_colonne(), Outil.Case(" "))

        #On passe maintenant a l'actualisation de l'eau
        for eau in self.get_eaux():
            supp = []
            for zone in eau.get_prolongement():
                #On regarde si la case d'eau que l'on veut afficher est vide
                if self.grille[zone[0]][zone[1]].est_libre():
                    #Si c'est le cas alors on affiche l'eau sur la case
                    self.set_grille(zone[0], zone[1], Outil.Case('E'))
                elif self.get_grille()[zone[0]][zone[1]].est_plein():
                    #Si un bloc est deja present alors on coupe la source d'eau
                    obstacle = self.get_grille()[zone[0]][zone[1]]
                    transition = []
                    #On affiche donc toute les cases d'eaux qui reste
                    for zone_2 in eau.get_prolongement():
                        if zone_2[2] <= zone[2]:
                            transition.append(zone_2)
                        else:
                            supp.append(zone_2)
                    eau.set_prolongement(transition)
                    
            #Et on supprime toutes les cases d'eaux qui disparaissent
            for zone in supp:
                if obstacle == zone:
                    self.set_grille(zone[0], zone[1], obstacle)
                else:
                    self.get_grille()[zone[0]][zone[1]].liberer()
                    self.afficher_terrain(zone[0] * 40, zone[1] * 40)

        #On affiche enfin le depart ainsi que l'objectif
        self.set_grille(self.get_depart()[0], self.get_depart()[1], Outil.Case('I'))

        self.set_grille(self.get_objectif().get_ligne(), self.get_objectif().get_colonne(), Outil.Case('O'))
    
    def cpt_mort(self, nombre):
        chiffre = pygame.image.load("Sprite/Fond/Fond_Compteur_Mort.png").convert()
        screen.blit(chiffre, (1280, 0))
        for indice in range(len(nombre)):
            chiffre = pygame.image.load(f"Sprite/Fond/{nombre[indice]}.png").convert_alpha()
            screen.blit(chiffre, (1495 - ((len(nombre) - indice) * 70), 0))
        mort = pygame.image.load("Sprite/Fond/Tete_de_mort.png").convert_alpha()
        screen.blit(mort, (1495, 0))

    def animer(self):
        """
        Affiche un tour de jeu de maniere fluide
        """
        #On commence tout d'abord par actualiser tout ce qui n'a pas encore bouge pendant le tour
        self.actualisation()
        self.cpt_mort(str(self.get_mort()[0] + len(self.get_mort()) - 1))
        for i in range(20):
            #On va ensuite faire apparaître les images qui bougent frames par frames
            self.frame(i)
            sleep(self.get_temps())

    def test_vide(self, liste, ligne, colonne):
        """
        Test si la case donnee est deja dans la liste elle aussi donnee
        Si la case est deja dans la liste alors la fonction renvoie True.
        Sinon elle renvoie les coordonnees de la case
        """
        test = None
        for case in liste:
            if (ligne, colonne) == (case[0], case[1]):
                test = True
        if test == None:
            test = [ligne, colonne]
        return test

    def case_vide(self, liste, ligne, colonne):
        """
        Affiche, ou non, une case vide a l'emplacement donne.
        La case vide est affichee uniquement si les coordonnees donnees ne sont pas dans la liste donnee
        """
        #On test d'abord si les coordonnees sont dans la liste
        test = self.test_vide(liste, ligne, colonne)
        if test is not True:
            #Si les coordonnees n'y sont pas alors on affiche la case vide et on ajoute les coordonnees a la liste
            liste.append(test)
            self.afficher_terrain(ligne, colonne)
        #On renvoie enfin la liste qu'elle soit modifiee ou pas
        return liste

    def test_eau(self, zone, eau, stade, etape):
        """
        Determine quelle image d'eau il faut utiliser
        La forme de l'eau n'est pas la même selon son emplacement est cette fonction
        se charge de savoir quelle forme il faut utiliser pour la zone donne
        """
        #On regarde tout d'abord si la zone est a la même hauteur que le source de l'eau
        if zone[0] == eau.get_source()[0]:
            #On regarde ensuite si la zone a du vide en dessous d'elle ou pas
            if self.grille[zone[0] + 1][zone[1]].est_plein() is not True:
                #On regarde enfin si zone est a gauche, a droite ou sur la source
                if zone[1] == eau.get_source()[1]:
                    self.afficher_eau(zone[0] * 40, zone[1] * 40, stade, 5, etape)
                elif zone[1] > eau.get_source()[1]:
                    self.afficher_eau(zone[0] * 40, zone[1] * 40, stade, 3, etape)
                elif zone[1] < eau.get_source()[1]:
                    self.afficher_eau(zone[0] * 40, zone[1] * 40, stade, 4, etape)
            else:
                if zone[1] > eau.get_source()[1]:
                    self.afficher_eau(zone[0] * 40, zone[1] * 40, stade, 1, etape)
                elif zone[1] < eau.get_source()[1]:
                    self.afficher_eau(zone[0] * 40, zone[1] * 40, stade, 2, etape)
                else:
                    self.afficher_eau(zone[0] * 40, zone[1] * 40, stade, 1, etape)
        else:
            self.afficher_eau(zone[0] * 40, zone[1] * 40, stade, 5, etape)

    def frame(self, etape):
        """
        Permet d'afficher toute les choses mobiles pendant une frame
        """
        vide = []
        #On commence par afficher l'eau
        for eau in self.get_eaux():
            for zone in eau.get_prolongement():
                #On elimine d'abord les cases d'eaux des cases pouvant être vide
                vide.append([zone[0] * 40, zone[1] * 40])
                #On verifie une derniere foi si la case doit bien s'afficher
                if self.grille[zone[0]][zone[1]].get_Terrain() == "E":
                    #On regarde ensuite si la case vient d'apparaître, auquel cas il faut l'animer et non pas juste l'afficher
                    if zone[2] == eau.get_DernierStade():
                        stade = "Animer"
                    else:
                        stade = "Statique"
                    #On affiche ensuite la case
                    self.test_eau(zone, eau, stade, etape)

        #On passe ensuite aux creatures
        for lem in self.get_creature():
            hauteur_supp = 0
            ascenseur = 0
            #On determine la direction dans laquelle ils regardent
            if lem.get_direction() == 1:
                direction = "Droite"
            else:
                direction = "Gauche"
            #On verifie ensuite s'ils sont sur un ascenseur
            if lem.get_deplacement() == "AscenseurAvancer":
                #Et on modifie la hauteur a laquelle va être afficher la creature
                hauteur_supp = -40 + (etape * 2) + 2
                lem.set_deplacement("Avancer")
                ascenseur = 1
            elif lem.get_deplacement() == "AscenseurRetour":
                hauteur_supp = -40 + (etape * 2) + 2
                lem.set_deplacement("Retour")
                ascenseur = 1

            #On choisi ensuite quelle image faut afficher en fonction des coordonnees de la creature, de son action, de sa forme et de la frame a laquelle l'image s'affiche
            if lem.get_deplacement() == "Monter":
                #On commemence par rendre la ou les case vide
                vide = self.case_vide(vide, lem.get_ligne() * 40, lem.get_colonne() * 40)
                vide = self.case_vide(vide, (lem.get_ligne() + 1) * 40, lem.get_colonne() * 40)
                #Et on affiche la creature
                self.afficher_lemming_monte(lem.get_ligne() * 40 - hauteur_supp , lem.get_colonne() * 40, direction, lem.get_forme(), etape)

            elif lem.get_deplacement() == "Avancer":
                vide = self.case_vide(vide, lem.get_ligne() * 40, lem.get_colonne() * 40)
                vide = self.case_vide(vide, lem.get_ligne() * 40, (lem.get_colonne() - lem.get_direction()) * 40)
                if ascenseur == 1:
                    vide = self.case_vide(vide, (lem.get_ligne() + 1) * 40, lem.get_colonne() * 40)
                    vide = self.case_vide(vide, (lem.get_ligne() + 1) * 40, (lem.get_colonne() - lem.get_direction()) * 40)
                self.afficher_lemming_avance(lem.get_ligne() * 40 - hauteur_supp, lem.get_colonne() * 40, direction, lem.get_forme(), etape)

            elif lem.get_deplacement() == "AvancerEau":
                #Pour les mouvements on doit d'abord afficher la case d'eau et ensuite la creature
                for eau in self.get_eaux():
                    for zone in eau.get_prolongement():
                        if zone[0] == lem.get_ligne() and zone[1] == lem.get_colonne():
                            bonne_eau = eau
                self.test_eau([lem.get_ligne(), lem.get_colonne()], bonne_eau, "Statique", etape)
                vide = self.case_vide(vide, lem.get_ligne() * 40, (lem.get_colonne() - lem.get_direction()) * 40)
                self.afficher_lemming_avance(lem.get_ligne() * 40 - hauteur_supp, lem.get_colonne() * 40, direction, lem.get_forme(), etape)

            elif lem.get_deplacement() == "Retour":
                vide = self.case_vide(vide, lem.get_ligne() * 40, lem.get_colonne() * 40)
                if ascenseur == 1:
                    vide = self.case_vide(vide, (lem.get_ligne() + 1) * 40, lem.get_colonne() * 40)
                self.afficher_lemming_retour(lem.get_ligne() * 40 - hauteur_supp, lem.get_colonne() * 40, direction, lem.get_forme(), etape)

            elif lem.get_deplacement() == "RetourEau":
                for eau in self.get_eaux():
                    for zone in eau.get_prolongement():
                        if zone[0] == lem.get_ligne() and zone[1] == lem.get_colonne():
                            bonne_eau = eau
                self.test_eau([lem.get_ligne(), lem.get_colonne()], bonne_eau, "Statique", etape)
                self.afficher_lemming_retour(lem.get_ligne() * 40 - hauteur_supp, lem.get_colonne() * 40, direction, lem.get_forme(), etape)

            elif lem.get_deplacement() == "Tomber":
                vide = self.case_vide(vide, lem.get_ligne() * 40, lem.get_colonne() * 40)
                vide = self.case_vide(vide, (lem.get_ligne() - 1) * 40, lem.get_colonne() * 40)
                self.afficher_lemming_tombe(lem.get_ligne() * 40 - hauteur_supp, lem.get_colonne() * 40, direction, lem.get_forme(), etape)

            elif lem.get_deplacement() == "TomberEau":
                for eau in self.get_eaux():
                    for zone in eau.get_prolongement():
                        if zone[0] == lem.get_ligne() and zone[1] == lem.get_colonne():
                            bonne_eau = eau
                self.test_eau([lem.get_ligne(), lem.get_colonne()], bonne_eau, "Statique", etape)
                vide = self.case_vide(vide, (lem.get_ligne() - 1) * 40, lem.get_colonne() * 40)
                self.afficher_lemming_tombe(lem.get_ligne() * 40 - hauteur_supp, lem.get_colonne() * 40, direction, lem.get_forme(), etape)

            elif lem.get_deplacement() == "Statique":
                vide = self.case_vide(vide, lem.get_ligne() * 40, lem.get_colonne() * 40)
                self.afficher_lemming(lem.get_ligne() * 40 - hauteur_supp, lem.get_colonne() * 40, direction, lem.get_forme())

            elif lem.get_deplacement() == "Creuser":
                #Quand le lemming sol creuse, le bloc de terre se modifie en consequence
                vide = self.case_vide(vide, lem.get_ligne() * 40, lem.get_colonne() * 40)
                vide = self.case_vide(vide, lem.get_ligne() * 40, (lem.get_colonne() - lem.get_direction()) * 40)
                self.creuser(lem.get_ligne() * 40 , lem.get_colonne() * 40 - hauteur_supp, direction, etape)
                self.afficher_lemming_avance(lem.get_ligne() * 40 - hauteur_supp, lem.get_colonne() * 40, direction, lem.get_forme(), etape)

            if ascenseur == 1:
                lem.set_deplacement(f"Ascenseur{lem.get_deplacement()}")

        
        #On fait ensuite exactement la même chose avec l'objectif
        objectif = self.get_objectif()
        direction = "Gauche"
        if objectif.get_porteur() is not None:
            if objectif.get_porteur().get_direction() == 1:
                direction = "Droite"
        
        ascenseur = 0
        hauteur_supp = 0
        if objectif.get_deplacement() == "AscenseurAvancer":
            hauteur_supp = -40 + (etape * 2) + 2
            objectif.set_deplacement("Avancer")
            ascenseur = 1
        elif objectif.get_deplacement() == "AscenseurStatique":
            hauteur_supp = -40 + (etape * 2) + 2
            objectif.set_deplacement("Statique")
            ascenseur = 1
        mvt_objectif = objectif.get_deplacement()
            
        if mvt_objectif == "Monter":
            vide = self.case_vide(vide, objectif.get_ligne() * 40, objectif.get_colonne() * 40)
            vide = self.case_vide(vide, (objectif.get_ligne() + 1) * 40, objectif.get_colonne() * 40)
            self.afficher_lemming_monte(objectif.get_ligne() * 40, objectif.get_colonne() * 40, direction, "Objectif", etape)
        
        elif mvt_objectif == "Tomber":
            vide = self.case_vide(vide, objectif.get_ligne() * 40, objectif.get_colonne() * 40)
            vide = self.case_vide(vide, (objectif.get_ligne() - 1) * 40, objectif.get_colonne() * 40)
            self.afficher_lemming_tombe(objectif.get_ligne() * 40, objectif.get_colonne() * 40, direction, "Objectif", etape)
        
        elif mvt_objectif == "Avancer":
            vide = self.case_vide(vide, objectif.get_ligne() * 40, objectif.get_colonne() * 40)
            vide = self.case_vide(vide, objectif.get_ligne() * 40, (objectif.get_colonne() - objectif.get_porteur().get_direction()) * 40)
            if ascenseur == 1:
                vide = self.case_vide(vide, (objectif.get_ligne() + 1) * 40, objectif.get_colonne() * 40)
                vide = self.case_vide(vide, (objectif.get_ligne() + 1) * 40, (objectif.get_colonne() - objectif.get_porteur().get_direction()) * 40)
            self.afficher_lemming_avance(objectif.get_ligne() * 40 - hauteur_supp, objectif.get_colonne() * 40, direction, "Objectif", etape)
        
        elif mvt_objectif == "Statique":
            vide = self.case_vide(vide, objectif.get_ligne() * 40, objectif.get_colonne() * 40)
            if ascenseur == 1:
                vide = self.case_vide(vide, (objectif.get_ligne() + 1) * 40, objectif.get_colonne() * 40)
            self.afficher_objectif(objectif.get_ligne() * 40 - hauteur_supp, objectif.get_colonne() * 40)
        
        if ascenseur == 1:
            objectif.set_deplacement(f"Ascenseur{objectif.get_deplacement()}")
            
        
        #On s'occupe ensuite des portes et des leviers
        for levier in self.get_leviers():
            #On s'occupe d'abord des leviers qu'on differement en fonction de sa forme et de son etat actuel
            if etape == 0:
                if levier.get_mode() == "Off":
                    if levier.get_forme() == "Levier":
                        self.afficher_levier_off(levier.get_ligne() * 40, levier.get_colonne() * 40)
                    else:
                        self.afficher_terrain(levier.get_ligne() * 40, levier.get_colonne() * 40)
                else:
                    if levier.get_forme() == "Levier":
                        self.afficher_levier_on(levier.get_ligne() * 40, levier.get_colonne() * 40)
                    else:
                        self.afficher_bouton(levier.get_ligne() * 40, levier.get_colonne() * 40)

            #On passe ensuite aux portes
            for porte in levier.get_portes():
                #On va simplement afficher chaque bloc en fonction du deplacement de la porte, de la place du bloc dans la porte et de la frame active
                if porte.get_deplacement() == "Avancer":
                    sens = porte.orientation()
                    for i in range(porte.get_etape()):
                        if i == 0:
                            place = "Premier"
                        else:
                            place = "Suivant"
                        ligne = porte.get_ligne() + ((i + 1) * sens[0])
                        colonne = porte.get_colonne() + ((i + 1) * sens[1])
                        self.afficher_porte_avance(ligne * 40, colonne * 40, porte.get_direction(), sens, place, etape)
                elif porte.get_deplacement() == "Reculer":
                    sens = porte.orientation()
                    for i in range(porte.get_etape() + 1):
                        ligne = porte.get_ligne() + ((i + 1) * sens[0])
                        colonne = porte.get_colonne() + ((i + 1) * sens[1])
                        vide = self.case_vide(vide, ligne * 40, colonne * 40)
                        if i == 0:
                            place = "Premier"
                        elif i == porte.get_etape() - 1:
                            place = "Dernier"
                        else:
                            place = "Suivant"
                        self.afficher_porte_recule(ligne * 40, colonne * 40, porte.get_direction(), sens, place, etape)

        pygame.display.flip()

    def afficher(self):
        """
        Affiche tout se qui ne bouge pas en se basant sur le plan du terrain
        """
        affichage = self.get_grille()
        cpt_ligne = 0
        for ligne in affichage:
            cpt_colonne = 0
            for colonne in ligne:
                bloc = str(colonne)
                if bloc == "#":
                    self.afficher_mur(cpt_ligne, cpt_colonne)
                elif bloc == " ":
                    self.afficher_terrain(cpt_ligne, cpt_colonne)
                elif bloc == "T":
                    self.afficher_terre(cpt_ligne, cpt_colonne, 0)
                elif bloc == "P":
                    self.afficher_pierre(cpt_ligne, cpt_colonne)
                elif bloc == "I":
                    self.afficher_olimar(cpt_ligne, cpt_colonne)
                cpt_colonne += 40
            cpt_ligne += 40

        for levier in self.get_leviers():
            for porte in levier.get_portes():
                sens = porte.orientation()
                for i in range(porte.get_etape()):
                    ligne = porte.get_ligne() + ((i + 1) * sens[0])
                    colonne = porte.get_colonne() + ((i + 1) * sens[1])
                    self.afficher_porte(ligne * 40, colonne * 40, porte.get_direction())

        pygame.display.flip()

    def afficher_mur(self, ligne, colonne):
        """
        Affiche un mur aux coordonnees donnees
        """
        fond = pygame.image.load("Sprite/BlocPierre.png").convert()
        screen.blit(fond, (colonne + self.get_index()[0], ligne + self.get_index()[1]))

    def afficher_terrain(self, ligne, colonne):
        """
        Affiche une case vide aux coordonnees donnees
        """
        fond = pygame.image.load("Sprite/Terrain1.png").convert()
        screen.blit(fond, (colonne + self.get_index()[0], ligne + self.get_index()[1]))

    def afficher_pierre(self, ligne, colonne):
        """
        Affiche un bloc de pierre escaladable aux coordonnees donnees
        """
        fond = pygame.image.load("Sprite/BlocGravier.png").convert_alpha()
        screen.blit(fond, (colonne + self.get_index()[0], ligne + self.get_index()[1]))

    def placer_grille(self, ligne, colonne, lemming):
        """
        Affiche la creature ou l'objectif donne sur le plan du terrain
        """
        if lemming == "Monstre":
            self.set_grille(ligne, colonne, Outil.Case("M"))
        elif lemming == "Objectif":
            self.set_grille(ligne, colonne, Outil.Case("O"))
        else:
            self.set_grille(ligne, colonne, Outil.Case(">", Outil.Creature(lemming, ligne, colonne, 1, 1)))

    def afficher_lemming(self, ligne, colonne, sens, lemming):
        """
        Affiche un lemming imobile aux coordonnees donnees
        """
        fond = pygame.image.load(f"Sprite/{lemming}/{sens}/Statique.png").convert_alpha()
        screen.blit(fond, (colonne + self.get_index()[0], ligne + self.get_index()[1]))
        self.placer_grille(int(ligne/40), int(colonne/40), lemming)

    def afficher_lemming_avance(self, ligne, colonne, sens, lemming, etape):
        """
        Affiche un lemming qui avance aux coordonnees donnees
        """
        if sens == "Droite":
            decalage = -40
        else:
            decalage = 40
        if lemming == "Aile":
            limite = 13
        elif lemming == "Combat":
            limite = 15
        elif lemming == "Monstre":
            limite = 17
        elif lemming == "Eau" or lemming == "Jump":
            limite = 13
        elif lemming == "Sol":
            limite = 14
        elif lemming == "Objectif":
            limite = 18
        if etape >= 1:
            fond = pygame.image.load(f"Sprite/{lemming}/{sens}/Avancer/Arrive{etape}.png").convert_alpha()
            screen.blit(fond, (colonne + self.get_index()[0], ligne + self.get_index()[1]))
        if etape <= limite:
            fond2 = pygame.image.load(f"Sprite/{lemming}/{sens}/Avancer/Depart{etape}.png").convert_alpha()
            screen.blit(fond2, (colonne + self.get_index()[0] + decalage, ligne + self.get_index()[1]))
        self.placer_grille(int(ligne/40), int(colonne/40), lemming)

    def afficher_lemming_monte(self, ligne, colonne, sens, lemming, etape):
        """
        Affiche un lemming qui monte aux coordonnees donnees
        """
        if etape >= 1:
            fond = pygame.image.load(f"Sprite/{lemming}/{sens}/Monter/Arrive{etape}.png").convert_alpha()
            screen.blit(fond, (colonne + self.get_index()[0], ligne + self.get_index()[1]))
        if etape <= 15 and lemming == "Aile":
            fond2 = pygame.image.load(f"Sprite/{lemming}/{sens}/Monter/Depart{etape}.png").convert_alpha()
            screen.blit(fond2, (colonne + self.get_index()[0], ligne + self.get_index()[1] + 40))
        elif etape <= 18 and lemming != "Aile":
            fond2 = pygame.image.load(f"Sprite/{lemming}/{sens}/Monter/Depart{etape}.png").convert_alpha()
            screen.blit(fond2, (colonne + self.get_index()[0], ligne + self.get_index()[1] + 40))
        self.placer_grille(int(ligne/40), int(colonne/40), lemming)

    def afficher_lemming_retour(self, ligne, colonne, sens, lemming, etape):
        """
        Affiche un lemming qui fait demi tour aux coordonnees donnees
        """
        if sens == "Droite":
            sens = "Gauche"
        else:
            sens = "Droite"
        if lemming == "Aile":
            limite = 12
        elif lemming == "Combat":
            limite = 15
        elif lemming == "Monstre":
            limite = 16
        elif lemming == "Eau" or lemming == "Jump" or lemming == "Sol":
            limite = 13
        if etape <= limite:
            fond = pygame.image.load(f"Sprite/{lemming}/{sens}/Retour/Depart1.png").convert_alpha()
            screen.blit(fond, (colonne + self.get_index()[0], ligne + self.get_index()[1]))
        else:
            fond2 = pygame.image.load(f"Sprite/{lemming}/{sens}/Retour/Depart{etape - limite}.png").convert_alpha()
            screen.blit(fond2, (colonne + self.get_index()[0], ligne + self.get_index()[1]))
        self.placer_grille(int(ligne/40), int(colonne/40), lemming)

    def afficher_lemming_tombe(self, ligne, colonne, sens, lemming, etape):
        """
        Affiche un lemming qui tombe aux coordonnees donnees
        """
        if etape >= 1:
            fond = pygame.image.load(f"Sprite/{lemming}/{sens}/Tomber/Arrive{etape}.png").convert_alpha()
            screen.blit(fond, (colonne + self.get_index()[0], ligne + self.get_index()[1]))
        if etape <= 18:
            fond2 = pygame.image.load(f"Sprite/{lemming}/{sens}/Tomber/Depart{etape}.png").convert_alpha()
            screen.blit(fond2, (colonne + self.get_index()[0], ligne + self.get_index()[1] - 40))
        self.placer_grille(int(ligne/40), int(colonne/40), lemming)

    def afficher_eau(self, ligne, colonne, stade, forme, etape):
        """
        Affiche un bloc d'eau aux coordonnees donnees
        """
        if stade == "Statique":
            self.afficher_terrain(ligne, colonne)
            fond = pygame.image.load(f"Sprite/BlocEau/Bloc{forme}/Depart19.png").convert_alpha()
            screen.blit(fond, (colonne + self.get_index()[0], ligne + self.get_index()[1]))
        elif stade == "Animer":
            fond2 = pygame.image.load(f"Sprite/BlocEau/Bloc{forme}/Depart{etape}.png").convert_alpha()
            screen.blit(fond2, (colonne + self.get_index()[0], ligne + self.get_index()[1]))
        self.set_grille(int(ligne/40), int(colonne/40), Outil.Case("E"))

    def creuser(self, ligne, colonne, sens, etape):
        """
        Affiche un bloc de terre qui se fait creuser aux coordonnees donnees
        """
        if sens == "Droite":
            sens = "Gauche"
        else:
            sens = "Droite"
        fond = pygame.image.load(f"Sprite/BlocSol/{sens}/BlocSol{etape}.png").convert_alpha()
        screen.blit(fond, (colonne + self.get_index()[0], ligne + self.get_index()[1]))

    def afficher_terre(self, ligne, colonne, etape):
        """
        Affiche un bloc de terre aux coordonnees donnees
        """
        self.afficher_terrain(ligne, colonne)
        fond = pygame.image.load(f"Sprite/BlocSol/Droite/BlocSol{etape}.png").convert_alpha()
        screen.blit(fond, (colonne + self.get_index()[0], ligne + self.get_index()[1]))

    def afficher_bouton(self, ligne, colonne):
        """
        Affiche un bouton aux coordonnees donnees
        """
        self.afficher_terrain(ligne, colonne)
        fond = pygame.image.load("Sprite/Bouton.png").convert_alpha()
        screen.blit(fond, (colonne + self.get_index()[0], ligne + self.get_index()[1]))

    def afficher_levier_on(self, ligne, colonne):
        """
        Affiche un levier en mode on aux coordonnees donnees
        """
        self.afficher_terrain(ligne, colonne)
        fond = pygame.image.load("Sprite/LevierOn.png").convert_alpha()
        screen.blit(fond, (colonne + self.get_index()[0], ligne + self.get_index()[1]))

    def afficher_levier_off(self, ligne, colonne):
        """
        Affiche un levier en mode off aux coordonnees donnees
        """
        self.afficher_terrain(ligne, colonne)
        fond = pygame.image.load("Sprite/LevierOff.png").convert_alpha()
        screen.blit(fond, (colonne + self.get_index()[0], ligne + self.get_index()[1]))

    def afficher_porte(self, ligne, colonne, direction):
        """
        Affiche une porte imobile aux coordonnees donnees
        """
        self.afficher_terrain(ligne, colonne)
        fond = pygame.image.load(f"Sprite/Porte/{direction}/Depart0.png").convert_alpha()
        screen.blit(fond, (colonne + self.get_index()[0], ligne + self.get_index()[1]))

    def afficher_porte_avance(self, ligne, colonne, direction, sens, place, etape):
        """
        Affiche une porte qui avance aux coordonnees donnees
        """
        fond = pygame.image.load(f"Sprite/Porte/{direction}/Arrive{etape + 1}.png").convert_alpha()
        screen.blit(fond, (colonne + self.get_index()[0], ligne + self.get_index()[1]))
        if place == "Suivant" and etape <= 18:
            fond2 = pygame.image.load(f"Sprite/Porte/{direction}/Depart{etape + 1}.png").convert_alpha()
            screen.blit(fond2, (colonne + self.get_index()[0] - 40 * sens[1], ligne + self.get_index()[1] - 40 * sens[0]))

    def afficher_porte_recule(self, ligne, colonne, direction, sens, place, etape):
        """
        Affiche une porte qui recule aux coordonnees donnees
        """
        fond = pygame.image.load(f"Sprite/Porte/{direction}/Arrive{19 - etape}.png").convert_alpha()
        screen.blit(fond, (colonne + self.get_index()[0], ligne + self.get_index()[1]))
        if place != "Premier":
            fond2 = pygame.image.load(f"Sprite/Porte/{direction}/Depart{19 - etape}.png").convert_alpha()
            screen.blit(fond2, (colonne + self.get_index()[0] - 40 * sens[1], ligne + self.get_index()[1] - 40 * sens[0]))

    def afficher_objectif(self, ligne, colonne):
        """
        Affiche l'objectif aux coordonnees donnees
        """
        fond = pygame.image.load("Sprite/Objectif/Droite/Statique.png").convert_alpha()
        screen.blit(fond, (colonne + self.get_index()[0], ligne + self.get_index()[1]))

    def afficher_olimar(self, ligne, colonne):
        """
        Affiche le depart aux coordonnees donnees
        """
        self.afficher_terrain(ligne - 40, colonne)
        self.afficher_terrain(ligne, colonne)
        fond = pygame.image.load("Sprite/Olimar.gif").convert()
        screen.blit(fond, (colonne + self.get_index()[0], ligne + self.get_index()[1] - 40))
