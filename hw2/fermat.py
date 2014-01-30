def check_fermat(a,b,c,n):
    if(n<2):
        print 'No, that doesn\'t work'
    elif(a**n+b**n==c**n):
        print 'Holy smokes, Fermat was wrong!'
    else:
        print 'No, that doesn\'t work'
        
def user_fermat():
    a = raw_input('Enter \'a\' value\n')
    try:
        a2 = int(a)
    except ValueError:
        a2 = 0
    b = raw_input('Enter \'b\' value\n')
    try:
        b2 = int(b)
    except ValueError:
        b2 = 0
    c = raw_input('Enter \'c\' value\n')
    try:
        c2 = int(c)
    except ValueError:
        c2 = 0
    n = raw_input('Enter \'n\' value\n')
    try:
        n2 = int(n)
    except ValueError:
        n2 = 0
    check_fermat(a2,b2,c2,n2)
    
user_fermat()