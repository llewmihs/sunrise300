import sys
def main():
    try:
        Answer = 1/0
        print  (Answer)
    except:
        print ('Program terminated')
        sys.exit()
    print ('You wont see this')

if __name__ == '__main__': 
    try:
        main()  
    finally:
        print( "Poo")