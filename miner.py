import hashlib
import time

def mine_block(block_number, transactions, previous_hash, difficulty_level):
    # The target: We need our hash to start with this many zeros
    target_prefix = '0' * difficulty_level
    
    print(f"⛏️ Mining Block {block_number} (Difficulty: {difficulty_level})...")
    
    # We will try up to 100 million different guesses
    for nonce in range(100000000):
        # 1. Combine all the data together into one long string
        text_to_hash = str(block_number) + transactions + previous_hash + str(nonce)
        
        # 2. Scramble it using SHA-256 encryption
        new_hash = hashlib.sha256(text_to_hash.encode()).hexdigest()
        
        # 3. Check if we won! Does it start with the required number of zeros?
        if new_hash.startswith(target_prefix):
            print(f"🎉 BLOCK MINED SUCCESSFULLY!")
            print(f"🎯 Winning Nonce (Guess): {nonce}")
            print(f"🔗 New Block Hash: {new_hash}")
            return new_hash

    print("❌ Failed to find a valid hash. Try increasing the max guess limit.")
    return None

# --- Let's run the miner! ---

# Fake transactions for our block
transactions = """
Alice pays Bob 5 BTC
Charlie pays Dave 2 BTC
"""

# The hash of the previous block in the chain (made up for this example)
previous_hash = "0000000xa036944e29568d0cff17edbe038f81208fecf9a66be9a2b8321c6ec7"

# Difficulty level = How many zeros the hash MUST start with. 
# WARNING: Changing this from 4 to 5 or 6 will make it take exponentially longer!
difficulty = 4 

# Start the timer
start_time = time.time()

# Run the mining function
mined_hash = mine_block(
    block_number=1, 
    transactions=transactions, 
    previous_hash=previous_hash, 
    difficulty_level=difficulty
)

# Stop the timer
end_time = time.time()
print(f"⏱️ Total time taken: {round(end_time - start_time, 2)} seconds")
