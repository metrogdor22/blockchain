import hashlib
import os
import statistics
import datetime

def getCurrentBlock(ledger):
	curBlock = -1
	f = open(ledger,"r")
	lines = f.readlines()

	for line in lines:
		if line[0] == line[1] == "@":
			curBlock = line[2]

	return curBlock
	f.close()

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

	prevBlockHash = hashlib.md5(''.join(lines[prevBlockN-1:curBlockN]).encode('utf-8')).hexdigest()

	f.write("\n" + prevBlockHash + "\n" + "@@" + str((int(curBlock) + 1)))
	
	#print(lines[prevBlockN-1:curBlockN])
	print("Wrote hash " + prevBlockHash + " and added block " + str((int(curBlock) + 1)))
	f.close()

def validate(ledger):
	f = open(ledger,"r")
	lines = f.readlines()
	prevBlockStartLine = 1

	for n, line in enumerate(lines):
		if line[0] == line[1] == "@":
			prevBlockHashInLedger = lines[n-1]
			#
			
			#print(lines[prevBlockStartLine-1:n-1])
			#print(hashlib.md5(''.join(lines[prevBlockStartLine-1:n-1]).encode('utf-8')).hexdigest())
			calcPrevBlockHash = hashlib.md5(''.join(lines[prevBlockStartLine-1:n-1]).encode('utf-8')).hexdigest()
			#print("Calculated Previous Block Hash: " + str(calcPrevBlockHash))

			print("Block " + line[2] + " Hash In Ledger: " + str.rstrip(prevBlockHashInLedger))
			print("Calculated Block " + line[2] + " Hash: " + str(calcPrevBlockHash))

			if str.rstrip(prevBlockHashInLedger) == calcPrevBlockHash:
				print("VALID\n")
			else:
				print("INVALID\n")

			prevBlockStartLine = n
	f.close()

def addLine(ledger, text):
	f = open(ledger,"a")
	f.write("\n" + text)
	f.close()

def compare(ledgers):
	l = []
	for ledger in ledgers:
		l.append(hashlib.md5(''.join(open(ledger,"r").readlines()).encode('utf-8')).hexdigest())

	mode = str(statistics.mode(l))

	for i,n in enumerate(l):
		if n != mode:
			return ledgers[i]
	return -1 

def help():
	print("Command Line Test v0.6\n")
	print("exit/blank - exit")
	print("clear - clear the screen")
	print("help - show this help text")
	print("add block - add a block")
	print("get block - get the current block number")
	print("validate - validate the ledger")
	print("add line - add a line")
	print("set ledger - change the current ledger")
	print("compare - return the ledger that does not match")
	print("get ledger - return the current ledger")
	print("add ledger - create a new ledger")
	print("transact - add a transaction to the pool")
	print("commit - insert the pool as a new block")
	print("\n")

def addLineToPool(text):
	f = open("pool","a")
	now = str(datetime.datetime.now())
	f.write("\n" + text + "::" + now + "::" + hashlib.md5((text + now).encode('utf-8')).hexdigest())
	print(text + "::" + now + "::" + hashlib.md5((text + now).encode('utf-8')).hexdigest())
	f.close()

def commitPool(ledger):
	p = open("pool","r")
	lines = p.readlines()
	print("Committing transactions: ")
	for line in lines:
		if line != "" and line != "\n":
			print(line.strip())
			addLine(ledger,line.strip())

	print("To " + ledger)
	addBlock(ledger)
	p.close()
	open("pool","w").close()

def checkEqual(text):
	equal = True
	for i,j in enumerate(text):
		if i < len(text)-1:
			if text[0] != "0" or text[i] != text[i+1]:
				equal = False
				break
	return equal

def findHash(start,difficulty):
	for i in range(start,2147483647):
		h = hashlib.md5(str(i).encode('utf-8')).hexdigest()
		if checkEqual(str(h)[0:difficulty]):
			return str(i),str(h)

prevStart = 0
for i in range(0,10):
	t = datetime.datetime.now()
	h = findHash(int(prevStart),i)
	prevStart = h[0]
	prevHash = h[1]

	print(str(i) + " " + prevStart + " " + prevHash + " " + str(datetime.datetime.now()-t))