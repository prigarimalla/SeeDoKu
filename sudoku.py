class SuDoKu(object):
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.origPuzzle = puzzle
        self.solved = False

    def solution(self):
        if not self.solved:
            self.solve()
        return self.puzzle

    def solve(self, cell=0):
        if not self.solved:
            col, row = cell/9, cell%9
            if col > 8:
                self.solved = True
                return
            if self.origPuzzle[col][row] != 0:
                self.solve(cell+1)
            else:
                for i in range(1,10):
                    if self.isValidPlacement(col, row, i):
                        self.puzzle[col][row] = i
                        self.solve(cell+1)
                if not self.solved:
                    self.puzzle[col][row] = 0

    def isValidPlacement(self, col, row, num):
        return self.puzzle[col].count(num) == 0 \
               and [self.puzzle[i][row] for i in range(9)].count(num) == 0 \
               and [self.puzzle[col/3*3+i][row/3*3+j] for i in range(3) for j in range(3)].count(num) == 0