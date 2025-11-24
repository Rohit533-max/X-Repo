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
    #here how a single block looks like
    block = {
        'index' : 1,
        'timestamp' : 1506057125.900786, #one dig change
        'transactions' : [
            {
                'sender' : "8527147fe1f5426f9dd545de4b27ee00",
                 'receiver' : "a77f5cdfa2934df3954a5c7c7da5df1f",

            }
        ],
        'proof' : 324984774000,
        'previous_hash' :"a77f5cdfa2934df3954a5c7c7da5df1f",
    }
    