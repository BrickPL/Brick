import ply.lex as lex

#Initializing tokens
#TODO Add rest of tokens
tokens = (
    'BLOCKCHAIN',
    'ID', # only one ID is needed, difference between ids will be specified in parser
    'ASSIGN',
    'LBRACKET',
    'RBRACKET',
    'TYPEASSIGN',
    'TYPE',
    'SEPARATOR',
    'ADD',
    'LPARENTH',
    'RPARENTH',
    'NUMBER',
    'PRINT',
    'JSON'
    )

#Declare action for each token
#TODO Declare actions for tokens

t_ignore = r' \t'
t_BLOCKCHAIN = r'blockchain'
t_ASSIGN = r'='
t_LBRACKET = r'\{'
t_RBRACKET = r'\}'
t_TYPEASSIGN = r':'
#figure out what to do with TYPE, should be a string. Possible just use ID
t_SEPARATOR = r','
t_LPARENTH = r'\('
t_RPARENTH = r'\)'


reserved = {
    'blockchain' : 'BLOCKCHAIN',
    'add' : 'ADD',
    'print' :'PRINT'
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




