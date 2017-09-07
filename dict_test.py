

class boop:
    def __init__(self):
        self.herro = [1,2,3]
        self.boop = 'meep'

def main():
    d = dict()
    d[1] = boop()
    d[2] = boop()


    file = open( 'test.txt', 'w+' )

    print(d)


if __name__ == "__main__":
    main()