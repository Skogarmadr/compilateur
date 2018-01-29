#################################################
#  Projet Compilateur INF3dlm-a					#
#												#
#  Luca Srdjenovic Et Axel Bento Da Silva		#
#												#
#  29 janvier 2018								#
#  recInterpreter.py							#
#################################################

import AST
from AST import addToClass
from functools import reduce

operations = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y,
    '%': lambda x, y: x % y,
    '==': lambda x, y: x == y,
    '!=': lambda x, y: x != y,
    '<': lambda x, y: x < y,
    '>': lambda x, y: x > y,
    '>=': lambda x, y: x >= y,
    '<=': lambda x, y: x <= y,
}

types_tab = ["int", "float", "str"]

vars = {}


#
# Noeud du programme
#
@addToClass(AST.ProgramNode)
def execute(self):
    for c in self.children:
        c.execute()


#
# Noeud de fin
#
@addToClass(AST.TokenNode)
def execute(self):
    if isinstance(self.tok, str):
        try:
            if vars[self.tok][0] is None:
                print("*** Attention : la variable %sn'a pas de type!" % self.tok)
        except IndexError:
            print("*** Attention: la variable %s est inconnu !" % self.tok)
            return "error"
        vars[self.tok][2] = True
        if vars[self.tok][1] is None:
            print("*** Attention:  la variable %s n'est pas utilisé !" % self.tok)
            vars[self.tok][1] = 0
            vars[self.tok][2] = False
        return vars[self.tok][1]
    return self.tok


#
# Noeud d'opération
#
@addToClass(AST.OpNode)
def execute(self):
    args = [c.execute() for c in self.children]

    if len(args) == 1:
        args.insert(0, 0)
    return reduce(operations[self.op], args)


#
# Noeud d'assignation
#
@addToClass(AST.AssignNode)
def execute(self):
    # On regarde si la variable e été déclaré
    if len(vars[self.children[0].tok]) == 1:
        vars[self.children[0].tok].append(self.children[1].execute())
        vars[self.children[0].tok].append(False)
    else:
        vars[self.children[0].tok].append(None)  # permet a l'interpreteur de verifier si la variable a ete declaree.
        vars[self.children[0].tok].append(self.children[1].execute())
        vars[self.children[0].tok].append(False)


#
# Noeud de comparaison
#
@addToClass(AST.CompareNode)
def execute(self):
    args = [c.execute() for c in self.children]

    if len(args) == 1:
        args.insert(0, 0)
    return reduce(operations[self.op], args)


#
# Noeud de print
#
@addToClass(AST.PrintNode)
def execute(self):
    print(self.children[0].execute())


#
# Noeud de loop while
#
@addToClass(AST.WhileNode)
def execute(self):
    while self.children[0].execute():
        self.children[1].execute()


#
# Noeud de loop for
#
@addToClass(AST.ForNode)
def execute(self):
    self.children[0].execute()
    while self.children[1].execute():
        self.children[3].execute()
        self.children[2].execute()


#
# Noeud de if
#
@addToClass(AST.IfNode)
def execute(self):
    if (len(self.children) < 2):
        if (self.children[0].execute()):
            self.children[1].execute()
    else:
        if (self.children[0].execute()):
            self.children[1].execute()
        else:
            self.children[2].execute()


#
# Noeud de pour check le type d'une variable
#
@addToClass(AST.TypeNode)
def execute(self):
    if self.children[0] in types_tab:
        if type(self.children[0]) is str:
            return "STRING"
        if type(self.children[0]) is int:
            return "INT"
        if type(self.children[0]) is float:
            return "FLOAT"
    else:
        return 'unknown type'


#
# Problème de compilation du code car problème de code python...
# Erreur circular dependecy non gérer
if __name__ == "__main__":
    from parser import parse
    import sys

    prog = open(sys.argv[1]).read()

    ast = parse(prog)
    print(ast)

    ast.execute()
