class CycleDetector:
    def __init__(self, adj_list):
        self.adj_list = adj_list

    def has_cycle(self):
        visited = set()
        rec_stack = set()

        for node in self.adj_list:
            if node not in visited:
                if self._dfs_check(node, visited, rec_stack):
                    return True
        return False

    def _dfs_check(self, v, visited, rec_stack):
        visited.add(v)
        rec_stack.add(v)

        for neighbor in self.adj_list.get(v, []):
            if neighbor not in visited:
                if self._dfs_check(neighbor, visited, rec_stack):
                    return True
            elif neighbor in rec_stack:
                # Jika tetangga ada di stack rekursi aktif, berarti ada CYCLE!
                print(f"⚠️ Terdeteksi Circular Dependency pada: {v} -> {neighbor}")
                return True

        rec_stack.remove(v)
        return False

# Tes Logika
if __name__ == "__main__":
    # Test 1: Graph Aman (Data dari Seed kita)
    safe_graph = {
        'Flask': ['Werkzeug', 'Jinja2'],
        'Jinja2': ['MarkupSafe'],
        'Werkzeug': [],
        'MarkupSafe': []
    }
    
    # Test 2: Graph Rusak (Cycle)
    cycle_graph = {
        'A': ['B'],
        'B': ['C'],
        'C': ['A']
    }

    detector = CycleDetector(safe_graph)
    print(f"Safe Graph ada cycle? {detector.has_cycle()}")

    detector_bad = CycleDetector(cycle_graph)
    print(f"Cycle Graph ada cycle? {detector_bad.has_cycle()}")