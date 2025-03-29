import storage

class TextDAO:
    def get(self, file_path):
        container = []
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                new_data_line = [int(x) if x != "_" else "_" for x in line.strip().split(", ")]
                container.append(new_data_line)
        return container
    def export(self, file_path, input_path, solution, algorithm, runtime):
        height = len(solution)
        width = len(solution[0])
        cells = height * width
        blanks = sum(cell in ("T", "G") for row in solution for cell in row)
        gems = sum(cell == "G" for row in solution for cell in row)
        traps = sum(cell == "T" for row in solution for cell in row)
        filled = gems + traps
        cnfs = len(storage.cnf)        

        with open(file_path, 'w') as f:
            f.write(f"Algorithm: {algorithm}\n")
            f.write("\n")
            
            f.write("TESTCASE INFORMATION -------------------------------------\n")
            f.write(f"Input Path: {input_path}\n")
            f.write(f"Size: {height}x{width}\n")
            f.write(f"Blanks: {blanks}/{cells}\n")

            f.write("\n")
            f.write("SOLUTION -------------------------------------------------\n")
            for row in solution:
                f.write(', '.join(map(str, row)))
                f.write('\n')
            
            f.write(f"\nFilled: {filled}\n")
            f.write(f"  Gems: {gems}\n")
            f.write(f" Traps: {traps}\n")

            f.write("\n")
            f.write(f"Number of CNF clauses: {cnfs}\n")
            f.write(f"Run time: {runtime:6f} seconds\n")
