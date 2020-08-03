from functions import *

ledger = "ledger"
command = ""
uid = 0

os.system('cls')
help()
print(datetime.datetime.now())
while True:
	command = input(">")

	if command == "" or command == "exit":
		break

	if command == "add block":
		addBlock(ledger)
	elif command == "get block":
		print(getCurrentBlock(ledger))
	elif command == "clear":
		os.system('cls')
	elif command == "help":
		help()
	elif command == "validate":
		validate(ledger)
	elif command == "add line":
		text = input(">> ")
		addLine(ledger,text)
	elif command == "set ledger":
		text = input(">> ")
		ledger = text
	elif command == "compare":
		l = []
		while True:
			text = input(">> ")

			if text == "end" or text == "":
				break
			else:
				l.append(text)
		print(compare(l))
	elif command == "get ledger":
		print(ledger)
	elif command == "add ledger":
		n = input(">> ")
		f = open(n,"w+")
		f.write("@@0\n" + "69567d2a452f3e1de45ce48026a9767b::" + str(datetime.datetime.now()))
		f.close()
		print("Created " + n)

	elif command == "transact":
		text = input(">> ")
		addLineToPool(text)
	elif command == "commit":
		commitPool(ledger)
	elif command == "set uid":
		uid = input(">> ")
	elif command == "mine":
		os.system('python %CD%\\miner.py')
	else:
		print("Unknown command")