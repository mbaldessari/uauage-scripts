f = open("./ligs.txt", "r")
for line in f.readlines():
    s = line.strip()
    print("sub underscore " + str(s) + " underscore by")
