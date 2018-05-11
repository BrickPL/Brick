import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request

class Blockchain(object):

    def __init__(self, param):
        self.chain = []
        self.current_data = []
        self.parameters = param
        self.new_block(previous_hash=1, proof=100)

        for data in param:
            print(data)



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
            print(data[datum])
            print(t)

            t[datum] = data[datum]
        self.current_data.append(t)
        return self.last_block['index'] + 1

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


