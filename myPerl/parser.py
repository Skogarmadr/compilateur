#################################################
#  Projet Compilateur INF3dlm-a					#
#												#
#  Luca Srdjenovic Et Axel Bento Da Silva		#
#												#
#  29 janvier 2018								#
#  parser.py									#
#################################################


import ply.yacc as yacc

from lex import tokens
import AST

vars = {}


#
# Structure de PROGRAMME
#
def p_programme_statement(p):
    ''' programme : statement '''
    p[0] = AST.ProgramNode(p[1])


def p_programme_recursive(p):
    ''' programme : statement programme '''
    p[0] = AST.ProgramNode([p[1]] + p[2].children)


# ----------------------------------------

#
# Structure de PROGRAMME
#
def p_statement(p):
    ''' statement : statement_semicolon
        | statement_expression
        | statement_print
        | statement_assignation
        | statement_iteration
        | statement_conditional'''
    p[0] = p[1]


def p_statement_semicolon(p):
    '''statement_semicolon : SEMI_COLON'''
    p[0] = None


def p_statement_expression(p):
    '''statement_expression : expression SEMI_COLON'''
    p[0] = p[1]


# ----------------------------------------

#
# Structure de STATEMENT PRINT
#
def p_statement_print(p):
    ''' statement_print : PRINT expression SEMI_COLON '''
    p[0] = AST.PrintNode(p[2])


# ----------------------------------------

#
# Structure de STATEMENT AVEC ASSIGNATION
#
def p_statement_assignation(p):
    ''' statement_assignation : expression_assignation SEMI_COLON'''
    p[0] = p[1]


def p_expression_assignation(p):
    '''expression_assignation : IDENTIFIER assignation_operator expression '''
    p[0] = AST.AssignNode([AST.TokenNode(p[1]), p[3]])


def p_assignation_operator(p):
    '''assignation_operator : ASSIGNATION
        | EQUAL_PLUS
        | EQUAL_MINUS
        | EQUAL_TIMES
        | EQUAL_DIV '''
    p[0] = p[1]


# ----------------------------------------

#
# Structure de STATEMENT ITERATION AVEC WHILE ET FOR
#
def p_statement_iteration_while(p):
    ''' statement_iteration : WHILE LEFT_PAREN expression RIGHT_PAREN LEFT_BRACE programme RIGHT_BRACE '''
    p[0] = AST.WhileNode([p[3], p[6]])


def p_statement_iteration_for(p):
    ''' statement_iteration : FOR LEFT_PAREN statement_expression statement_expression expression RIGHT_PAREN LEFT_BRACE programme RIGHT_BRACE '''
    p[0] = AST.ForNode([p[3], p[4], p[5], p[8]])


# ----------------------------------------

#
# Structure de STATEMENT CONDITIONAL AVEC IF ET ELSE
#
def p_statement_conditional_if(p):
    ''' statement_conditional : IF LEFT_PAREN expression RIGHT_PAREN LEFT_BRACE programme RIGHT_BRACE %prec IFX '''
    p[0] = AST.IfNode([p[3], p[6]])


def p_statement_conditional_if_else(p):
    ''' statement_conditional : IF LEFT_PAREN expression RIGHT_PAREN LEFT_BRACE programme RIGHT_BRACE ELSE LEFT_BRACE programme RIGHT_BRACE '''
    p[0] = AST.IfNode([p[3], p[6], p[10]])


# ----------------------------------------

#
# Structure de EXPRESSION
#
def p_expression_int(p):
    '''expression : NUMBER_INT'''
    p[0] = AST.TokenNode(p[1])


def p_expression_float(p):
    '''expression : NUMBER_FLOAT'''
    p[0] = AST.TokenNode(p[1])


def p_expression_string(p):
    '''expression : STRING'''
    p[0] = AST.TokenNode(p[1])


def p_expression_identifier(p):
    '''expression : IDENTIFIER'''
    p[0] = AST.TokenNode(p[1])


def p_expression_paren(p):
    '''expression : LEFT_PAREN expression RIGHT_PAREN '''
    p[0] = p[2]


def p_expression_operator(p):
    '''expression : expression PLUS expression
            | expression MINUS expression
            | expression TIMES expression
            | expression DIVISION expression
            | expression MODULO expression'''
    p[0] = AST.OpNode(p[2], [p[1], p[3]])


def p_expression_minus(p):
    ''' expression : MINUS expression %prec UMINUS '''
    p[0] = AST.OpNode(p[1], [p[2]])


# ----------------------------------------

#
# Structure de COMPARAISON D'EXPRESSION
#
def p_expression_comparison(p):
    ''' expression : expression comparison_operator expression '''
    p[0] = AST.CompareNode(p[2], [p[1], p[3]])


def p_comparison_operator(p):
    ''' comparison_operator : GREATER
        | LESS
        | EQUAL
        | NOT_EQUAL
        | GREATER_EQUAL
        | LESS_EQUAL '''
    p[0] = p[1]


# ----------------------------------------

#
# Structure de TYPE
#
def p_expression_type(p):
    ''' expression : type '''
    p[0] = p[1]


def p_type(p):
    ''' type : TYPE LEFT_PAREN expression RIGHT_PAREN'''
    p[0] = AST.TypeNode(p[3])


# ----------------------------------------

def p_error(p):
    if p:
        print("Syntax error in line %d" % p.lineno)
        yacc.errok()
    else:
        print("Sytax error: unexpected end of file!")


precedence = (
    ('left', 'PLUS'),
    ('left', 'MINUS'),
    ('left', 'TIMES'),
    ('left', 'DIVISION'),
    ('left', 'MODULO'),
    ('right', 'UMINUS'),
    ('nonassoc', 'IFX'),
    ('nonassoc', 'ELSE'),
)


def parse(program):
    return yacc.parse(program)


yacc.yacc(outputdir='generated')

if __name__ == "__main__":
    import sys

    prog = open(sys.argv[1]).read()
    result = yacc.parse(prog)

    if result:
        print(result)

        import os

        graph = result.makegraphicaltree()
        name = os.path.splitext(sys.argv[1])[0] + '-ast.pdf'
        graph.write_pdf(name)
        print("wrote ast to", name)
    else:
        print("Parsing returned no result!")
