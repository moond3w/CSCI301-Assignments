# CSCI301 Assignment 1
# -------------------------
# This program identifies and decrypts all .enc files in current directory by
# first decrypting the corresponding session keys via RSA private key decryption.
# The decrypted session keys are then used to decrypt all .enc files back to text files.
# (filename.txt.decrypted)
# -------------------------
# Date: 21/01/2024 


import os

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from base64 import b64decode
from Crypto.Util.Padding import unpad

# Decryption of rsa encrypted session key using private key
def rsa_decryption(private_key_file, encrypted_data_file):
    file_in = open(encrypted_data_file, "rb")
    private_key = RSA.import_key(open(private_key_file).read())
    rsa_enc_data = file_in.read(private_key.size_in_bytes())
    cipher_rsa = PKCS1_OAEP.new(private_key)
    decrypted_data = cipher_rsa.decrypt(rsa_enc_data)
    file_in.close()
    
    print (encrypted_data_file + " has been decrypted via RSA Private Key Decryption.")
    return decrypted_data

# Symmetric decryption given an encoded iv, encoded ct and known symmetric session key
def symmetric_decryption(encoded_iv, encoded_ct, key):
    try:
        iv = b64decode(encoded_iv)
        ct = b64decode(encoded_ct)
        
        cipher = AES.new(key, AES.MODE_CBC, iv)
        # Retrieve message
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        return pt
    except ValueError:
        print("Incorrect decryption")
    except KeyError:
        print("Incorrect Key")

# Read inital vector and cipher text (iv, ct) sent in .enc files
def read_ivct_file(encrpyted_text_file):
    with open(encrpyted_text_file, "r") as text:
        encrpyted_text = text.readlines()
    
    for line in encrpyted_text:
        line = line.rstrip("\n")
    
    iv = encrpyted_text[0]
    ct = encrpyted_text[1]

    print (encrpyted_text_file + " read successfully.")

    return iv, ct

# List files in directory automatically
def list_files(directory):
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        if os.path.isfile(path):
            yield path

# Write decrypted message into new text file
def writefile(message, filename):
    formatted_filename = filename.replace(".encrypted", ".decrypted")
    with open(formatted_filename, "wb+") as output_file:
        output_file.write(message)
    
    print(formatted_filename + " created.")

# =============== Main program =================

# Set directory to current folder
directory = '.'

# Private key to decrypt files
private_key_file = "privatekey1.pem"

# Loop through file in current directory
for filename in list_files(directory):
    if filename.endswith(".encrypted"):
        # Retrieve iv and ct from file
        iv, ct = read_ivct_file(filename)

        # Identify corresponding session key file
        sess_key_file = filename.replace(".encrypted", ".session_key.bin")

        # Decrypt session key
        decrypted_symm_key = rsa_decryption(private_key_file, sess_key_file)

        # Read and save data
        message = symmetric_decryption(iv, ct, decrypted_symm_key)
        writefile(message, filename)
        print("")
