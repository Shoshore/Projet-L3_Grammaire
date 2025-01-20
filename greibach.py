from unit_del_copie import unit, del_, axiome_premiere_ligne, start


def suppression_recursion_gauche(grammaire):
    """
    Supprime la récursion gauche directe pour une grammaire donnée.
    """
    nouvelles_regles = []
    non_terminals = sorted(set(g for g, _ in grammaire.regles))

    for Ai in non_terminals:
        regles_recursive = []
        regles_non_recursive = []

        for gauche, droite in grammaire.regles:
            if gauche == Ai:
                if droite[0] == Ai:
                    regles_recursive.append(droite[1:])
                else:
                    regles_non_recursive.append(droite)

        if regles_recursive:
            # Générer un nouveau non-terminal unique qui respecte l'expression régulière [A-Z][0-9]?
            compteur = 1
            while True:
                Ai_prime = f"{Ai[0]}{compteur}"
                if all(Ai_prime != g for g, _ in grammaire.regles):
                    break
                compteur += 1

            nouvelles_regles.extend((Ai, regle + [Ai_prime]) for regle in regles_non_recursive)
            nouvelles_regles.extend((Ai_prime, regle + [Ai_prime]) for regle in regles_recursive)
            nouvelles_regles.append((Ai_prime, ['E']))
        else:
            nouvelles_regles.extend((Ai, droite) for droite in regles_non_recursive)

    grammaire.regles = nouvelles_regles
    return grammaire


def supprimer_occurences_en_tete(grammaire):
    """
    Supprime les occurrences des non-terminaux dans les règles de production de la grammaire.
    """
    non_terminals = sorted(set(g for g, _ in grammaire.regles))
    
    for Ai in non_terminals:
        Ai_regles = [(g, d) for g, d in grammaire.regles if g == Ai]
        for Aj in non_terminals:
            if Ai != Aj:
                Aj_regles = [(g, d) for g, d in grammaire.regles if g == Aj]
                updated_Aj_regles = []
                for gauche, droite in Aj_regles:
                    if droite[0] == Ai:
                        updated_Aj_regles.extend(
                            (gauche, Ai_droite + droite[1:]) for _, Ai_droite in Ai_regles
                        )
                    else:
                        updated_Aj_regles.append((gauche, droite))
                grammaire.regles = [rule for rule in grammaire.regles if rule[0] != Aj] + updated_Aj_regles
    
    return grammaire


def greibach(grammaire):
    """
    Transforme une grammaire donnée en Forme Normale de Greibach (GNF).
    Cette fonction applique une série de transformations pour convertir la grammaire
    d'entrée en Forme Normale de Greibach. Les transformations incluent :
    1. Remplacé l'axiome par un nouvel axiome si il apparait dans les règles de droites.
    2. Suppression des productions inutiles.
    3. Élimination des productions unitaires.
    4. Suppression de la récursion gauche.
    5. Suppression des occurrences dans la tête des productions.
    Args:
        grammaire (dict): La grammaire d'entrée représentée comme un dictionnaire où les clés sont
                          des symboles non-terminaux et les valeurs sont des listes de règles de production.
    Returns:
        dict: La grammaire transformée en Forme Normale de Greibach.
    """
    grammaire = start(grammaire)
    # print(f"START:\n{grammaire}\n")
    grammaire = del_(grammaire)
    # print(f"DEL:\n{grammaire}\n")
    grammaire = unit(grammaire)
    # print(f"UNIT:\n{grammaire}\n")
    grammaire = suppression_recursion_gauche(grammaire)
    # print(f"REC:\n{grammaire}\n")
    grammaire = supprimer_occurences_en_tete(grammaire)
    # print(f"HEAD:\n{grammaire}\n")

    # Réorganiser les règles pour que l'axiome soit en première ligne
    grammaire = axiome_premiere_ligne(grammaire)
    return grammaire
