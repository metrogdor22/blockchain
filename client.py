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
		print("> Line to add:")
		text = input(">> ")
		addLine(ledger,text)
	elif command == "set ledger":
		print("> Set ledger:")
		text = input(">> ")
		ledger = text
	elif command == "compare":
		l = []
		while True:
			print("> Ledgers to compare:")
			text = input(">> ")

			if text == "end" or text == "":
				break
			else:
				l.append(text)
		print(compare(l))
	elif command == "get ledger":
		print(ledger)
	elif command == "add ledger":
		print("> Ledger name:")
		n = input(">> ")
		f = open(n,"w+")
		f.write("@@0\n" + "69567d2a452f3e1de45ce48026a9767b::" + str(datetime.datetime.now()) + "::" + str(uid))
		f.close()
		print("Created " + n)

	elif command == "transact":
		text = input(">> ")
		addLineToPool(text)
	elif command == "commit":
		commitPool(ledger,uid)
	elif command == "set uid":
		uid = input(">> ")
	elif command == "mine":
		mine(input(">> Starting number: "),input(">> Difficulty: "), uid)
	else:
		print("Unknown command")