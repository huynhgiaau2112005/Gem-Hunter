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

    def result(self, algorithm, solution, runtime):
        print(f"Algorithm: {algorithm}")   

        if solution:
            gems = sum(cell == "G" for row in solution for cell in row)
            traps = sum(cell == "T" for row in solution for cell in row)
            filled = gems + traps
            cnfs = len(storage.cnf)

            print("Solution:")
            for row in solution:
                for element in row:
                    if element == "G":
                        print(f"\033[32m{element}\033[0m", end=" ") # green text
                    elif element == "T":
                        print(f"\033[31m{element}\033[0m", end=" ") # red text
                    else:
                        print(f"{element}", end=" ")
                print("")

            print(f"\nFilled: \033[34m{filled}\033[0m")
            print(f"  Gems: \033[32m{gems}\033[0m")
            print(f" Traps: \033[31m{traps}\033[0m")

            print("")
            print(f"Number of CNF clauses: \033[34m{cnfs}\033[0m")
            print(f"Run time: \033[34m{runtime:6f}\033[0m seconds\n") # green text
        else:
            print("No solution found")

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

        runtime = end_time - start_time

        print("-------------------------------")
        self.result(algorithm, solution, runtime)
        
        if solution:
            global outputPath
            path = inputPath.replace("input", "output").replace(".txt", "") \
                + "_" + algorithm.replace(" ", "").lower() \
                + ".txt"
            TextDAO().export(path, inputPath, solution, algorithm, runtime)
            print(f"File '{path}' has been exported.\n")