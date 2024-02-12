# CSCI 301 Assignment 2: Implementing Pay-to-Multi-Signature (P2MS)
# Date: 12/2/2024
# Program takes two parameters:
# 1) Number of signatures (M) for scriptSig
# 2) Number of public keys (N) for scriptPubKey

import sys
from Crypto.PublicKey import DSA
from Crypto.Signature import DSS
from Crypto.Hash import SHA256
import binascii

# Set message for the signatures to be signed against
message = b'CSCI301 Contemporary topic in security 2024'
hash_obj = SHA256.new(message)

# Check if input is int
if (sys.argv[1].isdigit and sys.argv[2].isdigit()):
    M = int(sys.argv[1])
    N = int(sys.argv[2])
else:
    raise ValueError("Inputs must be an integer. Exiting program.")

# Check if M <= N
if (M > N):
    raise ValueError("N Must be larger or equal to M. Exiting program.")

# Set domain parameters
param_key = DSA.import_key(open("public_key.pem").read())
param = [param_key.p, param_key.q, param_key.g]
keys = []

# Write public key into scriptPubKey.txt
scriptPubKey = open("scriptPubKey.txt", "w+")
scriptPubKey.write("OP_" + str(M) + "\n")

# Generate N DSA keys
for x in range(N):
    key = DSA.generate(1024, domain=param)
    keys.append(key)
    scriptPubKey.write(hex(key.y) + "\n")

scriptPubKey.write("OP_" + str(N) + "\n")
scriptPubKey.write("OP_CHECKMULTISIG\n")
scriptPubKey.close()
print ("scriptPubKey.txt created.")

# Create scriptSig using private keys
scriptSig = open("scriptSig.txt", "w+")
scriptSig.write("OP_0\n") # Dummy value

# Generate M DSA signatures based on keys
for y in range(M):
    signer = DSS.new(keys[y], 'fips-186-3')
    signature = signer.sign(hash_obj)
    signature_hex = binascii.hexlify(signature)
    sig = signature_hex.decode("utf-8")

    # Write signatures
    scriptSig.write(sig + "\n")

scriptSig.close()
print ("scriptSig.txt created.")