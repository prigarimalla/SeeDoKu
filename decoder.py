import numpy as np
import cv2
from PIL import Image
import pytesseract


class Decoder(object):
    def __init__(self, image):
        self.origImage = image
        self.image = image
        self.thresholdImage = None
        self.puzzleBounds = None
        self.corners = None
        self.puzzleImage = None
        self.puzzle = [[0 for i in range(9)] for i in range(9)]

    def decode(self):
        self.origImage = self._prepareImage(self.origImage, mono=False)
        self.image = self._prepareImage(self.image)
        self.thresholdImage = self._makeBinary(self.image, blurKernel=9, thresholdKernel=21)
        self._findPuzzle()
        self._identifyDigits()
        self._drawContoursOnImage((self.puzzleBounds))

    def _prepareImage(self, img, mono=True):
        img = cv2.copyMakeBorder(img, 20, 20, 20, 20, cv2.BORDER_REPLICATE)
        if len(img.shape) != 2 and mono:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        factor = 900.0/(img.shape[1])
        return cv2.resize(img, None, fx=factor, fy=factor)

    def _makeBinary(self, img, blurKernel, thresholdKernel):
        img = cv2.GaussianBlur(img, (blurKernel, blurKernel), 0)
        return cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,thresholdKernel,10)

    def _findPuzzle(self):
        contours = cv2.findContours(self.thresholdImage.copy(), mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_SIMPLE)[1]
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[1:2]
        self.puzzleBounds = contours
        points = []
        for p in contours:
            for q in p:
                for r in q:
                    points.append((r[0],r[1]))
        corners=[min(points, key=lambda (x,y): x*y), max(points, key=lambda (x,y): x-y),
                 max(points, key=lambda (x,y): y-x), max(points, key=lambda (x,y): x*y)]
        src = np.float32([[corners[0][0], corners[0][1]],
                          [corners[1][0], corners[1][1]],
                          [corners[2][0], corners[2][1]],
                          [corners[3][0], corners[3][1]]])
        dst = np.float32([[0,0], [900,0], [0,900], [900,900]])
        M = cv2.getPerspectiveTransform(src, dst)
        self.puzzleImage = cv2.warpPerspective(self.image, M, (900, 900))
        self.corners = corners

    def _identifyDigits(self):
        img = self.puzzleImage
        img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,21,10)
        img = cv2.GaussianBlur(img, (41,41), 0)
        vals = []
        for p,q in ((x,y) for x in (i*100+50 for i in range(9)) for y in (i*100+50 for i in range(9))):
            if img[p][q] < 230:
                vals.append((p,q))
                num = self.puzzleImage[p-35:p+35, q-35:q+35]
                num = cv2.cvtColor(num, cv2.COLOR_BAYER_GR2RGB)
                num = Image.fromarray(num)
                self.puzzle[(q-50)/100][(p-50)/100] = pytesseract.image_to_string(num, config='-psm 10')
                cv2.circle(img, (q,p), 3, (0,0,255))

    def _drawContoursOnImage(self, contours, idx=-1, color=(0,255,0), lineWidth=2):
        cv2.drawContours(self.origImage, contours, idx, color, lineWidth)
        for point in self.corners:
            cv2.circle(self.origImage, point, 25, (255,0,0), lineWidth)

if __name__ == '__main__':
    import sys
    img = cv2.imread(sys.argv[1], cv2.IMREAD_COLOR)
    d = Decoder(img)
    d.decode()
    print d.puzzle
    cv2.imshow('img', d.puzzleImage)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
