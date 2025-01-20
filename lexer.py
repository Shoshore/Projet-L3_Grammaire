import ply.lex as lex

# Liste des tokens
tokens = (
    'NON_TERMINAL',
    'TERMINAL',
    'COLON',
    'EPSILON',
    'ALTERNATIVE',
    'NEWLINE'
)

# Définition des tokens
t_NON_TERMINAL = r'[A-Z][0-9]?'
t_TERMINAL = r'[a-z]'
t_COLON = r':'
t_EPSILON = r'E'
t_ignore = ' \t'
t_NEWLINE = r'\n'


def t_error(t):
    print(f"Caractère illégal'{t.value[0]}' à la ligne {t.lexer.lineno}")
    t.lexer.skip(1)


lexer = lex.lex()


# Structure de données pour la grammaire
def build_lexer(grammaire):
    """
    Initialise le lexer avec la grammaire fourni et le retourne.
    Args:
        grammaire (str): La grammaire à analyser par le lexer.
    Returns:
        Lexer: L'objet lexer initialisé avec la grammaire fourni.
    """
    lexer.input(grammaire)
    return lexer
