class BacktrackingSolver:
    def __init__(self):
        self.board = []
        self.cnf = []
        self.var_map = {}
        self.solution = []
        self.value = {}
        self.rows = 0
        self.cols = 0
        self.solved = False

    def isClauseTrue(self, clause):
        for x in clause:
            if x > 0 and self.value[x] == 1: # true for Trap
                return True
            elif x < 0 and self.value[-x] == 0: # true for Gem
                return True
        return False

    def backtrack(self, x=0, y=0):
        #print(f"({x}, {y}) - {self.solved}")

        if self.solved:
            return
        
        # nếu đã hoàn thành cnf
        if x == len(self.cnf):
            self.solved = True
            self.solution = [row[:] for row in self.board]
            
            for key in self.value:
                x = (key - 1) // self.cols
                y = (key - 1) % self.cols
                self.solution[x][y] = "G" if self.value[key] == 1 else "T"

            return

        # nếu đã hoàn thành 1 clause
        if y == len(self.cnf[x]):
            #input("end clause")
            if self.isClauseTrue(self.cnf[x]):
                self.backtrack(x + 1, 0)
                return
            else:
                return
        
        cell = abs(self.cnf[x][y])
        #print(cell)

        if self.value[cell] == -1:
            for value in range(2):
                self.value[cell] = value
                self.backtrack(x, y + 1)

                if self.solved:
                    return
                
                self.value[cell] = -1
        else:
            self.backtrack(x, y + 1)
            if self.solved:
                return
        #print(f"{x},{y} = {-1}")

    def solve(self, board, cnf, var_map):
        self.board = board
        self.cnf = cnf
        self.var_map = var_map
        self.rows, self.cols = len(self.board), len(self.board[0]) 
        self.solved = False

        for x in range(self.rows):
            for y in range(self.cols):
                if self.board[x][y] == "_":
                    id = self.var_map[x, y]
                    self.value[id] = -1

        # for row in self.board:
        #     print(" ".join(map(str, row)))
        # print(self.value)

        self.backtrack()

        # print(self.solution)

        if self.solved:
            return self.solution





