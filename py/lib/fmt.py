
def heading (list):
    for i in list:
        #print (i, list[i])
        print ("%*s" % (list[i], i), end = " ")
    print ()
    for i in list:
        for j in range (list[i]):
            print ("-", end="")
        print (" ", end="")
    print ()
