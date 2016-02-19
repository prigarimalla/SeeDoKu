import sys, cv2
from decoder import Decoder
from sudoku import SuDoKu
from copy import copy
def decodeAndSolve(image, showSolution=False):
    d = Decoder(image)
    d.decode()
    s = SuDoKu(d.puzzle)
    solution = s.solution()
    if showSolution:
        img = copy(d.puzzleImage)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        for q,p in ((x,y) for x in (i*100+30 for i in range(9)) for y in (i*100+70 for i in range(9))):
            if ((q-30)/100, (p-70)/100) not in d.numberLocations:
                cv2.putText(img, str(solution[(q-30)/100][(p-70)/100]), (q,p), cv2.FONT_HERSHEY_PLAIN, 4, (0,150,0), thickness=6)
        cv2.imshow('Solution - Press any key to exit.', img)
        cv2.waitKey(0)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        decodeAndSolve(sys.argv[1], showSolution=True)
    else:
        print 'No file specified\nUsage: python seedoku.py image.jpg'