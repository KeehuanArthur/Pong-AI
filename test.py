hello = 10


def p1():
    global hello 
    print( hello )
    hello += 1

def p2():
    global hello
    print( hello )


def main():
    p1()
    p2()

if __name__ == '__main__':
    main()