import hashlib
import os
import statistics
import datetime

# Returns the most recent block in a ledger
def getCurrentBlock(ledger):
	curBlock = -1
	f = open(ledger,"r")
	lines = f.readlines()

	for line in lines:
		if line[0] == line[1] == "@":
			curBlock = line[2]

	return curBlock
	f.close()

# Adds a block to a ledger
def addBlock(ledger):
	curBlock = getCurrentBlock(ledger)
	f = open(ledger,"r+")
	lines = f.readlines()
	prevBlockN = 1

	for n, line in enumerate(lines):
		
		if line[0] == line[1] == "@":
			if int(line[2]) == int(curBlock):
				prevBlockN = n

			curBlockN = len(lines)
			#print(prevBlockN)

	lines[len(lines)-1] = str(lines[len(lines)-1]) + "\n"
	#print("prev " + str(prevBlockN))
	#print("cur " + str(curBlockN-1))
	prevBlockHash = hashlib.md5(''.join(lines[prevBlockN:curBlockN-1]).encode('utf-8')).hexdigest()

	f.write("\n@@" + str((int(curBlock) + 1)) + "\n" + prevBlockHash + "::" + str(datetime.datetime.now()))
	
	#print(lines[prevBlockN-1:curBlockN])
	print("Wrote hash " + prevBlockHash + " and added block " + str((int(curBlock) + 1)))
	f.close()

# Validates a ledger
def validate(ledger):
	f = open(ledger,"r")
	lines = f.readlines()
	prevBlockStartLine = 1

	for n, line in enumerate(lines):
		#print(prevBlockStartLine)
		if line[0] == line[1] == "@" and int(line[2]) > 0:
			prevBlockHashInLedger = lines[n+1][0:32]
			#
			
			#print(lines[prevBlockStartLine-1:n-1])
			#print("prev " + str(prevBlockStartLine-1))
			#print("cur " + str(n))
			#print(hashlib.md5(''.join(lines[prevBlockStartLine-1:n-1]).encode('utf-8')).hexdigest())
			calcPrevBlockHash = hashlib.md5(''.join(lines[prevBlockStartLine-1:n-1]).encode('utf-8')).hexdigest()
			#print("Calculated Previous Block Hash: " + str(calcPrevBlockHash))

			print("Block " + line[2] + " Hash In Ledger: " + str.rstrip(prevBlockHashInLedger))
			print("Calculated Block " + line[2] + " Hash: " + str(calcPrevBlockHash))

			if str.rstrip(prevBlockHashInLedger) == calcPrevBlockHash:
				print("VALID\n")
			else:
				print("INVALID\n")

			prevBlockStartLine = n+1
			#print(prevBlockStartLine)
	f.close()

# Adds a line to a ledger
def addLine(ledger, text):
	f = open(ledger,"a")
	now = str(datetime.datetime.now())
	f.write("\n" + text + "::" + now + "::" + hashlib.md5((text + now).encode('utf-8')).hexdigest())
	print(text + "::" + now + "::" + hashlib.md5((text + now).encode('utf-8')).hexdigest())
	f.close()

# Compares a list of ledgers' hashes, returning the odd one out
def compare(ledgers):
	l = []
	for ledger in ledgers:
		l.append(hashlib.md5(''.join(open(ledger,"r").readlines()).encode('utf-8')).hexdigest())

	mode = str(statistics.mode(l))

	for i,n in enumerate(l):
		if n != mode:
			return ledgers[i]
	return -1 

# Prints help text
def help():
	print("Command Line Test v0.7\n")
	print("exit/blank - exit")
	print("clear - clear the screen")
	print("help - show this help text")
	print("add block - add a block")
	print("get block - get the current block number")
	print("add line - add a line to the ledger")
	print("get ledger - return the current ledger")
	print("add ledger - create a new ledger")
	print("set ledger - change the current ledger")
	print("validate - validate the ledger")
	print("compare - return the ledger that does not match")
	print("transact - add a transaction to the pool")
	print("commit - insert the pool as a new block into the ledger")
	print("set uid - set user ID")
	print("\n")

# Adds a line to a temporary pool of transactions
def addLineToPool(text):
	f = open("pool","a")
	now = str(datetime.datetime.now())
	f.write("\n" + text + "::" + now + "::" + hashlib.md5((text + now).encode('utf-8')).hexdigest())
	print(text + "::" + now + "::" + hashlib.md5((text + now).encode('utf-8')).hexdigest())
	f.close()

# Commits the temporary pool of transactions to a ledger
def commitPool(ledger):
	p = open("pool","r")
	lines = p.readlines()
	print("Committing transactions: ")
	for line in lines:
		if line != "" and line != "\n":
			#print(line.strip())
			addLine(ledger,line.strip())

	print("To " + ledger)
	addBlock(ledger)
	p.close()
	open("pool","w").close()

# Returns True if a string of text is all the same character
def checkEqual(text):
	equal = True
	for i,j in enumerate(text):
		if i < len(text)-1:
			if text[0] != "0" or text[i] != text[i+1]:
				equal = False
				break
	return equal

# Finds a hash that starts with [difficulty] 0s between [start] and 2147483647. Returns [the number][it's hash]
def findHash(start,difficulty):
	for i in range(start,2147483647):
		h = hashlib.md5(str(i).encode('utf-8')).hexdigest()
		if checkEqual(str(h)[0:difficulty]):
			return str(i),str(h)