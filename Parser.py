import ply.yacc as yacc
#So I think that we have to store blockchains in a list
from Blockchain import Blockchain

blockchains = []


def p_new_block(p):
    '''blockchain : ID ASSIGN LBRACKET attribute RBRACKET'''
    vars[p[1]] = Blockchain(p[4])

def p_attributes(p):
    '''attributes: ID SEPARATOR ID
                | ID SEPARATOR attributes'''

