import hashlib
from operator import index, truediv
import string
import time
import random

i = 5
Difficulty = 4
attacker_precentage = 600
transaction_list = ["Bassiony Sends Alice $500 ", "Hafez sends Bob $100 ",
                    "Sab3 sends Hafez $670 ", "Bassiony sends Bob $170 ",
                    "Bob sends Alice $608 ", "Osama sends Ahmed $120 ",
                    "Bassiony sends Nagah $150 ", "Nagah sends Hafez $30 ",
                    "Bassiony sends Ali $1570 ", "Ahmed sends Hafez $350 ",
                    "Alice sends Sab3 $100 ", "Sab3 sends Hafez $800 ",
                    "Alice sends Osama $1500 ", "Hafez Sends Alice $1200 "]



class Block:

    def __init__(self, index, transaction_lst, timestamp, previousHash):

        self.index = str(index)
        self.transactions = transaction_lst
        self.timestamp = timestamp
        self.prevHash = previousHash
        self.proof = self.calculate_nonce()
        self.TotalData = self.index + \
            " , " + self.transactions + " , " + self.timestamp + \
            " , " + self.prevHash + " , " + self.proof
        self.block_hash = self.compute_hash()

    def calculate_nonce(self):

        proof=0
        Found = False
        while Found == False:            
            blockData = str(self.index) + " , " + self.transactions + " , " + \
                str(self.timestamp) + " , " + \
                self.prevHash + " , " + str(proof)
            Hash = hashlib.sha256(blockData.encode()).hexdigest()
            if Hash.startswith('0' * Difficulty):
                Found = True
                return str(proof)
            else:
                proof+=1
        return -1

    def compute_hash(self):
        return hashlib.sha256(self.TotalData.encode()).hexdigest()

    
class BlockChain:
    #constructor
    def __init__(self):
        self.unconfirmed_transactions = []
        self.array = []
        self.create_genesis_block()
    #first block in the blockchain
    def create_genesis_block(self):
        genesis_block = Block("0", "", str(time.time()), "0")
        self.array.append(genesis_block)

    # Get the last block in the blockchain
    def get_previous_block(self):
        return self.array[-1]
    # get the hash of the last block in the blochain
    def last_hash(self):
        return ((self.get_previous_block()).block_hash)

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    def get_unconfirmed_transaction(self):
        t = self.unconfirmed_transactions
        self.unconfirmed_transactions = []
        return t

    def is_valid_hash(self, block, block_hash):
        return (block_hash.startswith('0' * Difficulty) and
                block_hash == block.compute_hash())

    # add block to blockchain
    def add_block(self, block, hash):
        """
        * Checking if the proof is valid.
        * The previous_hash referred in the block and the hash of latest block
          in the chain match.
        """
        previous_hash = (self.last_hash())
        if previous_hash != block.prevHash:
            self.unconfirmed_transactions = []
            return False, block.transactions

        if not self.is_valid_hash(block, hash):
            return False

        self.array.append(block)
        return True

    def mining(self, prev_hash):
        if not len(self.unconfirmed_transactions):
            return False
        time_1=time.time()
        transaction = check_transaction(self.unconfirmed_transactions)
        last = self.get_previous_block()
        last_hash = prev_hash
        timee = time.time()
        index = int(last.index) + 1
        new_block = Block(str(index), transaction,
                           str(timee), last_hash)
        hash = new_block.block_hash
        x = self.add_block(new_block, hash)
        time_2=time.time()
        while((time_2-time_1)<1):
            time_2=time.time()
        if x:
            self.unconfirmed_transactions = []
            return new_block.index, True
        else:
            return new_block, False


class Branch:
    def __init__(self, index):
        self.array = []
        self.index = int(index)
    # Get the last block in the branch
    def get_previous_block(self):
        return self.array[-1]
    # get the hash of the last block in the branch
    def prev_hash(self):
        return ((self.get_previous_block()).block_hash)

    def is_valid_hash(self, block, block_hash):
        return (block_hash.startswith('0' * Difficulty) and
                block_hash == block.compute_hash())

    # Function that add block to a chain
    def add_block(self, block, hash):
        """
        * Checking if the proof is valid.
        * The previous_hash referred in the block and the hash of latest block
          in the chain match.
        """
        if len(self.array) > 0:
            previous_hash = block.prevHash
            if previous_hash != block.prevHash:
                return False

            if not self.is_valid_hash(block, hash):
                return False

            self.array.append(block)
            return True
        else:
            self.array.append(block)
            return True

    def mining(self, transaction, prev_hash):
        if len(self.array) == 0:
            index = self.index
            transactionn = check_transaction(transaction)
            timee = time.time()
            new_block = Block(str(index), transactionn,
                               str(timee), prev_hash)
            hash = new_block.block_hash
            x = self.add_block(new_block, hash)
        else:
            last = self.get_previous_block()
            last_hash = prev_hash
            timee = time.time()
            transactionn = check_transaction(transaction)
            index = int(last.index) + 1
            new_block = Block(str(index), transactionn,
                               str(timee), last_hash)
            hash = new_block.block_hash
            x = self.add_block(new_block, hash)
        if x:
            self.unconfirmed_transactions = []
            return new_block.index, True
        else:
            return new_block, False

    # choose the longest branch
    def choose_longest_branch(self, branch2):
        last_index_in_branch1 = self.get_previous_block().index;
        last_index_in_branch2 = branch2.get_previous_block().index;
        
        if (int(last_index_in_branch1) > int(last_index_in_branch2)):
            return self
        else:
            return branch2
        

# generate random transactions
def generation():
    transaction = ''.join(random.choice(transaction_list))
    return transaction


def check_transaction(transaction):
    if len(transaction) > 1:
        concat_tr = ''
        for x in range(len(transaction)):
            concat_tr += transaction[x]
            if x != (len(transaction)-1):
                concat_tr += "-"
    transaction = concat_tr
    return concat_tr

def append_longest_branch(branch,main_blockchain):
        #check if the last element in main chain needs to be replaced
        start_index=int(branch.index)
        if(((len(main_blockchain.array))-1) == start_index):
            main_blockchain.array[start_index]=branch.array[0]
            for x in range(1,len(branch.array)):
                main_blockchain.array.append(branch.array[x])
        else:
            for x in range (len(branch.array)):
                main_blockchain.array.append(branch.array[x]);

# First for loop to generate the main Block:
main_chain = BlockChain()
size_before_branching=4
timme=0
for x in range(size_before_branching):
    t1 = generation()
    main_chain.add_new_transaction(t1)
    t2 = generation()
    main_chain.add_new_transaction(t2)
    t3 = generation()
    main_chain.add_new_transaction(t3)
    prev_hash_main = main_chain.last_hash()
    time1=time.time()
    main_chain.mining(prev_hash_main)
    time2=time.time()
    timme=timme+(time2-time1)
Avg_time=timme/size_before_branching

print("Chain before branching is: ")
for x in main_chain.array:
    print(x.__dict__)
    # print(x.block_hash)

prev_hash_attacker = prev_hash_main
prev_hash_others = main_chain.last_hash()
attacker_index = len(main_chain.array) - 1
other_index = len(main_chain.array)
c1 = Branch(attacker_index)
c2 = Branch(other_index)

for x in range(5):
    for y in range(i):
        x = random.randint(0, 1000)
        t1 = generation()
        main_chain.add_new_transaction(t1)
        t2 = generation()
        main_chain.add_new_transaction(t2)
        t3 = generation()
        main_chain.add_new_transaction(t3)
        if x < attacker_precentage:
            transaction = main_chain.get_unconfirmed_transaction()
            c1.mining(transaction, prev_hash_attacker)
            prev_hash_attacker = c1.prev_hash()
        else:
            transaction = main_chain.get_unconfirmed_transaction()
            c2.mining(transaction, prev_hash_others)
            prev_hash_others = c2.prev_hash()


longest= c1.choose_longest_branch(c2)
append_longest_branch(longest,main_chain)

print("Longest chain is ")
for x in (c1.choose_longest_branch(c2)).array:
    print(x.__dict__)

print("Chain after choosing normal branch becomes ")
for x in main_chain.array:
    print(x.__dict__)

print("Average time taken by a block")
print(Avg_time)
