import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid4
from urllib.parse import urlparse

from flask import Flask, jsonify, request

class Blockchain(object):

    def __init__(self, param):
        self.chain = []
        self.current_data = []
        self.parameters = param
        self.new_block(previous_hash=1, proof=100)
        self.nodes = set()


    def new_block(self, proof, previous_hash = None):
        # Creates a new Block and adds it to the chain
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'data': self.current_data,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.current_data = []
        self.chain.append(block)
        return block

    def new_data(self, data):
        # Adds new data to the list of data
        # Receives p, an array of data sent by the user.
        # This method checks each element of p if their data types fit  the defined data types
        # If they fit, then the data is added to the list of current_data
        t = {}
        for datum in data:
            type = self.parameters.get(datum)
            #TODO: check if the type sent is the same type as parameter
            #UPDATE: It was done in the 'add' section of the Brick class
            t[datum] = data[datum]

        self.current_data.append(t)
        return self.last_block['index'] + 1

    def type(self):
        return type

    def proof_of_work(self, last_proof):

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    @staticmethod
    def hash(block):
        # Hashes a Block
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        # Returns the last Block in the chain
        return self.chain[-1]

    def current_chain(self):
        return self.chain

    def current_chaindata(self):
        return self.chain

    def mine(self):
        last_block = self.chain[-1]
        last_proof = last_block['proof']
        proof = self.proof_of_work(last_proof)

        previous_hash = self.hash(last_block)
        new = self.new_block(proof, previous_hash)
        return new

    def register_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def valid_chain(self, chain):

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            if block['previous_hash'] != self.hash(last_block):
                return False

            if not self.valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True
