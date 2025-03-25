import os

class BacktrackingSolver:
    def __init__(self):
        self.board = []
        self.cnf = []
        self.var_map = {}
        self.solution = []
        self.value = {}
        self.blank = []
        self.rows = 0
        self.cols = 0
        self.solved = False

    def isClauseTrue(self, clause):
        for literal in clause:
            if literal < 0 and self.value[-literal] in (0, -1): # Gem
                return True
            if literal > 0 and self.value[literal] in (1, -1): # Trap
                return True
        
        return False

    def isSuitable(self):
        for clause in self.cnf:
            if not self.isClauseTrue(clause):
                return False
        return True

    def backtrack(self, index=0):
        if self.solved:
            return
        
        # if done cnf
        if index == len(self.value):
            self.solved = True

            self.solution = [row[:] for row in self.board]
            for key in self.value:
                x = (key - 1) // self.cols
                y = (key - 1) % self.cols
                self.solution[x][y] = "T" if self.value[key] == 1 else "G"

            return
        print(index)
        var = self.blank[index]

        for value in range(2):
            self.value[var] = value
            if self.isSuitable():
                self.backtrack(index + 1)
            if self.solved:
                return
            self.value[var] = -1


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
                    self.blank.append(id)
                    self.value[id] = -1

        # for row in self.board:
        #     print(" ".join(map(str, row)))
        # print(self.value)

        self.backtrack()

        # print(self.solution)

        if self.solved:
            return self.solution