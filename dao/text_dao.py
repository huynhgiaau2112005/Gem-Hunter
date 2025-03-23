class TextDAO:
    def get(self, file_path):
        container = []
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                new_data_line = [int(x) if x != "_" else "_" for x in line.strip().split(", ")]
                container.append(new_data_line)
        return container
    def export(self, file_path, solution, algorithm, runtime):
        with open(file_path, 'w') as f:
            f.write(f"Algorithm: {algorithm}")
            f.write("\n")
            for row in solution:
                f.write('\n')
                f.write(', '.join(map(str, row)))
            
            f.write(f"\n\nRun time: {runtime:6f} milliseconds")
