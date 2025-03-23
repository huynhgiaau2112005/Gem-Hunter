from itertools import product

class CNFGenerator:
    def get_neighbors(self, x, y, grid):
        X_MAX, Y_MAX = len(grid), len(grid[0])
        neighbors = []
        for dx, dy in product([-1, 0, 1], repeat=2):
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < X_MAX and 0 <= ny < Y_MAX and grid[nx][ny] == '_':
                neighbors.append((nx, ny))
        return neighbors
    
    def generate(self, grid):
        X_MAX, Y_MAX = len(grid), len(grid[0])
        var_map = {(nx, ny): nx * Y_MAX + ny + 1 for nx, ny in product(range(X_MAX), range(Y_MAX))}
        cnf = []
        
        for x, y in product(range(X_MAX), range(Y_MAX)):
            if isinstance(grid[x][y], int):  # ô có số
                neighbors = self.get_neighbors(x, y, grid)
                vars = [var_map[n] for n in neighbors] # số lượng ô trống liền kề
                num = grid[x][y] # số Trap xung quanh ô đang xét
                
                # Ràng buộc chính xác num Trap
                # --------------------------------------------------------------------
                # v: TRAP, -v: GEM
                # Xét: len(vars) = 6, num = 2:
                #
                # CNF cần đảm bảo:
                # 1. Đảm bảo Trap không nhiều hơn 2:
                #      Với mọi a, b, c: a ^ b ^ c luôn sai
                #   => Với mọi a, b, c: -(a ^ b ^ c) luôn đúng
                #   => Với mọi a, b, c: -a v -b v -c luôn đúng (1)
                # 2. Đảm bảo Trap không ít hơn 2: (Gem không ít hơn 6 - 2 = 4)
                #      Với mọi a, b, c, d, e: -a ^ -b ^ -c ^ -d ^ -e luôn sai
                #   => ... (tương tự với 1.)
                #   => Với mọi a, b, c, d, e: a v b v c v d v e luôn đúng (2)
                #
                # Các Clause của CNF gồm: (1) và (2)
                # --------------------------------------------------------------------
                from itertools import combinations
                cnf.extend([[v for v in comb] for comb in combinations(vars, num + 1)]) # (1)
                cnf.extend([[-v for v in comb] for comb in combinations(vars, len(vars) - num + 1)]) # (2)
        
        # Loại bỏ các ràng buộc trùng nhau
        cnf = list(map(list, set(map(tuple, cnf))))

        return cnf, var_map

