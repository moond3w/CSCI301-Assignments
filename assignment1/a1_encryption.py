# CSCI301 Assignment 1
# -------------------------
# This program generates two sets of RSA public/private key pairs and proceeds to 
# encrypt all .txt files in current directory through AES_CBC encryption. (filename.encrypted)
# The generated session keys are then encrypted via RSA public key encryption. 
# (filename.session_key.bin)
# -------------------------
# Date: 21/01/2024 

import os

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad

from base64 import b64encode
from base64 import b64decode

# Encrypt data through AES_CBC encryption. Returns key for RSA encryption
def symmetric_encryption(data, filename):
    key = get_random_bytes(16)

    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data,AES.block_size))

    iv = b64encode(cipher.iv).decode('utf-8')   # Generate IV
    ct = b64encode(ct_bytes).decode('utf-8')    # Generate CT
    key = b64encode(key).decode('utf-8')

    # Write iv and ct into a text file to be sent for reciepient
    encryption_file = open(filename + ".encrypted", "w")
    encryption_file.write(iv + "\n" + ct)
    encryption_file.close()

    print ("Data has been encrypted via AES_CBC encryption to " + filename + ".encrypted")
    return key

# Generate public and private key through RSA Encryption
def generate_RSA_keys(pkey_name, skey_name):
    rsa_key = RSA.generate(2048)
    private_key = rsa_key.export_key()

    file_out = open(skey_name, "wb")
    file_out.write(private_key)
    file_out.close()

    print ("RSA Secret Key: " + skey_name +  " generated successfully.")

    public_key = rsa_key.publickey().export_key()
    file_out = open(pkey_name, "wb")
    file_out.write(public_key)
    file_out.close()

    print ("RSA Public Key: " + pkey_name +  " generated successfully.")

# Encryption of symmetric session key using RSA public key
def rsa_encryption (public_key_file, symmetric_key, filename):
    recipient_key = RSA.import_key(open(public_key_file).read())
    # This data should be the symmetric key
    data = b64decode(symmetric_key)
    file_out = open(filename + ".session_key.bin", "wb")
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    enc_data = cipher_rsa.encrypt(data)
    file_out.write(enc_data)
    file_out.close()

    print (filename + "_session_key.bin generated.")

# List files in directory automatically
def list_files(directory):
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        if os.path.isfile(path):
            yield path

# =============== Main program =================

# Generating two sets of RSA public and private key
generate_RSA_keys("publickey1.pem", "privatekey1.pem")
generate_RSA_keys("publickey2.pem", "privatekey2.pem")

# Set directory to current folder
directory = '.'

# Loop through file in current directory
for filename in list_files(directory):
    if filename.endswith(".txt"):
        with open(filename, "rb") as file:  # Read all txt file in binary
            contents = file.read()
            # Strip filename for ease of reading
            new_filename = filename.replace(".txt", "")
            key = symmetric_encryption(contents, filename)
            rsa_encryption("publickey1.pem", key, filename)
            print("")
