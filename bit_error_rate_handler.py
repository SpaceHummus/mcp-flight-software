import os
import hashlib
import random
import string
import time
from pathlib import Path
import array


# Determine folder in which this file is present
CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
big_file_path  = Path(CURRENT_FOLDER + "/" + "bit_error_rate_random.bin")
hash_file      = Path(CURRENT_FOLDER + "/" + "hash.txt")


def _create_file():
    # Create an array of unsigned bytes
    data = array.array('B', range(256))

    with open(big_file_path, 'wb') as file:
        # Write 1 GB of data
        for _ in range(1024 * 1024 * 1024 // len(data)):
            file.write(data)

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
        h = _compute_hash(big_file_path)
        
        with open(hash_file, 'w') as file:
            file.write(h)
    
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
    start_time = time.time()
    _create_file()
    end_time = time.time()
    print("Creating file took {elapsed_time}")
    
    start_time = time.time()
    print(_compute_hash(big_file_path))
    end_time = time.time()
    print("Hashing the file took {elapsed_time}")