def printTop(n):
    print '+'+ '----+'*n
    
def printRest(n):
    print (('|'+'    |'*n+'\n')*4+'+'+ '----+'*n+'\n')*n
    
def drawGrid(n):
    printTop(n)
    printRest(n)

drawGrid(2)    
drawGrid(4)