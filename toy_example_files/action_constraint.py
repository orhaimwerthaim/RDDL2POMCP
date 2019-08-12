from __future__ import division
from sympy import *
from sympy.parsing.sympy_parser import parse_expr
import copy

PredicateToSymbol = {}
SymbolAssignment = {}
    #add to dictionary this predicate symbol
def definePredicate(predicate, value):
    symbol = 'a' + str(abs(hash(str(predicate)))) + 'a'
    PredicateToSymbol[predicate] = symbol
    SymbolAssignment[symbol] = value


def validateExp(exp):
    exp = exp.replace('\'', '').replace(',', '').replace(' ', '')#removing ',' and '\''
    exp = exp[exp.find('>>') + 2:]#removing the string before '>>', because we always only check for action that are True one the left side of '>>', so the result is the evaluation of the right side
    for key,value in PredicateToSymbol.items():
        symbols(value)
        normalKey = str(key).replace('\'', '')[1:-1].replace(',', '').replace(' ', '')
        exp = exp.replace(normalKey,value)
    ex = parse_expr(exp)
    return ex.subs(SymbolAssignment)
    # print('validate action result:')
    # print('expression:{}' .format(exp))
    # print('result:{}' .format(ex.subs(SymbolAssignment)))


#input is a single action 'constraint' and a 'groundBy' expression that could be an action/fluent/non-fluent key
#will return a copy of the constraint after it is grounded with objects by 'groundBy', and willreturn the parameters not grounded because they were not in 'groundBy'
def groundContraint(constraint, groundBy):
    notGround = []
    con = copy.deepcopy(constraint)
    replace = {}

    #finds all the matches between 'groundBy' and 'constraint' parameters, build 'replace' dictionary
    for i in range(len(con)):
        if  con[i][0] == groundBy[0]:
            for j in range(len(con[i][1])):
                replace[con[i][1][j]] = groundBy[1][j]
            #con[i] = True #the groundBy is activated so it is now true in the grounded expression

#replace/ground the paremeters and saves ones not replaced/grounded
    parameters = con[0][1]
    for i in range(len(parameters)):
        if parameters[i][1] in replace:
            parameters[i][1] = replace[parameters[i][1]]
        else:
            notGround.append(parameters[i])

    #ground all of the constraint
    for i in range(1, len(con)):
        if con[i] != True and len(con[i]) > 1: #size 1 tuples are for operators and True is assigned for the groundBy
            for z in range(len(con[i][1])):
                if con[i][1][z] in replace:
                    con[i][1][z] = replace[con[i][1][z]]
    return con, notGround

def constraintToStr(constraint):
    exp = ''
    for i in range(len(constraint)):
        for j in range(len(constraint[i])):
            exp += str(constraint[i][j])
    exp = exp.replace('[','(').replace(']',')')
    return exp

def validateGroundedConstraint(constraint,state):
    del constraint[0] #it is grounded so we dont need the paremeters defintions
    a = constraintToStr(constraint)
    return validateExp(a)
    # for i in range(len(constraint)):
    #     if constraint[i] != True and len(constraint[i]) > 1:
    #         tuple2 = (constraint[i][0], tuple(constraint[i][1]))
    #         if tuple2 in state:
    #             constraint[i] = state[tuple2]
    # #handle '(',')'
    # for i in reversed(range(len(constraint))):
    #     if constraint[i] == '~':
    #         constraint[i] = not constraint[i + 1]
    #         del constraint[i + 1]

def handleLogicalExpWithoutBrackets(exp):
    # handle '~'negate
    for i in reversed(range(len(exp))):
        if exp[i] == '~':
            exp[i] = not exp[i + 1]
            del exp[i + 1]
