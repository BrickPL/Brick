import ply.yacc as yacc
#So I think that we have to store blockchains in a list
from Blockchain import Blockchain

blockchains = {}

#Here we create a new blockchain, extracting the attributes and storing the blockchain in the dict

def p_new_block(p):
    '''blockchain : ID ASSIGN LBRACKET attribute RBRACKET'''
    vars[p[1]] = Blockchain(p[4])


#Here we extract the attributes
def p_attributes(p):
    '''attribute: ID TYPEASSIGN ID
                | attribute SEPARATOR attribute'''
    p[0] = (p[1], p[3]) #returns a tuple that contains the name of the parameter and the type