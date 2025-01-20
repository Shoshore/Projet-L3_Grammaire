import ply.yacc as yacc
from lexer import tokens, build_lexer


# Structure de données pour la grammaire

class Grammaire:
    """
    Classe représentant une grammaire formelle.
    Attributs:
    ----------
    regles : list
        Liste des règles de la grammaire sous forme de tuples (gauche, droite).
    axiome : None
        Axiome de la grammaire (non utilisé dans cette implémentation).
    Méthodes:
    ---------
    __init__():
        Initialise une nouvelle instance de la classe Grammaire avec une liste vide de règles et un axiome à None.
    ajouter_regle(gauche, droite):
        Ajoute une règle à la grammaire. La partie droite de la règle peut être une liste de listes, qui sera aplanie.
    __str__():
        Retourne une représentation sous forme de chaîne de caractères de toutes les règles de la grammaire.
    """
    def __init__(self):
        self.regles = []
        self.axiome = None

    def ajouter_regle(self, gauche, droite):
        droite_aplatie = [item for sublist in droite for item in (sublist if isinstance(sublist, list) else [sublist])]
        self.regles.append((gauche, droite_aplatie))

    def __str__(self):
        return "\n".join(f"{gauche} : {' '.join(droite)}" for gauche, droite in self.regles)


# Regles de la grammaire
def p_grammaire(p):
    '''grammaire : regles'''
    p[0] = p[1]


def p_regles(p):
    '''regles : regle NEWLINE regles
              | regle'''
    p[0] = Grammaire()
    gauche, droite = p[1]
    p[0].ajouter_regle(gauche, droite)
    if len(p) == 4:
        p[0].regles.extend(p[3].regles)


def p_regle(p):
    '''regle : NON_TERMINAL COLON productions'''
    p[0] = (p[1], p[3])


def p_productions(p):
    '''productions : production productions
                   | production'''
    p[0] = [p[1]] + (p[2] if len(p) == 3 else [])


def p_production(p):
    '''production : TERMINAL
                  | NON_TERMINAL
                  | EPSILON
                  | TERMINAL production
                  | NON_TERMINAL production'''
    p[0] = [p[1]] + (p[2] if len(p) == 3 else [])


def p_error(p):
    if p:
        print(f"Erreur syntaxique à la ligne {p.lineno}, à '{p.value}' (type: {p.type})")
    else:
        print("Erreur syntaxique à la fin de l'entrée")


# création du parser
parser = yacc.yacc(start="grammaire")


def build_parser(contenu):
    """
    Construit et retourne un analyseur pour le contenu donné.
    Args:
        contenu (str): Le contenu à analyser.
    Retourne:
        Le contenu analysé en utilisant l'analyseur lexical spécifié.
    """
    lexer = build_lexer(contenu)
    grammaire = parser.parse(contenu, lexer=lexer)
    grammaire.axiome = grammaire.regles[0][0]
    return grammaire
