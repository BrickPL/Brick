import ply.lex as lex

#Initializing tokens
tokens = [
    'ID', # only one ID is needed, difference between ids will be specified in parser
    'ASSIGN',
    'LBRACKET',
    'RBRACKET',
    'TYPEASSIGN',
    'TYPE',
    'SEPARATOR',
    'LPARENTH',
    'RPARENTH',
    'NUMBER',
    'JSON'
    ]
reserved = {
    'blockchain' : 'BLOCKCHAIN',
    'add' : 'ADD',
    'print' :'PRINT'
}

tokens += list(reserved.values())
#Declare action for each token

t_ignore = r' \t'
t_ASSIGN = r'='
t_LBRACKET = r'\{'
t_RBRACKET = r'\}'
t_TYPEASSIGN = r':'
#figure out what to do with TYPE, should be a string. Possible just use ID
t_SEPARATOR = r','
t_LPARENTH = r'\('
t_RPARENTH = r'\)'


reserved = {
    'blockchain': 'BLOCKCHAIN',
    'add': 'ADD',
    'print':'PRINT'
    'mine': 'MINE'
}

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

lexer = lex.lex()


import ply.yacc as yacc
# So I think that we have to store blockchains in a dict
from Blockchain import Blockchain

blockchains = {}


# Here we create a new blockchain, extracting the attributes and storing the blockchain in the dict

def p_new_block(p):
    '''blockchain : BLOCKCHAIN ID ASSIGN LBRACKET attributes RBRACKET
                    | ADD ID SEPARATOR LPARENTH attributes RPARENTH
                    | PRINT ID
                    |MINE ID'''
    if p[1] == 'blockchain':
        #TODO: Check if parameters have correct types
        blockchains[p[2]] = Blockchain(p[5])
    elif p[1] == 'add':
        blockchains.get(p[2]).new_data(p[5])
    elif p[1] == 'print':
        p[0] = blockchains.get(p[2]).current_chain()
        print(p[0])

# Here we extract the attributes
def p_attribute(p):
    '''attribute : ID TYPEASSIGN ID
                | ID TYPEASSIGN NUMBER'''
    p[0] = {p[1]: p[3]}

def p_attributes1(p):
    '''attributes : attribute'''
    p[0] = p[1]

def p_attributes2(p):
    '''attributes : attributes SEPARATOR attribute'''
    p[0] = p[1]
    p[0].update(p[3])



parser = yacc.yacc()

while True:
    try:
        s = input('Brick > ')   # Use raw_input on Python
    except EOFError:
        break
    parser.parse(s)

