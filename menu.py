import storage
from dao.text_dao import TextDAO
from cnf_generator import CNFGenerator
from algorithms.pysat import PysatSolver
from algorithms.backtracking import BacktrackingSolver
from algorithms.bruteforce import BruteforceSolver
import time

PYSAT = "Pysat"
BRUTE_FORCE = "Brute Force"
BACKTRACKING = "Backtracking"

algorithmName = {
    1: PYSAT,
    2: BRUTE_FORCE,
    3: BACKTRACKING
}

inputPath = {
    "1": storage.input_1_path,
    "2": storage.input_2_path,
    "3": storage.input_3_path
}

outputPath = {
    storage.input_1_path: storage.output_1_path,
    storage.input_2_path: storage.output_2_path,
    storage.input_3_path: storage.output_3_path
}

class Menu:
    def enterInputPath(self):
        global inputPath
        print("Choose an input")
        print("1. Input 1")
        print("2. Input 2")
        print("3. Input 3")
        enter = 0
        while enter not in ("1", "2", "3"):
            enter = input("> Pick: ")
        return inputPath[enter]

    def printInput(self, board):            
        for row in board:
            print(" ".join(map(str, row)))

    def setupCNF(self, board):
        storage.cnf, storage.var_map = CNFGenerator().generate(board)

    def enterAlgorithm(self):
        global algorithmName
        print("Choose an algorithm:")
        print("1. Pysat")
        print("2. Brute Force")
        print("3. Backtracking")
        enter = 0
        while enter not in ("1", "2", "3"):
            enter = input("> Pick: ")
        return algorithmName[int(enter)]

    def solve(self, algorithm, board, cnf, var_map):
        global PYSAT, BRUTE_FORCE, BACKTRACKING
        if algorithm == PYSAT:
            return PysatSolver().solve(board, cnf, var_map)
        elif algorithm == BRUTE_FORCE:
            return BruteforceSolver().solve(board, cnf, var_map)
        elif algorithm == BACKTRACKING:
            return BacktrackingSolver().solve(board, cnf, var_map)


    def execute(self):
        inputPath = self.enterInputPath()
        storage.board = TextDAO().get(inputPath)
        
        print("-------------------------------")
        print("Opted Input:")
        self.printInput(storage.board)

        print("-------------------------------")
        algorithm = self.enterAlgorithm()

        self.setupCNF(storage.board)

        start_time = time.perf_counter()
        solution = self.solve(algorithm, storage.board, storage.cnf, storage.var_map)
        end_time = time.perf_counter()

        runtime = (end_time - start_time) * 1000

        print("-------------------------------")
        print(f"Algorithm: {algorithm}")
        if solution:
            print("Solution:")
            for row in solution:
                print(" ".join(map(str, row)))
            print(f"Run time: {runtime:6f} milliseconds\n")

            global outputPath
            TextDAO().export(outputPath[inputPath], solution, algorithm, runtime)
            print(f"File '{outputPath[inputPath]}' has been exported.\n")
        else:
            print("No solution found")
        
        # for row in storage.cnf:
        #     print(row)