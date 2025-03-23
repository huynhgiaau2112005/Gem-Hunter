from pysat.solvers import Glucose3

class PysatSolver:
    def solve(self, board, cnf, var_map):
        solver = Glucose3()
        for clause in cnf:
            solver.add_clause(clause)
        
        if solver.solve():
            model = solver.get_model()
            solution = [[str(board[nx][ny]) if isinstance(board[nx][ny], int) else ("G" if var_map[nx, ny] in model else "T") 
                        for ny in range(len(board[0]))] for nx in range(len(board))]
            return solution
        return None
