from parser_yacc import build_parser


def lire_grammaire(fichier):
    """
    Lit une grammaire depuis un fichier et retourne son contenu sous forme de parser.

    Args:
        fichier (str): Le chemin du fichier contenant la grammaire.

    Returns:
        object: Un objet parser construit à partir du contenu du fichier.
    """
    with open(fichier, "r") as f:
        contenue = f.read()
    f.close()
    return build_parser(contenue) 


def ecrire_general(grammaire, fichier):
    """
    Écrit la représentation de la grammaire dans un fichier.
    """
    with open(fichier, "w") as f:
        f.write(str(grammaire))
    f.close()


def ecrire_generer(mots, fichier):
    """
    Écrit chaque mot de la liste dans un fichier, un par ligne.
    """
    with open(fichier, "w") as f:
        f.write("\n".join(mots) + "\n")
    f.close()