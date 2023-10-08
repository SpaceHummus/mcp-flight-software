import os
import hashlib
import random
import string
from pathlib import Path

# Determine folder in which this file is present
CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
big_file_path = Path(CURRENT_FOLDER + "/" + "bit_error_rate_random.bin")
hash_file =  = Path(CURRENT_FOLDER + "/" + "hash.txt")

def _create_tmp_file(file_path, size_gb=1):
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            # Generate random data
            random_data = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size_gb * 1024 * 1024 * 1024))
            f.write(random_data.encode())

def _compute_hash(file_path, hash_algorithm='sha256'):
    hasher = hashlib.new(hash_algorithm)
    with open(file_path, 'rb') as f:
        # Read the file in chunks to avoid loading the entire file into memory
        chunk_size = 8192
        while chunk := f.read(chunk_size):
            hasher.update(chunk)
    return hasher.hexdigest()

def update_hash():
    try:
        _create_tmp_file(big_file_path)
        h = _compute_hash(big_file_path)
        
        with open(hash_file, 'w') as file:
            f.write(h)
    
    except Exception as e:
        print(e)
        return 0
  
def read_hash():
     try:
        # Reading from the file
        with open(hash_file, 'r') as file:
            h = f.read()
            
        # Remove the file, so that it will be re-computed
        os.remove(hash_file)
        
        return h
            
    except Exception as e:
        # No file, or file has an issue start from 0
        return "Error"

# Example usage
if __name__ == "__main__":
    update_hash()
    print(read_hash())