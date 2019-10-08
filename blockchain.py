import hashlib, json
from time import time
from uuid import uuid4
from flask import Flask

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create genesis block
        self.new_block(proof=100, previous_hash=1)
    
    def new_block(self, proof, previous_hash=None):
        '''
        Create a new Block and add it to the chain
        Parameters:
        - proof <int>: The proof given by the Proof of Work algorithm
        - previous_hash (optional) <str>: Hash of the previous block
        
        Return <dict>: New block
        '''

        block = {
            'index': len(self.chain)+1,
            'timestamp':time(),
            'transactions': self.current_transactions,
            'proof':proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }

        # Reset the current list of transactions
        self.current_transactions=[]

        self.chain.append(block)

        return block

    def new_transaction(self, sender, recipient, amount):
        '''
        Create a new transaction to go into the next mined Block
        Parameters:
        - sender <str>: Address of the sender
        - recipient <str>: Address of the recipient
        - amount <float>: Amount
        
        Return <int>: Index of the Block that will hold this transaction
        '''

        self.current_transactions.append({
            'sender':sender,
            'recipient':recipient,
            'amount':amount
        })

        return self.last_block['index']+1

    @staticmethod
    def hash(block):
        '''
        Create a SHA-256 hash of Block
        Parameters:
        - block <dict>: Block
        
        Return <str>
        '''

        # Order dictionary to ensure consistent Hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        
        return hashlib.sha256(block_string).hexdigest()
        
    @property
    def last_block(self):
        '''
        Return the last block in the chain
        '''
        return self.chain[-1]
    
    def proof_of_work(self, last_proof):
        '''
        POW algorithm: Find a number p' such that hash(pp') contains leading 4 zeroes, 
        where p is the previous proof, and p' is the new proof
        Parameters:
        - last_proof <int>

        Return <int>        
        '''

        proof = 0
        while self.valid_proof(last_proof, proof) is false:
            proof+=1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        '''
        Validate the proof as per POW algorithm. 
        Parameters:
        - last_proof <int>: previous proof
        - proof <int>: current proof

        Return <bool>: True if hash(last_proof & proof) has 4 leading zeroes
        '''

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4]=='0000'

