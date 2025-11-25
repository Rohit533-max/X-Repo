#a class whose constructor creates an initial emply list(to store our blockchain), and antoher to store the transictions

#creating the first block which has no predecessors, the seed block
import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid4

from flask import Flask
from flask.json import jsonify

class Blockchain(object):

    def __init__(self):
        self.chain = []
        self.current_transactions = []

        #creating the seed block
    def new_block(self,proof,previous_hash = None):
        """
        Create a new block in the blockchain
        :param proof : <int> the Proof given by proof of Work algorithm
        :param previous_hash: (optional) <str> hash of previous block
        :return : <dict> New block
        """
        block ={
            'index' : len(self.chain) +1,
            'timestamp': time(),
            'transactions':self.current_transactions,
            'proof':proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        #reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block 

    def new_block(self):
        #create a new Block and adds it to the chain 
        pass
    "We need a way of adding transactions to a block to our new transactions function"
    
    def new_transaction(self, sender, receiver, amount):
        """
        Creates a new transaction to go into the next mined Block
        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the Block that will hold this transaction
        """
        self.current_transactions.append({
            'sender' :sender,
            'receiver' : receiver,
            'amount' : amount,
        })
        return self.last_block['index'] + 1
    @staticmethod
    def hash(block):
        #hashes a block
        """
        Docstring for hash
        
        Creates a SHA-256 hash of a Block
        :param block : <dict>block
        :return : <str>
        """
        #To ensure that the dictionary is ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    @property
    def last_block(self):
        #returns the last block in the chain
        return self.chain[-1]
    #here how a single block looks like
    block = {
        'index' : 1,
        'timestamp' : 1506057125.900786, #one dig change
        'transactions' : [
            {
                'sender' : "8527147fe1f5426f9dd545de4b27ee00",
                 'receiver' : "a77f5cdfa2934df3954a5c7c7da5df1f",
                 'amount' : 5,

            }
        ],
        'proof' : 324984774000,
        'previous_hash' :"a77f5cdfa2934df3954a5c7c7da5df1f",
        #each block within itself contain the hash of its previous block       
    }
    def proof_of_work(self,last_proof):
        """
        Simple proof of work algorithm:
        -Find a number p' in such that hash(pp') contains leading 4 zeroes, where p is the preious p'
        - p is the previous proof
        """
#Our blockchain as an API

#Instantiate our Node
app = Flask(__name__)

#Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

#instaniate the blockchain
blockchain =  Blockchain()

@app.route('/mine', methods = ['GET'])
def mine():
    return "We'll mine a new block"

@app.route('/transactions/new', methods =['POST'])
def new_transaction():
    return "We'll add a new transaction"

@app.route('/chain', methods =['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length':len(blockchain.chain),
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port =5000)

