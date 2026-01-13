"""Module de la classe Quoridor
Classes:
    * Quoridor - Classe pour encapsuler le jeu Quoridor.
    * interpréter_la_ligne_de_commande - Génère un interpréteur de commande.
"""

import argparse
from copy import deepcopy
import networkx as nx
from quoridor_error import QuoridorError
from graphe import construire_graphe

class Quoridor:
    """Classe pour encapsuler le jeu Quoridor.

    Vous ne devez pas créer d'autre attributs pour votre classe.

    Attributes:
        joueurs (List): Un itérable de deux dictionnaires joueurs
            dont le premier est toujours celui qui débute la partie.
        murs (Dict): Un dictionnaire contenant une clé 'horizontaux' associée à
            la liste des positions [x, y] des murs horizontaux, et une clé 'verticaux'
            associée à la liste des positions [x, y] des murs verticaux.
        tour (int): Un entier positif représentant le tour du jeu (1 pour le premier tour).
    """


    def __init__(self, joueurs, murs=None, tour=1):
        """Constructeur de la classe Quoridor.
        Initialise une partie de Quoridor avec les joueurs, les murs et le tour spécifiés,
        en s'assurant de faire une copie profonde de tout ce qui a besoin d'être copié.
        Cette méthode ne devrait pas être modifiée.

        Args:
            joueurs (List): un itérable de deux dictionnaires joueurs
                dont le premier est toujours celui qui débute la partie.
            murs (Dict, optionnel): Un dictionnaire contenant une clé 'horizontaux' associée à
                la liste des positions [x, y] des murs horizontaux, et une clé 'verticaux'
                associée à la liste des positions [x, y] des murs verticaux.
            tour (int, optionnel): Un entier positif représentant le tour du jeu 
            (1 pour le premier tour).
        """
        self.tour = tour
        self.joueurs = deepcopy(joueurs)
        self.murs = deepcopy(murs or {"horizontaux": [], "verticaux": []})


    def état_partie(self):
        """Produire l'état actuel du jeu.

        Cette méthode ne doit pas être modifiée.

        Returns:
            Dict: Une copie de l'état actuel du jeu sous la forme d'un dictionnaire.
                  Notez que les positions doivent être sous forme de liste [x, y] uniquement.
        """
        return deepcopy(
            {
                "tour": self.tour,
                "joueurs": self.joueurs,
                "murs": self.murs,
            }
        )


    def formater_entête(self):
        """Formater l'entete du jeu avec les joueurs et leurs murs."""
        joueurs = self.joueurs
        entete = "Legende:\n"

        # Trouver la longueur maximale des noms pour l'alignement
        longueur_max = max(len(joueur["nom"]) for joueur in joueurs)

        for i, j in enumerate(joueurs, 1):
            espace = " " * (longueur_max - len(j["nom"]))
            entete += f"   {i}={j['nom']},{espace} murs={'|' * j['murs']}\n"
        return entete


    def formater_le_damier(self):
        """Formater le damier du jeu avec les positions des joueurs et des murs."""
        damier = "   -----------------------------------\n"
        murs_verticaux = []
        for x in range(1, 10):
            for y in range(1, 10):
                if [x, y] in self.murs.get("verticaux", []):
                    murs_verticaux.append([x - 1, y + 1])
        for i in range(9):
            y = 9 - i
            ligne_cases = str(y) + " |"
            for x in range(1, 10):
                if [x, y] == self.joueurs[0]["position"]:
                    ligne_cases += " 1 "
                elif [x, y] == self.joueurs[1]["position"]:
                    ligne_cases += " 2 "
                else:
                    ligne_cases += " . "
                if x != 9:
                    if [x, y] in murs_verticaux or [x, y + 1] in murs_verticaux:
                        ligne_cases += "|"
                    else:
                        ligne_cases += " "
            damier += ligne_cases + "|\n"
            ligne_entre = "  |"
            x = 1
            while x <= 9:
                if [x, y] in self.murs.get("horizontaux", []):
                    ligne_entre += "-------"
                    if [x + 1, y] in murs_verticaux:
                        ligne_entre += "|"
                    elif x != 9:
                        ligne_entre += " "
                    x += 2
                else:
                    ligne_entre += "   "
                    if [x, y] in murs_verticaux:
                        ligne_entre += "|"
                    elif x != 9:
                        ligne_entre += " "
                    x += 1
            if i == 8:
                damier += (
                    "--|-----------------------------------\n"
                    "  | 1   2   3   4   5   6   7   8   9\n"
                )
                break
            damier += ligne_entre + "|\n"
        return damier


    def __str__(self):
        """Représentation complète du jeu avec l'entête et le damier."""
        return self.formater_entête() + self.formater_le_damier()


    def déplacer_un_joueur(self, nom_joueur, position):
        """Déplace un jeton sur le damier."""

        x, y = position

        # Vérifier si la position est dans le damier
        if not (1 <= x <= 9 and 1 <= y <= 9):
            raise QuoridorError("La position est invalide (en dehors du damier).")

        # Trouver le joueur
        joueur = next((j for j in self.joueurs if j["nom"] == nom_joueur), None)
        if joueur is None:
            raise QuoridorError(f"Le joueur {nom_joueur} n'existe pas.")

        # Construire le graphe pour vérifier les déplacements possibles
        graphe = construire_graphe(
            [j["position"] for j in self.joueurs],
            self.murs["horizontaux"],
            self.murs["verticaux"]
        )

        # Vérifier si la position demandée est atteignable depuis la position actuelle
        if tuple(position) not in graphe.successors(tuple(joueur["position"])):
            raise QuoridorError("La position est invalide pour l'état actuel du jeu.")

        # Déplacer le joueur
        joueur["position"] = position


    def placer_un_mur(self, nom_joueur, position, orientation):
        """Placer un mur sur le damier."""
        x, y = position

        # Vérifier que le joueur existe
        joueur = next((j for j in self.joueurs if j["nom"] == nom_joueur), None)
        if joueur is None:
            raise QuoridorError(f"Le joueur {nom_joueur} n'existe pas.")

        # Vérifier que le joueur a des murs disponibles
        if joueur["murs"] <= 0:
            raise QuoridorError("Le joueur a déjà placé tous ses murs.")

        # Vérifier que la position est valide pour le damier
        if not (1 <= x <= 9 and 1 <= y <= 9):
            raise QuoridorError("La position est invalide (en dehors du damier).")

        # Vérifier si un mur existe déjà à cette position
        murs = self.murs["horizontaux"] if orientation == "MH" else self.murs["verticaux"]
        if position in murs:
            raise QuoridorError("Un mur occupe déjà cette position.")

        # Ajouter temporairement le mur pour tester si cela bloque les joueurs
        murs.append(position)

        # Construire le graphe après ajout du mur
        graphe = construire_graphe(
            [j["position"] for j in self.joueurs],
            self.murs["horizontaux"],
            self.murs["verticaux"]
        )

        # Vérifier que chaque joueur peut encore atteindre sa ligne de victoire
        for i, j in enumerate(self.joueurs):
            destination = "B1" if i == 0 else "B2"
            if not nx.has_path(graphe, tuple(j["position"]), destination):
                # Annuler l'ajout du mur
                murs.remove(position)
                raise QuoridorError("Vous ne pouvez pas enfermer un joueur.")

        # Si tout est valide, mettre à jour le nombre de murs du joueur
        joueur["murs"] -= 1


    def appliquer_un_coup(self, nom_joueur, coup, position):
        """Appliquer un coup pour un joueur donné."""

        # Vérifier si la partie est terminée
        if self.partie_terminée():
            raise QuoridorError("La partie est déjà terminée.")

        # Vérifier que le joueur existe
        joueur = next((j for j in self.joueurs if j["nom"] == nom_joueur), None)
        if joueur is None:
            raise QuoridorError(f"Le joueur {nom_joueur} n'existe pas.")

        # Appliquer le coup selon le type
        if coup == "D":
            self.déplacer_un_joueur(nom_joueur, position)
        elif coup in ("MH", "MV"):
            self.placer_un_mur(nom_joueur, position, coup)
        else:
            raise QuoridorError(f"Type de coup invalide: {coup}")

        # Incrémenter le tour si c'est le joueur 2
        if self.joueurs.index(joueur) == 1:
            self.tour += 1

        return (coup, position)


    def sélectionner_un_coup(self, nom_joueur):
        """Demande au joueur son coup et vérifie sa validité."""

        while True:
            try:
                # Demander le type de coup
                coup = input(f"{nom_joueur}, entrez le type de coup (D, MH, MV) : ").strip()

                # Demander la position et transformer en liste d'entiers
                pos_str = input(f"{nom_joueur}, entrez la position du coup sous la forme x,y : ")
                position = [int(n.strip()) for n in pos_str.split(",")]

                # Créer une copie de l'état pour tester le coup
                copie_partie = Quoridor(self.joueurs, self.murs, self.tour)
                copie_partie.appliquer_un_coup(nom_joueur, coup, position)

                # Si aucun problème, on retourne le coup
                return (coup, position)

            except QuoridorError as e:
                print(f"Coup invalide : {e}. Veuillez réessayer.")
            except (ValueError, IndexError):
                print("Format de position invalide. Entrer deux entiers séparés d'une virgule.")


    def partie_terminée(self):
        """Déterminer si la partie est terminée."""

        # Joueur 1 : objectif ligne 9
        if self.joueurs[0]["position"][1] == 9:
            return self.joueurs[0]["nom"]

        # Joueur 2 : objectif ligne 1
        if self.joueurs[1]["position"][1] == 1:
            return self.joueurs[1]["nom"]

        # Sinon, la partie continue
        return False


    def jouer_un_coup(self, nom_joueur):
        """
        Docstring for jouer_un_coup
        Permet de jouer automatiquement un coup pour le joueur spécifié.
        """
        if self.partie_terminée():
            raise QuoridorError("La partie est déjà terminée.")

        joueur = next(j for j in self.joueurs if j["nom"] == nom_joueur)
        adversaire = next(j for j in self.joueurs if j["nom"] != nom_joueur)

        graphe = construire_graphe(
            [j["position"] for j in self.joueurs],
            self.murs["horizontaux"],
            self.murs["verticaux"]
        )

        # Objectifs
        objectif_joueur = "B1" if joueur == self.joueurs[0] else "B2"
        objectif_adv = "B2" if joueur == self.joueurs[0] else "B1"

        chemin_j = nx.shortest_path(graphe, tuple(joueur["position"]), objectif_joueur)
        chemin_a = nx.shortest_path(graphe, tuple(adversaire["position"]), objectif_adv)

        #Cas obligatoire : bloquer l'adversaire
        if len(chemin_a) == 2 and joueur["murs"] > 0:
            x, y = adversaire["position"]

            # Essayer mur horizontal puis vertical
            for orientation, pos in [
                ("MH", [x, y]),
                ("MV", [x, y])
            ]:
                try:
                    self.appliquer_un_coup(nom_joueur, orientation, pos)
                    return (orientation, pos)
                except QuoridorError:
                    pass  # essayer autre mur

        #Avancer sur le plus court chemin
        prochaine_case = list(chemin_j[1])
        self.appliquer_un_coup(nom_joueur, "D", prochaine_case)
        return ("D", prochaine_case)


def interpréter_la_ligne_de_commande():
    """Génère un interpréteur de commande.

    Returns:
        Namespace: Un objet Namespace tel que retourné par parser.parse_args().
                   Cette objet aura l'attribut «idul» représentant l'idul du joueur.
    """
    parser = argparse.ArgumentParser(description="Quoridor")

    parser.add_argument(
        "idul",
        help="IDUL du joueur"
    )
    parser.add_argument(
        "-a", "--automatique",
        action="store_true",
        help="Activer le mode automatique."
    )
    parser.add_argument(
        "-x", "--graphique",
        action="store_true",
        help="Activer le mode graphique."
    )

    return parser.parse_args()
