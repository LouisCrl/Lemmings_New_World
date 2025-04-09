#Cette page gere les niveaux et chaque tour pendant le niveau

import pygame
#La bibliotheque pygame sert a affichage le jeu
from time import *
#La bibliotheque time permet de faire des moments de pause
import Outil as Outil
#Cela sert a recuperer toutes les classes secondaires dont on aura besoin ici
import Affichage as Affichage
#Cela sert a recuperer la classe affichage qui permettra d'afficher le jeu qu'on fait tourner dans cette page

pygame.init()
size = width, height = 1600, 820
screen = pygame.display.set_mode(size)
#Creation d'une fenetre d'une taille de 1600 pixels sur 820 pixels

class Jeu:
    def __init__(self, grille_texte, creature, eaux, leviers, cpt_mort, niveaux):
        self.grille = []
        with open(grille_texte, 'r') as fichier:
            for ligne in fichier:
                Ligne = []
                for colonne in ligne:
                    c = Outil.Case(colonne)
                    Ligne.append(c)
                self.grille.append(Ligne)

        self.set_creature(creature)
        self.set_index(0)
        self.set_score(0)
        self.set_reference_lemming(len(creature))
        self.set_depart(0)
        self.set_objectif(0)
        self.set_compteur(None)
        self.set_eaux(eaux)
        self.set_leviers(leviers)
        self.set_temps(0.01)
        self.set_mort([cpt_mort])
        self.set_niveaux(niveaux)
    """
    Une classe qui lance un niveau et qui gere tout ce qu'il se passe pendant le niveau
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
        Score permet d'arreter le niveau ou bien le recommencer si besoin
        Tant que le score est a 0 le niveau continue, quand il est a 1 le niveau
        s'arrete et s'il est a 2 le niveau recommence
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
    
    def get_niveaux(self):
        return self.niveaux

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

    def set_mort(self, nouveau_mort):
        self.mort = nouveau_mort
        
    def set_niveaux(self, nouveaux_niveaux):
        self.niveaux = nouveaux_niveaux

    def info(self, nvx):
        """
        Permet de recuperer toutes les modifications qui ont eu lieu pendant l'affichage
        """
        self.set_creature(nvx.get_creature())
        self.set_index(nvx.get_index())
        self.grille = []
        for ligne in nvx.get_grille():
            Ligne = []
            for colonne in ligne:
                Ligne.append(colonne)
            self.grille.append(Ligne)
        self.set_score(nvx.get_score())
        self.set_reference_lemming(nvx.get_reference_lemming())
        self.set_depart(nvx.get_depart())
        self.set_objectif(nvx.get_objectif())
        self.set_compteur(nvx.get_compteur())
        self.set_eaux(nvx.get_eaux())
        self.set_leviers(nvx.get_leviers())
        self.set_temps(nvx.get_temps())

    def creation_affichage(self):
        """
        Permet de creer une classe Affichage qui va avoir les meme caracteristique que cette classe jeu
        """
        grille = self.get_grille()
        index = self.get_index()
        score = self.get_score()
        creature = self.get_creature()
        depart = self.get_depart()
        objectif = self.get_objectif()
        eaux = self.get_eaux()
        leviers = self.get_leviers()
        temps = self.get_temps()
        compteur = self.get_compteur()
        mort = self.get_mort()
        Creation = Affichage.Affichage(grille, index, score, creature, depart, objectif, eaux, leviers, temps, compteur, mort)
        return Creation

    def mourir(self, ligne, colonne):
        """
        Fait mourir la creature presente aux coordonnees donnees
        """
        cible = None
        nouveaux_creature = []
        #On identifie d'abord le lemming mort puis on le supprime des creatures presentes sur le terrain
        for lems in self.get_creature():
            if lems is not None:
                if lems.get_colonne() != colonne or lems.get_ligne() != ligne:
                    nouveaux_creature.append(lems)
                else:
                    cible = lems
                    if cible.get_forme() != "Monstre":
                        transition = self.get_mort()
                        transition.append(cible)
                        self.set_mort(transition)
        #On envoie ensuite le cri de mort des lemmings
        if cible.get_forme() != "Monstre":
            test = pygame.mixer.Sound("Musique/Mort_Lemming.wav")
            test.set_volume(1)
            test.play()
        self.set_creature(nouveaux_creature)
        return cible

    def tour(self):
        """
        Fait passer un tour de jeu
        """
        self.set_compteur(1)
        #On commence par faire passer un tour a l'eau
        for eau in self.get_eaux():
            #Pour commence on identifie a quel est le dernier stade utilise dans le cours d'eau
            stade_max = 0
            for zone in eau.get_prolongement():
                if zone[2] > stade_max:
                    stade_max = zone[2]
            nvx_stade_max = stade_max + 1
            #On va ensuite identifier ou l'eau va s'etendre en regardant les zones ou l'eau est deja presente, une par une
            source_provisoire = []
            for zone in eau.get_prolongement():
                sol = self.get_grille()[zone[0] + 1][zone[1]]
                place = self.get_grille()[zone[0]][zone[1]].get_Terrain()
                #On verifie tout d'abord si la case qu'on regarde est belle est bien une case d'eau
                if place == "E":
                    #On verifie ensuite si la case est a la meme hauteur de la source et qu'elle a bien un bloc complet en dessous d'elle
                    if zone[0] == eau.get_source()[0] and sol.est_plein():
                        #Si c'est le cas on regarde alors si la case de droite est libre
                        zone_test = self.grille[zone[0]][zone[1] + 1]
                        if zone_test.est_libre() is True:
                            #Si elle est libre alors la case de droite devient une case rempli d'eau
                            source_provisoire.append([zone[0], zone[1] + 1, nvx_stade_max])

                        #Si elle n'est pas libre on regarde si sur cette case il n'y a pas simplement des creatures qui ne sont pas des lemmings eaux
                        elif zone_test.get_creature() is not None and zone_test.get_creature().get_forme() != "Eau":
                            #Si c'est le cas alors la case de droite devient une case rempli d'eau et la creature presente meurt
                            source_provisoire.append([zone[0], zone[1] + 1, nvx_stade_max])
                            self.mourir(zone[1] + 1, zone[0])

                        #On fait ensuite la meme chose a gauche
                        zone_test = self.grille[zone[0]][zone[1] - 1]
                        if zone_test.est_libre() is True:
                            source_provisoire.append([zone[0], zone[1] - 1, nvx_stade_max])

                        elif zone_test.get_creature() is not None and zone_test.get_creature().get_forme() != "Eau":
                            source_provisoire.append([zone[0], zone[1] - 1, nvx_stade_max])
                            self.mourir(zone[1] - 1, zone[0])
                    
                    #Si la case qu'on regarde n'est pas a la meme hauteur que la source ou alors qu'en dessous d'elle il n'y a pas de bloc plein
                    #alors on regarde si en dessous d'elle il y a une case vide et on fait la meme chose que juste au dessus
                    zone_test = self.grille[zone[0] + 1][zone[1]]
                    if zone_test.est_libre() is True:
                        source_provisoire.append([zone[0] + 1, zone[1], nvx_stade_max])

                    elif zone_test.get_creature() is not None and zone_test.get_creature().get_forme() != "Eau":
                        source_provisoire.append([zone[0] + 1, zone[1], nvx_stade_max])
                        self.mourir(zone[1], zone[0] + 1)
            
            #On va ensuite modifie le plan pour y ajouter toutes les nouvelles cases
            for zone in source_provisoire:
                eau.etendre(zone)
            if source_provisoire == []:
                eau.set_DernierStade(None)


        #On passe donc aux creatures
        for lem in self.get_creature():
            if lem is not None:
                #On commmence par etablir plusieurs raccourci pour les cases autour du lemmin
                position = self.grille[lem.get_ligne()][lem.get_colonne()]
                dessus = self.grille[lem.get_ligne() - 1][lem.get_colonne()]
                dessous = self.grille[lem.get_ligne() + 1][lem.get_colonne()]
                devant = self.grille[lem.get_ligne()][lem.get_colonne() + lem.get_direction()]
                devant_haut = self.grille[lem.get_ligne() - 1][lem.get_colonne() + lem.get_direction()]
                devant_bas = self.grille[lem.get_ligne() + 1][lem.get_colonne() + lem.get_direction()]
                #On va ensuite s'interesse aux monstres
                if lem.get_forme() == "Monstre":
                    #Tout d'abord on cree les trois zones ou le monstre peut manger des lemmings
                    cible = "En cours"
                    vision1 = None
                    vision2 = None
                    vision3 = None
                    if dessus.get_creature() is not None:
                        vision1 = dessus.get_creature().get_forme()
                        vision = vision1
                    elif devant.get_creature() is not None:
                        vision2 = devant.get_creature().get_forme()
                        vision = vision2
                    elif dessous.get_creature() is not None:
                        vision3 = dessous.get_creature().get_forme()
                        vision = vision3
                    else:
                        cible = "Aucun"
                    
                    #On regarde ensuite dans lesquels des ses zones il y a reellement des lemmings
                    if cible == "En cours" and vision != "Monstre":
                        suivant = None
                        if vision1 != "Combat" and vision1 is not None:
                            ligne_suivant = lem.get_ligne() - 1
                            colonne_suivant = lem.get_colonne()
                            suivant = self.grille[ligne_suivant][colonne_suivant]
                        if vision2 != "Combat" and vision2 is not None:
                            ligne_suivant = lem.get_ligne()
                            colonne_suivant = lem.get_colonne() + lem.get_direction()
                            suivant = self.grille[ligne_suivant][colonne_suivant]
                        if vision3 != "Combat" and vision3 is not None:
                            ligne_suivant = lem.get_ligne() + 1
                            colonne_suivant = lem.get_colonne()
                            suivant = self.grille[ligne_suivant][colonne_suivant]

                        #Et si une des zones contient un lemming alors le monstre mange le lemming et le lemming meurt
                        if suivant is not None:
                            suivant.liberer()
                            cible = self.mourir(ligne_suivant, colonne_suivant)
                            self.set_grille(ligne_suivant, colonne_suivant, Outil.Case(" "))
                            aff = self.creation_affichage()
                            aff.afficher_terrain(ligne_suivant * 40, colonne_suivant * 40)
                            if cible == self.get_objectif().get_porteur():
                                self.get_objectif().set_porteur(None)
                            lem.set_deplacement("Statique")

                    #On regarde ensuite si la prochaine case ou le monstre ira contient de l'eau
                    elif devant.get_Terrain() == 'E' or dessous.get_Terrain() == 'E':
                        #Si c'est le cas alors le monstre meurt
                        position.liberer()
                        self.mourir(lem.get_ligne(), lem.get_colonne())

                    #Ensuite on regarde si le bloc en dessous du monstre est vide
                    elif dessous.est_libre() is True:
                        #Si c'est le cas alors de monstre tombe
                        position.liberer()
                        lem.tomber()
                        valeur_test = 1

                    #Puis on regarde si le bloc devant est vide
                    elif devant.est_libre() is True:
                        position.liberer()
                        #On regarde ensuite si le bloc de devant et sur du vide
                        if devant_bas.est_plein() is not True:
                            #Si c'est le cas alors de le monstre se retourne
                            lem.retourner()
                        else:
                            #Sinon le monstre avance
                            lem.avancer()
                            valeur_test = 2
                            
                    #Si rien de tout cela n'est realiser alors le monstre se retourne
                    else:
                        lem.retourner()

                    #On corrige ensuite si besoin les problemes de collisions avec les autres creatures
                    for lem_test in self.get_creature():
                        if lem.get_ligne() == lem_test.get_ligne() and lem.get_colonne() == lem_test.get_colonne() and lem.get_reference() != lem_test.get_reference():
                            if valeur_test == 1:
                                lem.monter()
                            elif valeur_test == 2:
                                lem.reculer()

                #On s'occupe ensuite des lemmings 
                else:
                    #On differencie tout d'abord tout les lemmings en fonction de leur forme
                    if lem.get_forme() == "Jump":
                        ordre = 0
                    elif lem.get_forme() == "Combat":
                        ordre = 1
                    elif lem.get_forme() == "Aile":
                        ordre = 2
                    elif lem.get_forme() == "Sol":
                        ordre = 3
                    elif lem.get_forme() == "Eau":
                        ordre = 4
                    valeur_test = 0

                    #On regarde tout d'abord quelle case est susceptible d'etre la prochaine case occupe par le lemming
                    if ordre != 2:
                        if dessous.est_libre() is True or dessous.get_Terrain() == "M":
                            if devant_bas.get_Terrain() != "P":
                                suivant = dessous
                                ligne_suivant = lem.get_ligne() + 1
                                colonne_suivant = lem.get_colonne()
                            else:
                                suivant = devant
                                ligne_suivant = lem.get_ligne()
                                colonne_suivant = lem.get_colonne() + lem.get_direction()
                        else:
                            suivant = devant
                            ligne_suivant = lem.get_ligne()
                            colonne_suivant = lem.get_colonne() + lem.get_direction()
                    else:
                        if dessus.est_libre() is True or dessus.get_Terrain() == "M":
                            suivant = dessus
                            ligne_suivant = lem.get_ligne() - 1
                            colonne_suivant = lem.get_colonne()
                        else:
                            suivant = devant
                            ligne_suivant = lem.get_ligne()
                            colonne_suivant = lem.get_colonne() + lem.get_direction()

                    #On va maintenant commencer tout les tests pour savoir quelle action sera effectuee par le lemming
                    #On regarde d'abord si le lemming est en plein saut et que la case devant lui est vide
                    if lem.get_capacite() == 'en saut' and devant.est_libre() is True:
                        #Si c'est le cas on regarde si la case de devant et sur du vide
                        if devant_bas.est_libre() is True:
                            #Si c'est le cas le lemming tombe
                            position.liberer()
                            lem.tomber()
                            valeur_test = 1
                        else:
                            #Sinon le lemming avance
                            position.liberer()
                            lem.avancer()
                            valeur_test = 3
                            lem.set_capacite(None)

                    #On regarde si le lemming peut tomber
                    elif dessous.est_libre() is True and ordre != 2 and devant_bas.get_Terrain() != "P":
                        #Si c'est le cas il tombe
                        position.liberer()
                        lem.tomber()
                        valeur_test = 1

                    #On regarde si le lemming est devant une pierre qu'il peut escalader et s'il peut l'escalader
                    elif devant.get_Terrain() == 'P' and self.get_objectif().get_porteur() != lem and dessus.est_libre():
                        #Si c'est le cas alors le lemming monte
                        position.liberer()
                        lem.monter()
                        valeur_test = 2

                    #On regarde ensuite si la prochaine case ou le lemming ira contient de l'eau
                    elif devant.get_Terrain() == 'E' or dessous.get_Terrain() == 'E':
                        if ordre == 4:
                            #Si c'est le cas et que le lemming est un lemming eau alors il monte ou il avance en fonction de la situation
                            if dessous.get_Terrain() == 'E':
                                position.liberer()
                                lem.tomber()
                                lem.set_deplacement("TomberEau")
                                valeur_test = 1

                            elif devant.get_Terrain() == 'E':
                                position.liberer()
                                lem.avancer()
                                lem.set_deplacement("AvancerEau")
                                valeur_test = 3

                        else:
                            #Sinon le lemming meurt
                            position.liberer()
                            self.mourir(lem.get_ligne(), lem.get_colonne())
                            aff = self.creation_affichage()
                            aff.afficher_terrain(lem.get_ligne() * 40, lem.get_colonne() * 40)
                            if lem == self.get_objectif().get_porteur():
                                self.get_objectif().set_porteur(None)
                                
                        #On envoie le bruit de l'eau
                        test = pygame.mixer.Sound("Musique/Eau.wav")
                        test.set_volume(0.5)
                        test.play()

                    #On regarde si le lemming est devant un levier et si c'est le cas le lemming l'active
                    elif suivant.get_Terrain() == "B" or suivant.get_Terrain() == "N":
                        test = pygame.mixer.Sound("Musique/Bouton.wav")
                        test.set_volume(0.2)
                        test.play()
                        for levier in self.get_leviers():
                            if [ligne_suivant, colonne_suivant] == [levier.get_ligne(), levier.get_colonne()]:
                                levier.set_mode("Off")
                                if suivant.get_Terrain() == "N":
                                    lem.retourner()
                                for porte in levier.get_portes():
                                    if porte.get_minuteur() is None:
                                        if porte.get_etat() == "On":
                                            porte.set_etat("Off")
                                        else:
                                            porte.set_etat("On")
                        lem.set_deplacement("Statique")

                    #Idem ici
                    elif suivant.get_Terrain() == "F":
                        test = pygame.mixer.Sound("Musique/Bouton.wav")
                        test.set_volume(0.2)
                        test.play()
                        for levier in self.get_leviers():
                            if [ligne_suivant, colonne_suivant] == [levier.get_ligne(), levier.get_colonne()]:
                                levier.set_mode("On")
                                lem.retourner()
                                for porte in levier.get_portes():
                                    if porte.get_minuteur() is None:
                                        if porte.get_etat() == "On":
                                            porte.set_etat("Off")
                                        else:
                                            porte.set_etat("On")
                        lem.set_deplacement("Statique")

                    #On regarde ensuite si le lemming est un lemming combat et qu'un monstre est juste a cote de lui
                    elif suivant.get_Terrain() == "M" and lem.get_forme() == "Combat":
                        #Si c'est le cas alors le lemming combat tue le monstre
                        suivant.liberer()
                        self.mourir(ligne_suivant, colonne_suivant)
                        lem.set_deplacement("Statique")

                    #On regarde ensuite si devant l'objectif est devant le lemming et que ce n'est pas un lemming aile
                    elif devant.get_Terrain() == 'O' and devant_haut.est_libre() and ordre != 2:
                        #Si c'est le cas alors le lemming prend l'objectif
                        test = pygame.mixer.Sound("Musique/Objectif.wav")
                        test.set_volume(1)
                        test.play()
                        self.get_objectif().set_porteur(lem)
                        position.liberer()
                        lem.avancer()
                        valeur_test = 3


                    #On regarde ensuite si l'objectif est sous le lemming que le lemming est un lemming aile
                    elif dessous.get_Terrain() == "O" and ordre == 2 and self.get_objectif().get_porteur() is None:
                        test = pygame.mixer.Sound("Musique/Objectif.wav")
                        test.set_volume(1)
                        test.play()
                        self.get_objectif().set_porteur(lem)
                        lem.set_deplacement("Statique")

                    #On regarde ensuite si la case au dessus du lemming est vide quand le lemming est un lemming aile
                    elif dessus.est_libre() is True and ordre == 2:
                        #Si c'est le cas le lemming monte
                        position.liberer()
                        lem.monter()
                        valeur_test = 2


                    #On regarde ensuite si la case devant le lemming est vide
                    elif devant.est_libre() is True:
                        #Si c'est le cas le lemming avance
                        position.liberer()
                        lem.avancer()
                        valeur_test = 3

                    #On regarde ensuite si la case devant le lemming est de la terre quand le lemming est un lemming sol
                    elif ordre == 3 and devant.get_Terrain() == 'T':
                        #Si c'est le cas le lemming creuse la terre
                        position.liberer()
                        self.set_grille(lem.get_ligne(), lem.get_colonne() + lem.get_direction(), Outil.Case(" "))
                        lem.avancer()
                        lem.set_deplacement("Creuser")

                    #On regarde ensuite si un saut est possible quand le lemming est un lemming jump
                    elif ordre == 0 and devant_haut.est_libre() is True:
                        #Si c'est le cas, on regarde si le lemming ne porte pas l'objectif
                        if self.get_objectif().get_porteur() != lem:
                            #Si c'est une nouvelle fois le cas, on regarde si la case au dessus du lemming est vide
                            if dessus.est_libre() is True:
                                #Si c'est le cas le lemming peut enfin monter
                                position.liberer()
                                lem.monter()
                                valeur_test = 2
                                lem.set_capacite("en saut")
                            else:
                                #Si la case du dessus n'est pas libre le lemming se retourne
                                lem.retourner()
                        else:
                            #Si le lemming porte l'objectif on regarde si la case au dessus de l'objectif est vide
                            if self.grille[lem.get_ligne() - 2][lem.get_colonne()].est_libre() is True:
                                #Si c'est le cas alors le lemming saute
                                position.liberer()
                                lem.monter()
                                valeur_test = 2
                                lem.set_capacite("en saut")
                            else:
                                #Sinon il se retourne
                                lem.retourner()

                    #Et enfin si aucune condition n'a etait validee alors le lemming se retourne
                    else:
                        lem.retourner()
                        for eau in self.get_eaux():
                            for zone in eau.get_prolongement():
                                if lem.get_ligne() == zone[0] and lem.get_colonne() == zone[1]:
                                    lem.set_deplacement("RetourEau")


                    #On corrige ensuite si besoin les problemes de collisions avec les autres creatures
                    for lem_test in self.get_creature():
                        if lem.get_ligne() == lem_test.get_ligne() and lem.get_colonne() == lem_test.get_colonne() and lem.get_reference() != lem_test.get_reference():
                            if valeur_test == 1:
                                lem.monter()
                            elif valeur_test == 2:
                                lem.tomber()
                            elif valeur_test == 3:
                                lem.reculer()
                            lem.set_deplacement("Statique")



        #On passe ensuite a l'objectif
        objectif = self.get_objectif()
        porteur = objectif.get_porteur()
        #On regarde tout d'abord si l'objectif est porte par un lemming
        if porteur is not None:
            #On regarde ensuite si le lemming qui le porte est un lemming aile
            if porteur.get_forme() == "Aile":
                #Puis on regarde si la case ou le lemming emmene l'objectif est vide
                suivant = self.get_grille()[porteur.get_ligne() + 1][porteur.get_colonne()]
                if suivant.est_plein() is not True or suivant.get_Terrain() == 'O':
                    #Si c'est le cas alors l'objectif suit le lemming
                    self.get_grille()[objectif.get_ligne()][objectif.get_colonne()].liberer()
                    objectif.suivre_aile()
                else:
                    #Sinon le lemming lÃ¢che l'objectif
                    objectif.set_porteur(None)
                    objectif.set_deplacement("Statique")
            else:
                #On fait la meme chose si le lemming n'est pas un lemming aile
                suivant = self.get_grille()[porteur.get_ligne() - 1][porteur.get_colonne()]
                if suivant.est_plein() is not True or suivant.get_Terrain() == 'O':
                    self.get_grille()[objectif.get_ligne()][objectif.get_colonne()].liberer()
                    objectif.suivre_normal()
                else:
                    objectif.set_porteur(None)
                    objectif.set_deplacement("Statique")
                    
        #On regarde ensuite si la case sous l'objectif est vide
        elif self.get_grille()[objectif.get_ligne() + 1][objectif.get_colonne()].est_plein() is not True:
            #Si c'est le cas alors l'objectif tombe
            self.get_grille()[objectif.get_ligne()][objectif.get_colonne()].liberer()
            objectif.tomber()
        #Sinon il ne bouge pas
        else:
            objectif.set_deplacement("Statique")

        #On regarde ensuite si l'objectif est a cote du depart et si c'est le cas le niveau se fini
        if self.get_grille()[objectif.get_ligne()][objectif.get_colonne() - 1].get_Terrain() == 'I':
            self.set_score(1)
        elif self.get_grille()[objectif.get_ligne()][objectif.get_colonne() + 1].get_Terrain() == 'I':
            self.set_score(1)
        elif self.get_grille()[objectif.get_ligne() + 1][objectif.get_colonne() + 1].get_Terrain() == 'I':
            self.set_score(1)
        elif self.get_grille()[objectif.get_ligne() + 1][objectif.get_colonne() - 1].get_Terrain() == 'I':
            self.set_score(1)
        elif objectif.get_ligne() + 2 < int((820 - (self.get_index()[1] * 2))/40):
            if self.get_grille()[objectif.get_ligne() + 2][objectif.get_colonne()].get_Terrain() == 'I':
                self.set_score(1)
                
        #Enfin on verifie si l'objectif n'est pas dans l'eau, si c'est le cas alors le niveau recommence
        for eau in self.get_eaux():
            for source in eau.get_prolongement():
                if objectif.get_colonne() == source[1]:
                    if objectif.get_ligne() == source[0] or objectif.get_ligne() + 1 == source[0]:
                        self.set_score(2)

    def demarrer(self, x_depart, y_depart, test_commande = None):
        """
        Permet de faire fonctionner le niveau correctement
        """
        def bouger():
            """
            Permet de passer un tour du niveau et d'afficher ensuite ce qui c'est passe
            """
            self.tour() # lance un tour de jeu
            aff = self.creation_affichage()
            aff.animer()
            self.info(aff)
            for i in range(10):
                touche_clavier()

        def attente():
            """
            Fait tourner le niveau tant qu'il n'est pas fini ou stoppe
            """
            while self.get_score() == 0:
                bouger()

        def pause():
            """
            Met le jeu en pause
            """
            fond = pygame.image.load("Sprite/Fond/Pause.png").convert_alpha()
            screen.blit(fond, (0, 0))
            pygame.display.flip()
            test = 0
            while test == 0:
                for event2 in pygame.event.get():
                    if event2.type == pygame.KEYDOWN:
                        if event2.key == pygame.K_p:
                            test = 1

            fond = pygame.image.load("Sprite/Fond/Fond_1.png").convert()
            screen.blit(fond, (0, 0))
            aff = self.creation_affichage()
            aff.afficher()
            self.info(aff)

        def commande():
            """
            Permet d'afficher les commandes du jeu
            """
            
            def modifier(page, ajout):
                """
                Permet changer la page des commandes
                """
                page += ajout
                if page == 12:
                    page = 1
                elif page == 0:
                    page = 11
                fond = pygame.image.load(f"Sprite/Commande/Page{page}.png").convert_alpha()
                screen.blit(fond, (300, 131))
                pygame.display.flip()
                return page

            test = 0
            page = 1
            fond = pygame.image.load(f"Sprite/Commande/Page{page}.png").convert_alpha()
            screen.blit(fond, (300, 131))
            pygame.display.flip()
            #On cree une boucle pour que les commandes soit quittees uniquement quand la touche t est pressee
            while test == 0:
                for event2 in pygame.event.get():
                    if event2.type == pygame.KEYDOWN:
                        if event2.key == pygame.K_t:
                            test = 1
                        #On regarde si les fleches de gauche et de droite sont presses pour changer, ou non, les pages
                        if event2.key == pygame.K_RIGHT:
                            page = modifier(page, 1)
                        if event2.key == pygame.K_LEFT:
                            page = modifier(page, -1)

            fond = pygame.image.load("Sprite/Fond/Fond_1.png").convert()
            screen.blit(fond, (0, 0))
            aff = self.creation_affichage()
            aff.afficher()
            self.info(aff)
            
        def menu():
            def menu_fleche(nb, horizontal):
                fond = pygame.image.load(f"Sprite/Commande/Menu.png").convert_alpha()
                screen.blit(fond, (300, 0))
                for i in range(1, 13):
                    if self.get_niveaux()[i - 1] == "Off":
                        fond = pygame.image.load(f"Sprite/Commande/Rouge.png").convert_alpha()
                    else:
                        fond = pygame.image.load(f"Sprite/Commande/Vert.png").convert_alpha()
                    screen.blit(fond, (560 + ((i - 1) % 6) * 90, 520 + (i // 7) * 120))
                    chiffre = pygame.image.load(f"Sprite/Commande/{i}.png").convert_alpha()
                    screen.blit(chiffre, (570 + ((i - 1) % 6) * 90, 520 + (i // 7) * 120))
                
                if nb < 2:
                    fleche = pygame.image.load(f"Sprite/Commande/fleche.png").convert_alpha()
                    screen.blit(fleche, (560, 245 + nb * 110))
                else:
                    fleche = pygame.image.load(f"Sprite/Commande/fleche.png").convert_alpha()
                    screen.blit(fleche, (570 + horizontal * 90, 340 + nb * 120))
                pygame.display.flip()
                
            fleche = 0
            horizontal = 0
            menu_fleche(fleche, horizontal)    
            test = 0
            while test == 0:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_t:
                            test = 1
                        if event.key == pygame.K_DOWN:
                            fleche += 1
                            if fleche > 3:
                                fleche = 0
                                horizontal = 0
                        if event.key == pygame.K_UP:
                            fleche -= 1
                            if fleche == 1:
                                horizontal = 0
                            if fleche < 0:
                                fleche = 3
                        if event.key == pygame.K_RIGHT and fleche > 1:
                            horizontal += 1
                            if horizontal == 6:
                                horizontal = 0
                        if event.key == pygame.K_LEFT and fleche > 1:
                            horizontal -= 1
                            if horizontal == -1:
                                horizontal = 5
                        if event.key == pygame.K_RETURN:
                            test = 1
                            if fleche == 0:
                                self.set_score(None)
                            elif fleche == 1:
                                fond = pygame.image.load("Sprite/Fond/Fond_1.png").convert()
                                screen.blit(fond, (0, 0))
                                commande()
                            else:
                                self.set_score(2 + (fleche - 2) * 6 + horizontal)
                            
                menu_fleche(fleche, horizontal)
                
            fond = pygame.image.load("Sprite/Fond/Fond_1.png").convert()
            screen.blit(fond, (0, 0))
            aff = self.creation_affichage()
            aff.afficher()
            self.info(aff)

        def touche_clavier():
            """
            Permet de retranscrire les actions que fait le joueur sur son clavier dans le jeu
            """
            info = ["rien"]
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    #On test si une touche est presse
                    if event.key == pygame.K_j:
                        info = ["oui", "Jump", 0]
                    if event.key == pygame.K_c:
                        info = ["oui", "Combat", 1]
                    if event.key == pygame.K_a:
                        info = ["oui", "Aile", 2]
                    if event.key == pygame.K_s:
                        info = ["oui", "Sol", 3]
                    if event.key == pygame.K_e:
                        info = ["oui", "Eau", 4]
                    if event.key == pygame.K_r:
                        info = ['non']
                    if event.key == pygame.K_f:
                        #Recommence le niveau
                        self.set_score(2)
                    if event.key == pygame.K_UP:
                        #Augmente la vitesse
                        if self.get_temps() >= 0.001:
                            self.set_temps(self.get_temps() - 0.001)
                    if event.key == pygame.K_DOWN:
                        #Diminue la vitesse
                        self.set_temps(self.get_temps() + 0.001)
                    if event.key == pygame.K_p:
                        #Met le jeu en pause
                        pause()
                    if event.key == pygame.K_t:
                        #Affiche les commandes
                        menu()



            if info[0] == "oui" and self.get_compteur() == 1:
                #Cree le lemming demande
                if self.get_grille()[self.get_depart()[0]][self.get_depart()[1] + 1].est_libre() is True:
                    test = pygame.mixer.Sound("Musique/Cri_Lemming.wav")
                    test.set_volume(0.2)
                    test.play()
                    self.set_compteur(0)
                    transition = []
                    for lem in self.get_creature():
                        if lem is not None:
                            transition.append(lem)
                    transition.append(Outil.Creature(info[1], self.get_depart()[0], self.get_depart()[1] + 1, 1, self.get_reference_lemming()))
                    self.set_reference_lemming(self.get_reference_lemming() + 1)
                    self.set_creature(transition) # on ajoute un lemming sur la grille

            elif info[0] == "non":
                #Fait disparaitre tout les lemming present sur le terrain
                transition = []
                for lem in self.get_creature():
                    if lem.get_forme() == "Monstre":
                        transition.append(lem)
                    else:
                        self.get_grille()[lem.get_ligne()][lem.get_colonne()].liberer()
                        aff = self.creation_affichage()
                        aff.afficher_terrain(lem.get_ligne() * 40, lem.get_colonne() * 40)
                self.set_creature(transition)
                self.get_objectif().set_porteur(None)


        #Creation du fond
        fond = pygame.image.load("Sprite/Fond/Fond_1.png").convert()
        screen.blit(fond, (0, 0))
        #Creation de valeur importante a l'affichage
        self.set_index([int((1600 - x_depart * 40)/2), int((820 - y_depart * 40)/2)])
        #Initialisation et affichage du niveau
        aff = self.creation_affichage()
        aff.initialisation()
        aff.afficher()
        self.info(aff)
        #Affichage des commandes si le niveau est le tuto 1
        if test_commande == 1:
            commande()
        #Et enfin lancement du jeu
        attente()
        return self.get_score(), len(self.get_mort()) - 1