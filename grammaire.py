from chomsky import chomsky
from greibach import greibach
from unit_del_copie import copie
from lire_ecrire import ecrire_general, lire_grammaire
import sys


def main():
    if len(sys.argv) != 2 or not sys.argv[1].endswith(".general"):
        print("Usage: grammaire.py <fichier.general>")
        sys.exit(1)

    fichier = sys.argv[1]
    grammaire = lire_grammaire(fichier)

    # Transformations
    grammaire_chomsky = chomsky(copie(grammaire))
    greibach_grammaire = greibach(copie(grammaire))

    # Écriture des grammaires
    nom_base = fichier.rsplit(".", 1)[0]
    ecrire_general(grammaire_chomsky, f"{nom_base}.chomsky")
    ecrire_general(greibach_grammaire, f"{nom_base}.greibach")


if __name__ == "__main__":
    main()
