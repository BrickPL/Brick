import ply.lex as lex
import json
import requests
from flask import Flask, jsonify, request
from uuid import uuid4



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
    'STR'
    ]
reserved = {
    'blockchain' : 'BLOCKCHAIN',
    'add': 'ADD',
    'print':'PRINT',
    'printdata' : 'PRINTDATA',
    'run': 'RUN',
    'mine': 'MINE',
    'str': 'STR', #To be able to validate strings the type has to be written as 'str"
    'int': 'INT',
    'long': 'LONG',
    'float': 'FLOAT',
    'List': 'LIST',
    'Tuple': 'TUPLE',
    'dict': 'DICT',
    'export': 'EXPORT'
}

types = {
    'str': 'STR',
    'int': 'INT',
    'long': 'LONG',
    'float': 'FLOAT',
    'List': 'LIST',
    'Tuple': 'TUPLE',
    'dict': 'DICT'
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


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_STR(t):
    r'"(?:[^\\]|(?:\\.))*"'
    t.type = reserved.get(t.value, 'STR')
    t.value = t.value[1:-1]
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

lexer = lex.lex()


import ply.yacc as yacc
# So I think that we have to store blockchains in a dict
from Blockchain import Blockchain


#------------------NODE---------------------------------------------

app = Flask(__name__)


def run(blockchain):
    global block
    block = blockchain
    app.run(host='0.0.0.0', port=5000)

@app.route('/chain', methods=['GET'])
def full_chain():
    global block
    response = {
        'chain': block.chain,
        'length': len(block.chain),
    }
    return jsonify(response), 200

@app.route('/data/new', methods=['POST'])
def new_datas():
    global block
    values = request.get_json()
    print(values)
    required = block.parameters
    if not all(k in values for k in required):
        return 'Missing values', 400

    index = block.new_data(values)

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/mine', methods=['GET'])
def mine():
    global block
    last_block = block.last_block
    last_proof = last_block['proof']
    proof = block.proof_of_work(last_proof)

    previous_hash = block.hash(last_block)
    new = block.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': new['index'],
        'transactions': new['data'],
        'proof': new['proof'],
        'previous_hash': new['previous_hash'],
    }
    return jsonify(response), 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    global block
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        block.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(block.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    global block
    replaced = resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': block.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': block.chain
        }

    return jsonify(response), 200

def resolve_conflicts(self):
    global block
    neighbours = block.nodes
    new_chain = None

        # We're only looking for chains longer than ours
    max_length = len(block.chain)

        # Grab and verify the chains from all the nodes in our network
    for node in neighbours:
        response = requests.get(f'http://{node}/chain')

        if response.status_code == 200:
            length = response.json()['length']
            chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
            if length > max_length and block.valid_chain(chain):
                max_length = length
                new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
    if new_chain:
        block.chain = new_chain
        return True

    return False

#-------------END-NODE--------------------------------------


blockchains = {}

# Here we create a new blockchain, extracting the attributes and storing the blockchain in the dict
def p_new_block(p):
    '''blockchain : BLOCKCHAIN ID ASSIGN LBRACKET attributes RBRACKET
                    | ADD ID SEPARATOR LPARENTH new_atts RPARENTH
                    | PRINT ID
                    | RUN ID
                    | MINE ID
                    | EXPORT ID
                    | PRINTDATA ID'''
    if p[1] == 'blockchain':
        #TODO: Check if parameters have correct types
        try:
            if(validate(p[5])):

                blockchains[p[2]] = Blockchain(p[5])
                print("Blockchain created.")

            else:
                print("Blockchain was not created")
        except ValueError:
            print("Can't have same parameter name")

    elif p[1] == 'add':
        data = p[5]
        data_to_add = {}
        for datum in data:
            datum_type = blockchains.get(p[2]).parameters.get(datum)
            if type(data[datum]).__name__ == datum_type:
                data_to_add[datum] = data[datum]
            elif datum_type == None :
                print("The new data was not added because",datum,"was not previously defined as an attribute.")
            else:
                print("The new data was not added because the type of the value do not match the type of", datum,".")
        if (data_to_add == data and data_to_add.__len__() == len(blockchains.get(p[2]).parameters)):
            blockchains.get(p[2]).new_data(data)
            print("Data was added")
        else:
            print("Some attributes are missing.")




    elif p[1] == 'print':
        p[0] = blockchains.get(p[2]).current_chain()
        print(p[0])

    elif p[1] == 'printdata':
        p[0] = blockchains.get(p[2]).current_chaindata()
        print(p[0])

    elif p[1] == 'run':
        run(blockchains[p[2]])

    elif p[1] == 'mine':
        p[0] = blockchains[p[2]].mine()
        print(p[0])

    elif p[1] == 'export':
        with open(p[2] + '.json', 'w') as outfile:
            json.dump(blockchains[p[2]].chain, outfile)


# Here we extract the attributes

def p_types(p):
    '''type : STR
            | INT
            | LONG
            | FLOAT
            | LIST
            | TUPLE
            | DICT'''
    p[0] = p[1]


def p_attribute(p):
    '''attribute : ID TYPEASSIGN type'''
    p[0] = {p[1]: p[3]}



def p_attributes1(p):
    '''attributes : attribute'''
    p[0] = p[1]

def p_attributes2(p):
    '''attributes : attributes SEPARATOR attribute'''
    p[0] = p[1]
    x = list(p[3].keys())

    if x[0] in p[0].keys():
        raise ValueError('EXCEPTION BRO u cant have the same paramater name idiot')

           
    else:
        p[0].update(p[3])

def p_new_att(p):
    '''new_att : ID TYPEASSIGN STR
               | ID TYPEASSIGN NUMBER'''
    p[0] = {p[1]: p[3]}


def p_new_atts1(p):
    '''new_atts : new_att'''
    p[0] = p[1]

def p_new_atts2(p):
    '''new_atts : new_atts SEPARATOR new_att'''
    p[0] = p[1]
    p[0].update(p[3])

#Verifies if each attribute has a valid type.
# Returns false if at least one is not valid,
# returns true otherwise.
def validate(p):
    for attribute in p:
        if not(p[attribute] in types):
            return False
        else: continue
    return True






parser = yacc.yacc()

while True:
    try:
        s = input('Brick > ')   # Use raw_input on Python
    except EOFError:
        break
    try:
        parser.parse(s)
    except ValueError:
        print("Can't have same parameter name")





node_identifier = str(uuid4()).replace('-', '')










