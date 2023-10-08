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

def hash_large_file():
    try:
        
        # If file doesn't exist, already - create it
        if not os.path.exists(big_file_path):
            _create_file()
            
        # If it does, hash it
        h = _compute_hash(big_file_path)
        return h
    
    except Exception as e:
        print(e)
        return "-"

# Example usage
if __name__ == "__main__":
    if True:
        print(hash_large_file())
    else:
        print("Creating the large file")
        start_time = time.time()
        _create_file()
        elapsed_time = time.time() - start_time
        print("Creating file took {elapsed_time}")
        
        print("Computing Hash on it")
        start_time = time.time()
        print(_compute_hash(big_file_path))
        elapsed_time = time.time() - start_time
        print("Hashing the file took {elapsed_time}")