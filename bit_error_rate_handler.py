import os
import hashlib
import random
import string
import time
from pathlib import Path

# Determine folder in which this file is present
CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
big_file_path  = Path(CURRENT_FOLDER + "/" + "bit_error_rate_random.bin")
hash_file      = Path(CURRENT_FOLDER + "/" + "hash.txt")

def _generate_random_bytes(size):
    return bytes([random.randint(0, 255) for _ in range(size)])

def _write_large_file(file_path, total_size, chunk_size):
    with open(file_path, 'wb') as file:
        for _ in range(total_size // chunk_size):
            random_chunk = generate_random_bytes(chunk_size)
            file.write(random_chunk)
            print('*')

        remaining_bytes = total_size % chunk_size
        if remaining_bytes > 0:
            random_chunk = generate_random_bytes(remaining_bytes)
            file.write(random_chunk)

def _create_tmp_file(file_path):
    if not os.path.exists(file_path):
        total_size = 1024 * 1024 * 10 # 10 MByte
        chunk_size = 1024 * 1024  # 1MB

        write_large_file(file_path, total_size, chunk_size)

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
    start_time = time.time()
    update_hash()
    end_time = time.time()
    print(f"My function took {elapsed_time} seconds to run.")
    print(read_hash())