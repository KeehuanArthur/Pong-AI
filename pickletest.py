import pickle 

class derp:
    def __init__(self):
        self.herp = ['1',2,3]
        self.merp = 200

def main():
    test_dict = dict()
    test_dict[(1,2,3)] = derp()
    test_dict[(3,2,1)] = derp()

    test_file = open('test_file.pkl', 'wb' )
    pickle.dump( test_dict, test_file )

    test_file.close()
    test_file = open('test_file.pkl', 'rb' )

    new_dict = pickle.load( test_file )    

    for key in new_dict:
        print( key, new_dict[key].herp )


if __name__ == "__main__":
    main()