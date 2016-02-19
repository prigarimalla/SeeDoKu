import sys
from decoder import Decoder

def decodeAndSolve(image):
    d = Decoder(image)
    d.decode()
    print d.puzzle

if __name__ == '__main__':
    if len(sys.argv) == 2:
        decodeAndSolve(sys.argv[1])
    else:
        print 'Usage: python seedoku.py image.jpg'