# CSCI301 Assignment 3
# ========================================================================
# Simple Blockchain System simulating proof-of-work between Alice and Bob.
# Alice and Bob will compete to add a new block to the system.
# This program represents Alice.
# Python Version Used: 3.10.10
# Additional Packages: PubNub (https://www.pubnub.com/)
# =======================================================================

import json
import hashlib
import threading
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory, PNOperationType
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import time
import os

# Given transactions
transactions = [ "[3, 4, 5, 6]", "[4, 5, 6, 7]", "[5, 6, 7, 8]", 
				"[6, 7, 8, 9]", "[7, 8, 9, 10]", "[8, 9, 10, 11]", 
				"[9, 10, 11, 12]", "[10, 11, 12, 13]", "[11, 12, 13, 14]", 
				"[12, 13, 14, 15]", "[13, 14, 15, 16]"]

# Setup for PubNub connection
pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-c2ba461a-64e4-4c78-ae1d-6b96d072b0a3'
pnconfig.publish_key = 'pub-c-4ec157c9-69d8-4855-9d50-e2993dcdc4f0'
pnconfig.user_id = "Client-Alice"
pubnub = PubNub(pnconfig)

def my_publish_callback(envelope, status):
	# Check whether request successfully completed or not
	if not status.is_error():
		pass  # Message successfully published to specified channel.
	else:
		pass  # Handle message publish error. Check 'category' property to find out possible issue
		# because of which request did fail.
		# Request can be resent using: [status retry];

class MySubscribeCallback(SubscribeCallback):
	def presence(self, pubnub, presence):
		pass  # handle incoming presence data

	def status(self, pubnub, status):
		if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
			pass  # This event happens when radio / connectivity is lost

		elif status.category == PNStatusCategory.PNConnectedCategory:
			# Connect event. You can do stuff like publish, and know you'll get it.
			# Or just use the connected event to confirm you are subscribed for
			# UI / internal notifications, etc
			pass
		elif status.category == PNStatusCategory.PNReconnectedCategory:
			pass
			# Happens as part of our regular operation. This event happens when
			# radio / connectivity is lost, then regained.
		elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
			pass
			# Handle message decryption error. Probably client configured to
			# encrypt messages and on live data feed it received plain text.

	def message(self, pubnub, message):
		# Store message in MessageHandler for processing
		print ("Message sent by " + message.publisher)
		MessageHandler.addMessage(message)
        

def createBlock(block_num, transaction):
	# Hash of previous block
	prev_block_f = open("a_" + str(block_num-1)+".json", "r")
	prev_block = prev_block_f.read()
	prev_block_f.close()
	prev_hash = hashlib.sha256(prev_block.encode()).hexdigest()

	nonce = 0

	# Create block while no message is sent to channel yet
	while (MessageHandler.isEmpty()):
		block = json.dumps(
			{'Block number': block_num, 'Hash': prev_hash, 
			'Transaction': transaction,'Nonce': nonce},
			sort_keys=True, 
			indent=4, 
			separators=(',', ': '))

		# Hash the block to determine current hash
		curr_hash = hashlib.sha256(block.encode()).hexdigest()

		# Break loop if hash starts with 00000
		if int(curr_hash[0:8], 16) < int("00000fff", 16):
			break

		# Next iteration
		nonce += 1

	# Publish block for challenge
	if (MessageHandler.isEmpty()):
		pubnub.publish().channel('Channel-Block').message(block).pn_async(my_publish_callback)

# Check if previous block is accurate given current block
def verifyBlock(current_block, current_block_num):
	verified = False

	# Retrieve hash of previous block
	prev_block_f = open("a_" + str(current_block_num-1)+".json", "r")
	prev_block = prev_block_f.read()
	prev_block_f.close()
	prev_hash = hashlib.sha256(prev_block.encode()).hexdigest()
    
	# Verify matches current block ['Hash'] value
	hash_val = json.loads(current_block)['Hash']

	if int(prev_hash, 16) == int(hash_val, 16):
		print ("a_" + str(current_block_num - 1) + ".json is verified")
		verified = True
	else:
		print ("a_" + str(current_block_num - 1) + ".json is NOT verified")
    
	# True if previous block matches current block. False otherwise
	return verified

# Class to determine which block between Alice and Bob to be added to chain
class MessageHandler:
	# Will contain maximum of 2 messages - Alice and Bob from same transaction
	# Happens in scenario where two messages are published - Will determine via timetoken
	msg_array = []

	@classmethod
	def addMessage(cls, message):
		cls.msg_array.append(message)

	@classmethod
	# Determine which block to add given maximum of two blocks from message
	def determineWinner(cls, block_num):
		if len(cls.msg_array) > 1:
			# Use built in timetoken to determine which message arrived first
			if cls.msg_array[0].timetoken < cls.msg_array[1].timetoken:
				winner = cls.msg_array[0]
				loser = cls.msg_array[1]
			else:
				winner = cls.msg_array[1]
				loser = cls.msg_array[0]
		else:
			winner = cls.msg_array[0]
    
		# Verify winning block
		if (verifyBlock(winner.message, block_num)):
			return winner.message
		
		# If not out of method due to failed verification
		if 'loser' in locals():
			if (verifyBlock(loser.message, block_num)):
				return loser.message
		
		# If still not out of method
		print ("ERROR: Generated block(s) failed verification.")
		return False
	
	@classmethod
	def clearArray(cls):
		cls.msg_array.clear()
	
	# Returns True if msg_array is empty, False otherwise
	@classmethod
	def isEmpty(cls):
		if not cls.msg_array:
			return True
		else:
			return False

# Listens to channel until message is sent by either party (Alice or Bob)
# Unsubscribe from channel to prevent receiving messages while handling current message
def listenToChannel():
	pubnub.subscribe().channels("Channel-Block").execute()

	while True:
		if not (MessageHandler.isEmpty()):
			pubnub.unsubscribe_all()
			return

# ====================================================
# 					Start of program
# ====================================================

block_num = 1
pubnub.add_listener(MySubscribeCallback())		

# Added delay so that alice and bob can be executed at approximately the same time
time.sleep(2)

# Loop through transactions
for transaction in transactions:
	block = False
	# While block is not verified
	while (block == False):
		print ("====== CHAIN " + str(block_num) + " ======")

		# Create threading for block creation and pubnub
		t1 = threading.Thread(target=createBlock, args=(block_num, transaction))
		t2 = threading.Thread(target=listenToChannel, args=())

		# Start threading
		t1.start()
		t2.start()

		# End thread execution
		t1.join()
		t2.join()

		# Added delay to attempt to prevent blocks from Alice and Bob from generating too quickly
		time.sleep(5)

		# Verify message once received - Returns False if unable to determine winner
		block = MessageHandler.determineWinner(block_num)
		MessageHandler.clearArray()

	# If verified message, write into file
	fw = open("a_" + str(block_num)+".json", "w+")
	fw.write(block)
	fw.close()
	print ("a_" + str(block_num)+".json created.")

	# Start next block creation process with next transaction
	block_num += 1
	print ("")

# End program
print ("=============================================================")
print ("All transactions are added to the blockchain. Ending program.")
os._exit(0)