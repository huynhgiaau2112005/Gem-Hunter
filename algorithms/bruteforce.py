class BruteforceSolver:
    def __init__(self):
        self.board = []
        self.cnf = []
        self.var_map = {}
        self.solution = []
        self.blank = []
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

    def isSolved(self):
        for clause in self.cnf:
            if not self.isClauseTrue(clause):
                return False
        return True

    def isValidRoot(self, root):
        bit_len = len(self.blank)
        for i in range(len(self.blank)):
            var = self.blank[i]
            bit_value = (root >> (bit_len - i - 1)) & 1
            self.value[var] = bit_value
        return self.isSolved()
        

    def solve(self, board, cnf, var_map):
        self.board = board
        self.cnf = cnf
        self.var_map = var_map
        self.rows, self.cols = len(self.board), len(self.board[0]) 
        self.solved = False
        self.blank = []

        for x in range(self.rows):
            for y in range(self.cols):
                if self.board[x][y] == "_":
                    var = self.var_map[x, y]
                    self.blank.append(var)
                    self.value[var] = -1

        for root in range(1 << len(self.value)):
            if self.isValidRoot(root):
                self.solved = True

                self.solution = [row[:] for row in self.board]
                for key in self.value:
                    x = (key - 1) // self.cols
                    y = (key - 1) % self.cols
                    self.solution[x][y] = "G" if self.value[key] == 1 else "T"
                    
        return self.solution if self.solved else None






