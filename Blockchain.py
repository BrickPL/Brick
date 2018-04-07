class Blockchain(object):
    def __init__(self, p):
        self.chain = []
        self.current_data = []
        self.datatypes = p

    def new_block(self):
        # Creates a new Block and adds it to the chain
        pass

    def new_data(self, p):
        # Adds new data to the list of data
        # Receives p, an array of data sent by the user.
        # This method checks each element of p if their data types fit  the defined data types
        # If they fit, then the data is added to the list of current_data
        pass

    @staticmethod
    def hash(block):
        # Hashes a Block
        pass

    @property
    def last_block(self):
        # Returns the last Block in the chain
        pass