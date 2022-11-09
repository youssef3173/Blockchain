from time import time
import hashlib
import json



"""
A block:
    - identifier
    - previous_hash
    - time
    - transaction:
        - sender
        - receiver
        - data/amount
    - proof
"""



class BlockChain():
    def __init__(self):
        self.chain = []

        # create the genesis block:
        genesis_block = {
            'index': 1,
            'previous_hash': 0,
            'timestamp': time(),
            'transactions': {"sender":0,
                            "recient":0,
                            "data":0,
                            },
        }
        proof = self.proof_of_work( genesis_block)
        genesis_block['proof'] = proof
        self.chain.append( genesis_block)


    def hash( self, block ):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256( block_string).hexdigest()       


    def add_block(self, sender, recipient, amount, previous_hash=None):
        # creates a new block in the blockchain
        block = {
            'index': len(self.chain)+1,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
            'timestamp': time(),
            'transactions': {"sender":sender,
                            "recient":recipient,
                            "data":amount,
                            },
        }

        proof = self.proof_of_work( block)
        block['proof'] = proof

        # add the block to the chain:
        self.chain.append(block)




    def proof_of_work(self, block, precision = 3):
        # Proof of work: Hash( { block, proof}) leading 3 zeros
        block_string = json.dumps(block, sort_keys=True)

        proof = 0
        guess = ( block_string + f'{proof}' ).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        while guess_hash[:3] != "000":
            proof += 1
            guess = ( block_string + f'{proof}' ).encode()
            guess_hash = hashlib.sha256(guess).hexdigest()


        return proof



if __name__ == '__main__':
    # initiate the Blockchain
    blockchain = BlockChain()
    
    blockchain.add_block( sender="aaa123", recipient="bbb456", amount=1.2345 )
    blockchain.add_block( sender="ccc123", recipient="ddd456", amount=2.3 )

    print( blockchain.chain )


