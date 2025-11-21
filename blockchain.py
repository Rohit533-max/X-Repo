#a class whose constructor creates an initial emply list(to store our blockchain), and antoher to store the transictions
class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

    def new_block(self):
        #create a new Block and adds it to the chain 
        pass
    def new_transaction(self):
        #add a new method to the list of transactions
        pass
    @staticmethod
    def hash(block):
        #hashes a block
        pass
    @property
    def last_block(self):
        #returns the last block in the chain
        pass
    