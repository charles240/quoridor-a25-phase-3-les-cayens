from api import appliquer_un_coup, créer_une_partie
from quoridor import Quoridor, interpréter_la_ligne_de_commande
from quoridorx import QuoridorX

JETONS = {
    "CHGAU223": "8f07387e-e832-4251-9c95-4307f520a97f",
}

if __name__ == "__main__":
    args = interpréter_la_ligne_de_commande()

    if args.idul not in JETONS:
        raise KeyError("IDUL inconnu.")

    secret = JETONS[args.idul]
    id_partie, état = créer_une_partie(args.idul, secret)

    # Choix de la classe selon -x
    ClasseJeu = QuoridorX if args.graphique else Quoridor
    quoridor = ClasseJeu(état["joueurs"], état["murs"], état["tour"])

    while True:
        if args.automatique:
            coup, position = quoridor.jouer_un_coup(
                quoridor.état_partie()["joueurs"][0]["nom"]
            )
        else:
            coup, position = quoridor.sélectionner_un_coup(
                quoridor.état_partie()["joueurs"][0]["nom"]
            )
            quoridor.appliquer_un_coup(
                quoridor.état_partie()["joueurs"][0]["nom"],
                coup,
                position,
            )

        try:
            coup, position = appliquer_un_coup(
                id_partie, coup, position, args.idul, secret
            )
            quoridor.appliquer_un_coup(
                quoridor.état_partie()["joueurs"][1]["nom"],
                coup,
                position,
            )
        except StopIteration as fin:
            print(f"Le gagnant est {fin}")
            break
