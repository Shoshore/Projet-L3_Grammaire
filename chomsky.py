from unit_del_copie import unit, del_, axiome_premiere_ligne, start


def term(grammaire): 
    """
    Remplace tous les terminaux apparaissant dans des règles de production de plus d'un symbole
    par des variables non terminales uniques. Ajoute les règles nécessaires pour ces nouvelles variables.
    """
    nouvelles_regles = []
    correspondance_terminaux = {}
    compteur_terminaux = 1

    def obtenir_nouvelle_variable(symbole):
        """
        Crée une nouvelle variable légale pour un terminal donné et ajoute une règle correspondante.
        """
        nonlocal compteur_terminaux
        if symbole not in correspondance_terminaux:
            nouvelle_variable = f"T{compteur_terminaux}"
            correspondance_terminaux[symbole] = nouvelle_variable
            compteur_terminaux += 1
            nouvelles_regles.append((nouvelle_variable, [symbole]))
        return correspondance_terminaux[symbole]

    nouvelles_regles.extend(
        (gauche, [obtenir_nouvelle_variable(symb) if symb.islower() else symb for symb in droite])
        if len(droite) > 1 else (gauche, droite)
        for gauche, droite in grammaire.regles
    )
    
    grammaire.regles = nouvelles_regles
    return grammaire


def bin(grammaire):
    """
    Transforme les règles de production pour qu'elles aient au maximum deux symboles à droite.
    Si une règle a plus de deux symboles à droite, elle est décomposée en plusieurs règles intermédiaires.
    """
    nouvelles_regles = []
    compteur_variables = 0

    def obtenir_nouvelle_variable():
        """
        Génère une nouvelle variable unique en incrémentant un compteur.
        Returns:
            str: Une nouvelle variable sous la forme "X{compteur_variables}".
        """
        nonlocal compteur_variables
        compteur_variables += 1
        return f"X{compteur_variables}"

    for gauche, droite in grammaire.regles:
        while len(droite) > 2:
            nouvelle_variable = obtenir_nouvelle_variable()
            nouvelles_regles.append((gauche, [droite[0], nouvelle_variable]))
            gauche = nouvelle_variable
            droite = droite[1:]
        nouvelles_regles.append((gauche, droite))
    
    grammaire.regles = nouvelles_regles
    return grammaire


def chomsky(grammaire):
    """
    Convertit une grammaire en forme normale de Chomsky en appliquant successivement
    les étapes de transformation : ajout d'un nouveau symbole de départ, remplacement des terminaux,
    binarisation des règles, suppression des epsilon-productions, et suppression des règles unitaires.

    Arguments:
    grammaire -- un objet représentant la grammaire

    Retourne:
    grammaire -- la grammaire transformée en forme normale de Chomsky
    """
    # print(f"Grammaire initiale:\n{grammaire}\n")
    grammaire = start(grammaire)
    # print(f"Après start:\n{grammaire}\n")
    grammaire = term(grammaire)
    # print(f"Après term:\n{grammaire}\n")
    grammaire = bin(grammaire)
    # print(f"Après bin:\n{grammaire}\n")
    grammaire = del_(grammaire)
    # print(f"Après del:\n{grammaire}\n")
    grammaire = unit(grammaire)
    # print(f"Après unit:\n{grammaire}\n")

    # Réorganiser les règles pour que l'axiome soit en première ligne
    grammaire = axiome_premiere_ligne(grammaire)
    return grammaire
