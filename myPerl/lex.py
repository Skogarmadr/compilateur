#################################################
#  Projet Compilateur INF3dlm-a					#
#												#
#  Luca Srdjenovic Et Axel Bento Da Silva		#
#												#
#  29 janvier 2018								#
#  lex.py										#
#################################################
import ply.lex as lex

reserved_words = (
    # Reserved tokens
    'while',
    'print',
    'if',
    'type',
    'for',
    # 'sub',
    'else',
)

tokens = (
             # Difficult tokens
             'NUMBER_INT',
             'NUMBER_FLOAT',
             'IDENTIFIER',
             'STRING',

             # caracter tokens
             'SEMI_COLON',
             'LEFT_PAREN',
             'RIGHT_PAREN',
             'LEFT_BRACE',
             'RIGHT_BRACE',
             'ASSIGNATION',
             'GREATER',
             'LESS',
             'EQUAL',
             'NOT_EQUAL',
             'GREATER_EQUAL',
             'LESS_EQUAL',
             'PLUS',
             'MINUS',
             'TIMES',
             'DIVISION',
             'MODULO',
             'EQUAL_PLUS',
             'EQUAL_MINUS',
             'EQUAL_TIMES',
             'EQUAL_DIV',
         ) + tuple(map(lambda s: s.upper(), reserved_words))

# caractères
t_SEMI_COLON = r';'
t_LEFT_PAREN = r'\('
t_RIGHT_PAREN = r'\)'
t_LEFT_BRACE = r'{'
t_RIGHT_BRACE = r'}'
t_ASSIGNATION = r'='
t_GREATER = r'>'
t_LESS = r'<'
t_EQUAL = r'=='
t_NOT_EQUAL = r'!='
t_GREATER_EQUAL = r'>='
t_LESS_EQUAL = r'<='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVISION = r'/(?!\*)'
t_MODULO = r'%'
t_EQUAL_PLUS = r'\+='
t_EQUAL_MINUS = r'-='
t_EQUAL_TIMES = r'\*='
t_EQUAL_DIV = r'/='


# Nombre réel
def t_NUMBER_FLOAT(t):
    r'\d+(\.\d+)+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Line %d: Problem while parsing %s!" % (t.lineno, t.value))
        t.value = 0
    return t


# Nombre entier
def t_NUMBER_INT(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Line %d: Problem while parsing %s!" % (t.lineno, t.value))
        t.value = 0
    return t


# Identifiant commençant par un '$' ou mot réservé ou nom de fonction
def t_IDENTIFIER(t):
    r'(?:\$.?[a-zA-Z_][a-zA-Z0-9_]*|[A-Za-z_][\w]*)'
    if t.value in reserved_words:
        t.type = t.value.upper()
    return t


# Chaine de caractère entre guillemet ou double guillement (langage perl)
def t_STRING(t):
    r'(?:"[^\n\\]*"|\'[^\n\\]*\')'

    return t


# Pour les commentaires, il faut un '#' pour écrire un commentaire
def t_COMMENT(t):
    r'\#.*'
    t.lexer.lineno += t.value.count(t.value)
    pass


# Pour les sauts de ligne
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# pour les espaces ou tabulations
def t_WHITE_SPACE(t):
    r'[ \t\n]+'
    pass


def t_error(t):
    print("Illegal character '%s'" % repr(t.value[0]))
    t.lexer.skip(1)


lex.lex()

# MAIN
if __name__ == "__main__":
    import sys

    prog = open(sys.argv[1]).read()

    lex.input(prog)

    while 1:
        tok = lex.token()
        if not tok: break
        print("line %d: %s(%s)" % (tok.lineno, tok.type, tok.value))
