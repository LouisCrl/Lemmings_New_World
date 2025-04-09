#Ici toute les classes secondaires sont initialisees ici

class Creature:
    def  __init__(self, forme, ligne,  colonne,  direction, reference, capacite = None):
        self.set_forme(forme)
        self.set_ligne(ligne)
        self.set_colonne(colonne)
        self.set_direction(direction)
        self.set_reference(reference)
        self.set_capacite(capacite)
        self.set_deplacement("Statique")
    """
    Une classe qui permet de creer et deplacer des creatures, monstres comme lemming
    """

    #Creation de tout les get et set qui permet de renvoyer ou modifier chaque attribut de la classe
    
    def get_forme(self):
        """
        Forme correspond a l'espece de la creature
        Ex: Monstre, Aile, Eau
        """
        return self.forme

    def get_ligne(self):
        """
        Ligne correspond a la ligne sur laquelle est la creature sur le terrain
        """
        return self.ligne

    def get_colonne(self):
        """
        Colonne correspond a la colonne sur laquelle est la creature sur le terrain
        """
        return self.colonne

    def get_direction(self):
        """
        Direction correspond au sens dans lequel regarde la creature :
        -1 quand la creature regarde a gauche
        1 quand la creature regzarde a droite
        """
        return self.direction

    def get_reference(self):
        """
        Reference permet de differencie tout les lemmings ce qui facilite leurs interactions.
        Chaque lemming a une reference differente
        """
        return self.reference

    def get_capacite(self):
        """
        Capacite permet de savoir si une capacite d'un lemming est en action.
        Exemple: Quand un lemming jump est en plein saut capacite devient "en saut"
        """
        return self.capacite

    def get_deplacement(self):
        """
        Deplacement correspond a l'action que la creature est en train de faire.
        Exemple: Monter, Tomber, Avancer, Statique
        """
        return self.deplacement

    def set_forme(self, nouvelle_forme):
        self.forme = nouvelle_forme

    def set_ligne(self, nouvel_ligne):
        self.ligne = nouvel_ligne

    def set_colonne(self, nouveau_colonne):
        self.colonne = nouveau_colonne

    def set_direction(self, nouveau_direction):
        self.direction = nouveau_direction

    def set_reference(self, nouvelle_reference):
        self.reference = nouvelle_reference

    def set_capacite(self, nouvelle_capacite):
        self.capacite = nouvelle_capacite

    def set_deplacement(self, nouveau_deplacement):
        self.deplacement = nouveau_deplacement

    def __str__(self):
        """
        Affiche la creature sous forme de >, < ou M en fonction de sa direction et de sa forme
        """
        if self.get_forme() == "Monstre":
            creature = "M"
        else:
            if self.get_direction() == 1:
                creature = ">"
            elif self.get_direction() == -1:
                creature = "<"
        return creature

    def avancer(self):
        """
        Avance la creature de une case
        """
        self.set_colonne(self.get_colonne() + self.get_direction())
        self.set_deplacement("Avancer")

    def reculer(self):
        """
        Recule la creature de une case
        """
        self.set_colonne(self.get_colonne() - self.get_direction())
        #Reculer sert uniquement a annuler une avance qui n'aurait 
        #pas du ÃÂªtre faite donc aucun deplacement n'est prevu pour cette fonction

    def retourner(self):
        """
        Change le sens de la creature
        """
        self.set_direction(self.get_direction() * -1)
        self.set_deplacement("Retour")

    def tomber(self):
        """
        Fait tomber la creature d'une case
        """
        self.set_ligne(self.get_ligne() + 1)
        self.set_deplacement("Tomber")

    def monter(self):
        """
        Fait monter la creature d'une case
        """
        self.set_ligne(self.get_ligne() - 1)
        self.set_deplacement("Monter")

#_________________________________________________________________________________

class Eau:
    def __init__(self, Source):
        self.set_source(Source)
        self.set_prolongement([Source])
        self.set_DernierStade(None)
    """
    Une classe qui permet de creer des sources d'eau et de les faire couler
    """

    #Creation de tout les get et set qui permet de renvoyer ou modifier chaque attribut de la classe
    def get_source(self):
        """
        Source correspond aux coordonnees de la source de l'eau 
        """
        return self.Source

    def get_prolongement(self):
        """
        Prolongement regroupe toutes les coordonnees de chaque case occupe par l'eau
        """
        return self.Prolongement

    def get_DernierStade(self):
        """
        DernierStade permet d'identifie quel est la ou les dernieres case qui ont etait remplis par l'eau.
        """
        return self.DernierStade

    def set_source(self, nouvelle_source):
        self.Source = nouvelle_source

    def set_prolongement(self, nouveaux_prolongements):
        self.Prolongement = nouveaux_prolongements

    def set_DernierStade(self, nouveau_dernier_stade):
        self.DernierStade = nouveau_dernier_stade

    def etendre(self, emplacement):
        """
        Prolonge la source d'eau sur l'emplacement choisi.
        Emplacement contient les coordonnees de la case a remplir ainsi que son
        ordre dans la source en entier qui devient d'ailleur le Dernier Stade 
        de la source puisqu'il s'agit de la derniere source cree
        """
        prolongement_provisoire = self.get_prolongement()
        prolongement_provisoire.append(emplacement)
        self.set_prolongement(prolongement_provisoire)
        self.set_DernierStade(emplacement[2])

    def supprimer_partie(self, stade):
        """
        Supprime chaque partie de la source qui est arrive apres l'etape "stade"
        """
        prolongement_provisoire = []
        for zone in self.get_prolongement():
            if zone[2] < stade:
                prolongement_provisoire.append(zone)
        self.set_prolongement(prolongement_provisoire)

#__________________________________________________________________________________________

class Objectif:
    def __init__(self, ligne, colonne, porteur = None):
        self.set_ligne(ligne)
        self.set_colonne(colonne)
        self.set_porteur(porteur)
        self.set_deplacement("Statique")
    """
    Une classe qui permet de creer et deplacer l'objectif
    """

    #Creation de tout les get et set qui permet de renvoyer ou modifier chaque attribut de la classe
    def get_ligne(self):
        """
        Ligne correspond a la ligne sur laquelle est l'objectif sur le terrain
        """
        return self.ligne

    def get_colonne(self):
        """
        Colonne correspond a la colonne sur laquelle est l'objectif sur le terrain
        """
        return self.colonne

    def get_porteur(self):
        """
        Porteur correspond, s'il y en a un, au lemming qui porte l'objectif
        """
        return self.porteur

    def get_deplacement(self):
        """
        Deplacement correspond a l'action de l'objectif sur le terrain
        """
        return self.deplacement

    def set_ligne(self, nouvelle_ligne):
        self.ligne = nouvelle_ligne

    def set_colonne(self, nouvelle_colonne):
        self.colonne = nouvelle_colonne

    def set_porteur(self, nouveau_porteur):
        self.porteur = nouveau_porteur

    def set_deplacement(self, nouveau_deplacement):
        self.deplacement = nouveau_deplacement

    def suivre_normal(self):
        """
        Suit le porteur s'il n'est pas un lemming aile
        """
        #Actualisation des coordonnees
        self.set_ligne(self.get_porteur().get_ligne() - 1) #Si le porteur n'est pas aile l'objectif sera toujours au dessus du lemming
        self.set_colonne(self.get_porteur().get_colonne())
        #Actualisation de l'action de l'objectif
        deplacement = self.get_porteur().get_deplacement()
        #L'objectif ne peut rien faire d'autre a part Avancer, Monter et Tomber
        if deplacement == "Avancer" or deplacement == "Tomber" or deplacement == "Monter":
            self.set_deplacement(deplacement)
        else:
            self.set_deplacement("Statique")

    def suivre_aile(self):
        """
        Suit le porteur s'il est un lemming aile
        """
        self.set_ligne(self.get_porteur().get_ligne() + 1) #Si le porteur est aile l'objectif sera toujours en dessous du lemming
        self.set_colonne(self.get_porteur().get_colonne())
        deplacement = self.get_porteur().get_deplacement()
        if deplacement == "Avancer" or deplacement == "Tomber" or deplacement == "Monter":
            self.set_deplacement(deplacement)
        else:
            self.set_deplacement("Statique")

    def tomber(self):
        """
        Fait tomber l'objectif de une case
        """
        self.set_ligne(self.get_ligne() + 1)
        self.set_deplacement("Tomber")

#___________________________________________________________________________________________

class Levier:
    def __init__(self, forme, ligne, colonne, portes, mode):
        self.set_forme(forme)
        self.set_ligne(ligne)
        self.set_colonne(colonne)
        self.set_portes(portes)
        self.set_mode(mode)
    """
    Une classe qui creer et modifier les leviers, boutons et minuteur
    """

    #Creation de tout les get et set qui permet de renvoyer ou modifier chaque attribut de la classe
    def get_forme(self):
        """
        Forme correspond au type de levier
        Exemple: Levier, Bouton
        """
        return self.forme

    def get_ligne(self):
        """
        Ligne correspond a la ligne sur laquelle est le levier sur le terrain
        """
        return self.ligne

    def get_colonne(self):
        """
        Colonne correspond a la colonne sur laquelle est le levier sur le terrain
        """
        return self.colonne

    def get_portes(self):
        """
        Portes correspond a toutes les portes que le levier peut ouvrir ou fermer
        """
        return self.portes

    def get_mode(self):
        """
        Mode permet de savoir si le levier est allume ou eteint
        """
        return self.mode

    def set_forme(self, nouvelle_forme):
        self.forme = nouvelle_forme

    def set_ligne(self, nouvelle_ligne):
        self.ligne = nouvelle_ligne

    def set_colonne(self, nouvelle_colonne):
        self.colonne = nouvelle_colonne

    def set_portes(self, nouvelles_portes):
        self.portes = nouvelles_portes

    def set_mode(self, nouveau_mode):
        self.mode = nouveau_mode

#_____________________________________________________________________________________________

class Porte:
    def __init__(self, ligne, colonne, direction, longueur, etape, etat, minuteur = None, minuteur_actuel = None):
        self.set_ligne(ligne)
        self.set_colonne(colonne)
        self.set_direction(direction)
        self.set_longueur(longueur)
        self.set_etape(etape)
        self.set_etat(etat)
        self.set_minuteur(minuteur)
        self.set_minuteur_actuel(minuteur_actuel)
        self.set_deplacement("Statique")
    """
    Une classe qui cree et modifie les portes misent en relations avec les leviers, boutons ou minuteurs
    """

    #Creation de tout les get et set qui permet de renvoyer ou modifier chaque attribut de la classe
    def get_ligne(self):
        """
        Ligne correspond a la ligne sur laquelle commence la porte sur le terrain
        """
        return self.ligne

    def get_colonne(self):
        """
        Colonne correspond a la colonne sur laquelle commence la porte sur le terrain
        """
        return self.colonne

    def get_direction(self):
        """
        Direction correspond a l'orientation de la porte
        Exemple: Droite, Haut, Bas, Gauche
        """
        return self.direction

    def get_longueur(self):
        """
        Longueur correspond a la longueur maximal de la porte
        """
        return self.longueur

    def get_etape(self):
        """
        Etape correspond au nombre de case qui sont sorti
        """
        return self.etape

    def get_etat(self):
        """
        Etat permet de savoir si la porte doit ÃÂªtre ouverte ou fermee
        """
        return self.etat

    def get_minuteur(self):
        """
        Minuteur correspond au delai auquel s'ouvre et se ferme la porte
        """
        return self.minuteur

    def get_minuteur_actuel(self):
        """
        Minuteur actuel correspond au stage auquel est le minuteur
        """
        return self.minuteur_actuel

    def get_deplacement(self):
        """
        Deplacement permet de savoir quel action la porte fait sur le terrain
        Exemple: Avancer, Statique, Reculer
        """
        return self.deplacement

    def set_ligne(self, nouvelle_ligne):
        self.ligne = nouvelle_ligne

    def set_colonne(self, nouvelle_colonne):
        self.colonne = nouvelle_colonne

    def set_direction(self, nouvelle_direction):
        self.direction = nouvelle_direction

    def set_longueur(self, nouvelle_longueur):
        self.longueur = nouvelle_longueur

    def set_etape(self, nouvelle_etape):
        self.etape = nouvelle_etape

    def set_etat(self, nouvelle_etat):
        self.etat = nouvelle_etat

    def set_minuteur(self, nouveau_minuteur):
        self.minuteur = nouveau_minuteur

    def set_minuteur_actuel(self, nouveau_minuteur_actuel):
        self.minuteur_actuel = nouveau_minuteur_actuel

    def set_deplacement(self, nouveau_deplacement):
        self.deplacement = nouveau_deplacement

    def temps(self):
        """
        Actualise le miuteur et/ou la porte associee
        """
        if self.get_etat() == "Off" and self.get_etape() == 0:
            self.set_minuteur_actuel(self.get_minuteur_actuel()  + 1)
            #Le minuteur augmente de 1 quand la porte est totalement rentre
            
        elif self.get_etat() == "On" and self.get_etape() == self.get_longueur():
            self.set_minuteur_actuel(self.get_minuteur_actuel()  + 1)
            #Le minuteur augmente de 1 quand la porte est totalement sorti
            
        if self.get_minuteur_actuel() == self.get_minuteur():
            self.set_minuteur_actuel(0)
            if self.get_etat() == "Off":
                self.set_etat("On")
                
            elif self.get_etat() == "On":
                self.set_etat("Off")
            #La porte change d'etat car le minuteur est fini

    def mouvement(self):
        """
        Ouvre ou ferme la porte
        """
        if self.get_etat() == "Off" and self.get_etape() != 0:
            self.set_etape(self.get_etape() - 1)
            self.set_deplacement("Reculer")
            #La porte rentre
            
        elif self.get_etat() == "On" and self.get_etape() != self.get_longueur():
            self.set_etape(self.get_etape() + 1)
            self.set_deplacement("Avancer")
            #La porte sort
            
        else:
            self.set_deplacement("Statique")
            #La porte ne bouge pas

    def orientation(self):
        """
        Renvoie les coordonnees correspondant a l'orientation de la porte
        """
        if self.get_direction() == "Droite":
            ligne_porte = 0
            colonne_porte = 1
        elif self.get_direction() == "Gauche":
            ligne_porte = 0
            colonne_porte = -1
        elif self.get_direction() == "Haut":
            ligne_porte = -1
            colonne_porte = 0
        elif self.get_direction() == "Bas":
            ligne_porte = 1
            colonne_porte = 0
        return ligne_porte, colonne_porte

#________________________________________________________________________________________

class Case:
    def  __init__(self,  Terrain, creature = None):
        self.set_Terrain(Terrain)
        self.set_creature(creature)
    """
    Une classe qui permet de modifier les cases du terrains ou les utiliser
    """

    #Creation de tout les get et set qui permet de renvoyer ou modifier chaque attribut de la classe
    def get_Terrain(self):
        """
        Terrain correspond au type de la case
        """
        return self.Terrain

    def get_creature(self):
        """
        Creature correspond a la creature presente sur la case s'il y en a une
        """
        return self.creature

    def set_Terrain(self, nouvel_Terrain):
        self.Terrain = nouvel_Terrain

    def set_creature(self, nouvelle_creature):
        self.creature = nouvelle_creature

    def __str__(self):
        """
        Affiche la classe
        """
        return self.get_Terrain()

    def est_libre(self):
        """
        Renvoie si la case est vide ou pas
        """
        if self.get_Terrain() == " ":
            libre = True
        else:
            libre = False
        return libre

    def est_plein(self):
        """
        Renvoie si la case est un bloc plein
        """
        test = self.get_Terrain()
        if test == "#" or test == "T" or test == "C" or test == "P":
            plein = True
        else:
            plein = False
        return plein

    def occuper(self, creature):
        """
        Affiche un lemming sur la case
        """
        if creature.get_direction() == 1:
            self.set_Terrain(">")
        elif creature.get_direction() == -1:
            self.set_Terrain("<")
        self.set_creature((creature.get_ligne(), creature.get_colonne(), creature.get_direction()))

    def liberer(self):
        """
        Supprime le lemming de la case
        """
        self.set_Terrain(" ")
        self.set_creature(None)
        
