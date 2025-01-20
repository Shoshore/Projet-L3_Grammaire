from copy import deepcopy


def copie(liste):
    """
    Renvoie une copie de la liste avec deepcopy.
    """
    return deepcopy(liste)


def unit(grammaire):
    """
    Supprime les règles unitaires, c'est-à-dire les règles où le côté droit est un unique non terminal.
    Modifie la grammaire pour inclure les productions correspondantes des non terminaux référencés.
    """
    regles = copie(grammaire.regles)
    unit_productions = [(g, d[0]) for g, d in grammaire.regles if len(d) == 1 and d[0].isupper()]

    # Initialiser la fermeture pour chaque non terminal, y compris ceux qui ne sont pas présents dans les règles unitaires
    non_terminals = set(g for g, _ in grammaire.regles).union(set(d[0] for _, d in grammaire.regles if d and d[0].isupper()))
    fermeture = {nt: set() for nt in non_terminals}

    for gauche, droite in unit_productions:
        fermeture[gauche].add(droite)

    # Etendre les fermetures
    changed = True
    while changed:
        changed = False
        for gauche in fermeture:
            for droite in list(fermeture[gauche]):
                if droite in fermeture:
                    if not fermeture[gauche].issuperset(fermeture[droite]):
                        fermeture[gauche].update(fermeture[droite])
                        changed = True

    # Ajouter les productions correspondantes sans créer de doublons
    nouvelles_regles_finales = set()
    for gauche in fermeture:
        visites = set()
        stack = [gauche]
        while stack:
            current = stack.pop()
            if current not in visites:
                visites.add(current)
                for droite in fermeture[current]:
                    for g, d in regles:
                        if g == droite and not (len(d) == 1 and d[0].isupper()):
                            nouvelles_regles_finales.add((gauche, tuple(d)))
                    if droite != gauche:
                        stack.append(droite)

    # Ajouter les règles terminales
    for g, d in regles:
        if not (len(d) == 1 and d[0].isupper()):
            nouvelles_regles_finales.add((g, tuple(d)))

    grammaire.regles = [(g, list(d)) for g, d in nouvelles_regles_finales]
    return grammaire


def del_(grammaire):
    """
    Supprime les productions E (epsilon), c'est-à-dire les règles où le côté droit est vide.
    Modifie les autres règles pour tenir compte de la suppression des productions E.
    """
    epsilon_productions = {gauche for gauche, droite in grammaire.regles if droite == ['E']}
    nouvelles_regles = set()

    def ajouter_nouvelles_regles(gauche, droite):
        """
        Ajoute de nouvelles règles en remplaçant les symboles E par toutes les combinaisons possibles.
        """
        for i in range(len(droite)):
            if droite[i] in epsilon_productions:
                nouvelle_droite = droite[:i] + droite[i+1:]
                if nouvelle_droite:
                    regle = (gauche, tuple(nouvelle_droite))
                    if regle not in nouvelles_regles:
                        nouvelles_regles.add(regle)
                        ajouter_nouvelles_regles(gauche, nouvelle_droite)

    for gauche, droite in grammaire.regles:
        if droite != ['E']:
            nouvelles_regles.add((gauche, tuple(droite)))
            ajouter_nouvelles_regles(gauche, droite)

    # Conversion en liste de tuples
    grammaire.regles = [(g, list(d)) for g, d in nouvelles_regles]
    return grammaire


def axiome_premiere_ligne(grammaire):
    """
    Réorganise les règles d'une grammaire pour que la règle correspondant à l'axiome soit la première.
    Args:
        grammaire (Grammaire): Un objet représentant la grammaire, qui contient un attribut 'regles' (une liste de tuples représentant les règles)
                               et un attribut 'axiome' (l'axiome de la grammaire).
    Returns:
        Grammaire: La grammaire modifiée avec la règle de l'axiome en première position.
    """
    axiome_rule = next((gauche, droite) for gauche, droite in grammaire.regles if gauche == grammaire.axiome)
    grammaire.regles.remove(axiome_rule)
    grammaire.regles.insert(0, axiome_rule)
    return grammaire


def start(grammaire):
    """
    Ajoute un nouveau symbole de départ unique si l'axiome de base est utilisé ailleurs
    comme symbole non terminal, ou si la grammaire ne commence pas correctement.

    Arguments:
    grammaire -- un objet représentant la grammaire

    Retourne:
    grammaire, axiome -- la grammaire mise à jour avec un nouveau symbole de départ unique si nécessaire, 
                         et l'axiome actuel
    """
    # Récupérer l'axiome actuel de la grammaire
    axiome = grammaire.axiome

    # Vérifier si l'axiome est utilisé dans les côtés droits des règles
    utilise_comme_terminal = any(axiome in droite for _, droite in grammaire.regles)

    if utilise_comme_terminal:
        compteur = 1
        base_axiome = axiome.rstrip('0123456789')
        nouvel_axiome = f'{base_axiome}{compteur}'
        while any(nouvel_axiome in droite for _, droite in grammaire.regles) or nouvel_axiome == 'E':
            compteur += 1
            nouvel_axiome = f'{base_axiome}{compteur}'
        grammaire.ajouter_regle(nouvel_axiome, [axiome])
        grammaire.axiome = nouvel_axiome

    return grammaire


