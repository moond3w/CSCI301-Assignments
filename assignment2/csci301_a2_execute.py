# CSCI 301 Assignment 2: Executing Pay-to-Multi-Signature (P2MS)
# Date: 12/2/2024
# Program uses scriptPubKey.txt and scriptSig.txt to execute P2MS Script
# The program csci301_a2.py should be executed before current program.

from Crypto.PublicKey import DSA
from Crypto.Signature import DSS
from Crypto.Hash import SHA256
import binascii
import sys

# Operation to check if all M signatures in are valid
def OP_CHECKMULTISIG(stack):
    # Initialize variables
    pub_key = []
    signature_hex = []
    verified_sig = 0

    # Retrieve param key and set message
    param_key = DSA.import_key(open("public_key.pem").read())
    message = b'CSCI301 Contemporary topic in security 2024'
    hash_obj = SHA256.new(message)

    # Retrieve N
    item = stack.pop()
    N = int(item.lstrip("OP_"))
    for i in range(N):
        item = stack.pop()
        pub_key.append(item)
    
    # Retrieve M
    item = stack.pop()
    M = int(item.lstrip("OP_"))
    for i in range(M):
        item = stack.pop()
        signature_hex.append(item)
    
    # Start of validation
    for hex_key in pub_key:
        # Construct DSA key
        y = int(hex_key, 16)
        tup = [y, param_key.g, param_key.p, param_key.q]
        key = DSA.construct(tup)
        verifier = DSS.new(key, 'fips-186-3')

        # Verify message with signature
        for sig_hex in signature_hex:
            signature = binascii.unhexlify(sig_hex)

            try:
                verifier.verify(hash_obj, signature)
                verified_sig += 1
                signature_hex.remove(sig_hex)
                break
            except ValueError:
                break
    
    # If all signatures are verified
    if (verified_sig == M):
        stack.append(1)
        print ("All signatures have been verified successfully. Script is valid.")

    else:
        stack.append(0)
        print ("Not all signatures were verified. Script is NOT valid.")

    # Stack after OP_CHECKMULTISIG
    print ("Stack after OP_CHECKMULTISIG: ")
    print (stack)

    return stack

# ======== START OF PROGRAM =========

# Read scriptSig and scriptPubKey and push into stack
stack = []

try:
    with open("scriptSig.txt", "r") as scriptSig:
        for line in scriptSig:
            line = line.rstrip()
            stack.append(line)
    
    print ("scriptSig.txt sucessfully added to stack.")
except IOError as e:
    print(f"Couldn't find scriptSig.txt ({e})")
    sys.exit()

try:
    with open("scriptPubKey.txt", "r") as scriptPubKey:
        for line in scriptPubKey:
            line = line.rstrip()
            stack.append(line)
    
    print ("scriptPubKey.txt sucessfully added to stack.")
except IOError as e:
    print(f"Couldn't find scriptPubKey.txt ({e})")
    sys.exit()


# Sanity check to ensure values match
counter = 0
for item in stack:
    # Retrieve value of M and N - This will ignore dummy value as value = 0
    if (item.startswith("OP")):
        valCheck = item.lstrip("OP_")
        if (valCheck != "CHECKMULTISIG"):
            numCheck = int(valCheck)
            if (numCheck != counter):
                raise ValueError("Sanity Check - Expected: " + str(numCheck) + " Got: " + str(counter))

        # Reset counter for next check        
        counter = 0
    else:
        # If not OP code
        counter += 1

print ("Sanity check passed.")

# Pops through stack to handle OP_CHECKMULTISIG
while (len(stack) != 0):
    item = stack.pop()
    # Start of CHECKMULTISIG
    if item == ("OP_CHECKMULTISIG"):
        stack = OP_CHECKMULTISIG(stack)