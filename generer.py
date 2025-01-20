import sys
from lire_ecrire import lire_grammaire, ecrire_generer


def generer_mots(grammaire, longueur_max):
    """
    Génère tous les mots possibles d'une longueur maximale donnée, 
    en suivant les règles de la grammaire fournie.

    Args:
        grammaire: Un objet représentant la grammaire.
        longueur_max: La longueur maximale des mots à générer.

    Returns:
        Une liste de tous les mots générés, triée par ordre lexicographique.
    """
    def etendre(symboles):
        """
        Étend récursivement une séquence de symboles en utilisant les règles de la grammaire.

        Args:
            symboles: Une liste de symboles (terminaux ou non-terminaux).

        Returns:
            Une liste de toutes les séquences de symboles obtenues après une étape d'expansion.
        """
        if all(sym.islower() for sym in symboles):
            return {"".join(symboles)}

        resultats = set()
        for i, sym in enumerate(symboles):
            if sym.isupper():
                for gauche, droite in grammaire.regles:
                    if gauche == sym:
                        nouveaux_symboles = symboles[:i] + droite + symboles[i+1:]
                        if len(nouveaux_symboles) <= longueur_max:
                            resultats.update(etendre(nouveaux_symboles))
                break
        return resultats

    mots = set()
    for gauche, droite in grammaire.regles:
        if gauche == grammaire.axiome:
            mots.update(etendre(droite))

    return sorted(mot for mot in mots if len(mot) <= longueur_max)


def main():
    """
    Fonction principale du programme.

    Lit une grammaire à partir d'un fichier, génère des mots et les écrit dans un nouveau fichier.
    """
    if len(sys.argv) != 3 or not (sys.argv[2].endswith(".greibach") or sys.argv[2].endswith(".chomsky")):
        print("Usage: generer.py <n> |<fichier.greibach> or <fichier.chomsky|")
        sys.exit(1)
    
    fichier_grammaire = sys.argv[2]
    longueur_max = int(sys.argv[1])

    # Lire la grammaire
    grammaire = lire_grammaire(fichier_grammaire)

    # Générer les mots
    mots = generer_mots(grammaire, longueur_max)
    # écriture des mots
    ancien_nom = fichier_grammaire.rsplit(".", 1)
    nouveau_fichier = f"{ancien_nom[0]}_{longueur_max}_{ancien_nom[1]}.res"
    ecrire_generer(mots, nouveau_fichier)


if __name__ == "__main__":
    main()
