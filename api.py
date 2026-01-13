"""Module d'API du jeu Quoridor

Attributes:
    URL (str): Constante représentant le début de l'url du serveur de jeu.

Functions:
    * créer_une_partie - Créer une nouvelle partie et retourne l'état de cette dernière.
    * récupérer_une_partie - Retrouver l'état d'une partie spécifique.
    * appliquer_un_coup - Exécute un coup et retourne le nouvel état de jeu.
"""

import requests

URL = "https://pax.ulaval.ca/quoridor/api/a25/"


def créer_une_partie(idul, secret):
    """Permet de créer une nouvelle partie de Quoridor. en utilissant l'idul et le secret."""
    rep = requests.post(f"{URL}/jeux", auth=(idul, secret), timeout=30000)
    if rep.status_code == 200:
        data = rep.json()
        return data["id"], data["état"]
    if rep.status_code == 401:
        raise PermissionError(rep.json()["message"])
    if rep.status_code == 406:
        raise RuntimeError(rep.json()["message"]) 
    raise ConnectionError


def appliquer_un_coup(id_partie, coup, position, idul, secret):
    """Permet d'appliquer un coup dans une partie existante."""
    rep = requests.put(
        f"{URL}/jeux/{id_partie}",
        auth=(idul, secret),
        json={"coup": coup, "position": position},
        timeout=30000)
    if rep.status_code == 200:
        data = rep.json()
        if data["partie"] == "terminée":
            raise StopIteration(data["gagnant"])
        return data["coup"], data["position"]
    if rep.status_code == 401:
        raise PermissionError(rep.json()["message"])
    if rep.status_code == 404:
        raise ReferenceError(rep.json()["message"])
    if rep.status_code == 406:
        raise RuntimeError(rep.json()["message"])
    raise ConnectionError


def récupérer_une_partie(id_partie, idul, secret):
    """Permet de continuer une partie existante en récupérant son état actuel."""
    rep = requests.get(f"{URL}/jeux/{id_partie}", auth=(idul, secret), timeout=30000)
    if rep.status_code == 200:
        data = rep.json()
        return data["id"], data["état"]
    if rep.status_code == 401:
        raise PermissionError(rep.json()["message"])
    if rep.status_code == 404:
        raise ReferenceError(rep.json()["message"])
    if rep.status_code == 406:
        raise RuntimeError(rep.json()["message"])
    raise ConnectionError
