from functions import *

# Find first hashes for difficulty 0-10
# 0 0 cfcd208495d565ef66e7dff9f98764da
# 1 0 cfcd208495d565ef66e7dff9f98764da
# 2 168  006f52e9102a8d3be2fe5614f42ba989
# 3 1970 0004d0b59e19461ff126e3a08a814c33
# 4 5329 00003e3b9e5336685200ae85d21b4f5e
# 5 1803305 00000f7264c27ba6fea0c837ed6aa0aa
# 6 20412333 0000002760a7f6313eb52ef22f47137a


prevStart = int(input("Initial starting number: "))
print("Difficulty    n    md5(n)    time to calculate")
for i in range(0,10):
	t = datetime.datetime.now()
	h = findHash(int(prevStart),i)
	prevStart = h[0]
	prevHash = h[1]

	print(str(i) + " " + prevStart + " " + prevHash + " " + str(datetime.datetime.now()-t))