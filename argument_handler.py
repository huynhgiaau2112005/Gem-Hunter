import sys
import storage
from dao.text_dao import TextDAO
from cnf_generator import CNFGenerator
from algorithms.pysat import PysatSolver
from algorithms.backtracking import BacktrackingSolver
from algorithms.bruteforce import BruteforceSolver
import time

inputPaths = {
    "1": storage.input_1_path,
    "2": storage.input_2_path,
    "3": storage.input_3_path
}

PYSAT = "pysat"
BRUTE_FORCE = "bruteforce"
BACKTRACKING = "backtracking"

PYSAT_SHORT = "py"
BRUTE_FORCE_SHORT = "bf"
BACKTRACKING_SHORT = "bt"

algorithms = (PYSAT, BRUTE_FORCE, BACKTRACKING,\
             PYSAT_SHORT, BRUTE_FORCE_SHORT, BACKTRACKING_SHORT)

algorithmName = {
    PYSAT: "Pysat",
    BRUTE_FORCE: "Brute Force",
    BACKTRACKING: "Backtracking",
    PYSAT_SHORT: "Pysat",
    BRUTE_FORCE_SHORT: "Brute Force",
    BACKTRACKING_SHORT: "Backtracking"
}

class ArgumentHandler:
    def __init__(self):
        self.arguments = sys.argv
    
    def solve(self, algorithm, board, cnf, var_map):
        global algorithmName
        global PYSAT, BRUTE_FORCE, BACKTRACKING
        if algorithm == algorithmName[PYSAT]:
            return PysatSolver().solve(board, cnf, var_map)
        elif algorithm == algorithmName[BRUTE_FORCE]:
            return BruteforceSolver().solve(board, cnf, var_map)
        elif algorithm == algorithmName[BACKTRACKING]:
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
        global inputPaths, algorithmName
        argvInputPath = self.arguments[1]
        argvAlgorithm = self.arguments[2]

        if argvInputPath not in list(inputPaths.keys()):
            print("Invalid argument for Input Path (2nd argument). Pick 1, 2 or 3")
            return
        
        if argvAlgorithm.lower() not in algorithms:
            print("Invalid argument for Algorithm (3nd argument). Pick one of: pysat, bruteforce, backtracking")
            return
        
        inputPath = inputPaths[argvInputPath]
        algorithm = algorithmName[argvAlgorithm.lower()]

        storage.board = storage.board = TextDAO().get(inputPath)
        storage.cnf, storage.var_map = CNFGenerator().generate(storage.board)
        # print(f"\nCNF size: {len(storage.cnf)}\n")
        # for row in storage.cnf:
        #     print(row)

        start_time = time.perf_counter()
        solution = self.solve(algorithm, storage.board, storage.cnf, storage.var_map)
        end_time = time.perf_counter()

        runtime = end_time - start_time

        self.result(algorithm, solution, runtime)

        if solution:
            global outputPath
            path = inputPath.replace("input", "output").replace(".txt", "") \
                + "_" + algorithm.replace(" ", "").lower() \
                + ".txt"
            TextDAO().export(path, inputPath, solution, algorithm, runtime)
            print(f"File '{path}' has been exported.\n")





