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
def addBlock(ledger, uid):
	curBlock = getCurrentBlock(ledger)
	f = open(ledger,"r+")
	lines = f.readlines()
	prevBlockN = 1

	for n, line in enumerate(lines):
		
		if line[0] == line[1] == "@":
			if int(line[2]) == int(curBlock):
				prevBlockN = n

			curBlockN = len(lines)


	lines[len(lines)-1] = str(lines[len(lines)-1]) + "\n"

	prevBlockHash = hashlib.md5(''.join(lines[prevBlockN:curBlockN-1]).encode('utf-8')).hexdigest()

	f.write("\n@@" + str((int(curBlock) + 1)) + "\n" + prevBlockHash + "::" + str(datetime.datetime.now()) + "::" + str(uid))
	

	print("Wrote hash " + prevBlockHash + " and added block " + str((int(curBlock) + 1)))
	f.close()

# Validates a ledger
def validate(ledger):
	f = open(ledger,"r")
	lines = f.readlines()
	prevBlockStartLine = 1

	for n, line in enumerate(lines):

		if line[0] == line[1] == "@" and int(line[2]) > 0:
			prevBlockHashInLedger = lines[n+1][0:32]

			calcPrevBlockHash = hashlib.md5(''.join(lines[prevBlockStartLine-1:n-1]).encode('utf-8')).hexdigest()


			print("Block " + str(int(line[2])-1) + " Hash In Ledger: " + str.rstrip(prevBlockHashInLedger))
			print("Calculated Block " + str(int(line[2])-1) + " Hash: " + str(calcPrevBlockHash))

			if str.rstrip(prevBlockHashInLedger) == calcPrevBlockHash:
				print("VALID\n")
			else:
				print("INVALID\n")

			prevBlockStartLine = n+1

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
def commitPool(ledger, uid):
	p = open("pool","r")
	lines = p.readlines()
	print("Committing transactions:\n")
	for line in lines:
		if line != "" and line != "\n":

			addLine(ledger,line.strip())

	print("To " + ledger + "\n")
	addBlock(ledger, uid)
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
def findHash(start, difficulty):
	for i in range(start,2147483647):
		h = hashlib.md5(str(i).encode('utf-8')).hexdigest()
		if checkEqual(str(h)[0:difficulty]):
			return str(i),str(h)

# Begins mining
def mine(start, difficulty, uid):
	# Find first hashes for difficulty 0-10

	# 0 0 cfcd208495d565ef66e7dff9f98764da
	# 1 0 cfcd208495d565ef66e7dff9f98764da
	# 2 168  006f52e9102a8d3be2fe5614f42ba989
	# 3 1970 0004d0b59e19461ff126e3a08a814c33
	# 4 5329 00003e3b9e5336685200ae85d21b4f5e
	# 5 1803305 00000f7264c27ba6fea0c837ed6aa0aa
	# 6 20412333 0000002760a7f6313eb52ef22f47137a

	prevStart = int(start)
	print("Difficulty    n    md5(n)    time to calculate")

	t = datetime.datetime.now()
	h = findHash(int(prevStart),int(difficulty))
	prevStart = h[0]
	prevHash = h[1]

	print(str(difficulty) + " " + prevStart + " " + prevHash + " " + str(datetime.datetime.now()-t))