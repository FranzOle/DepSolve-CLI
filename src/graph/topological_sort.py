class TopologicalSorter:
    def __init__(self, adj_list):
        self.adj_list = adj_list
        self.visited = set()
        self.order = []

    def sort(self):
        """
        Melakukan pengurutan paket.
        Hasilnya adalah urutan instalasi: Dependency dulu baru Parent.
        """
        self.visited.clear()
        self.order = []
        
        for node in self.adj_list:
            if node not in self.visited:
                self._dfs(node)
        
        return self.order

    def _dfs(self, v):
        self.visited.add(v)
        for neighbor in self.adj_list.get(v, []):
            if neighbor not in self.visited:
                self._dfs(neighbor)
        
        # Masukkan ke order setelah semua dependency-nya masuk
        self.order.append(v)

# tes logika dengan data dummy
if __name__ == "__main__":
    # Skenario: Flask butuh Werkzeug & Jinja2. Jinja2 butuh MarkupSafe.
    graph = {
        'Flask': ['Werkzeug', 'Jinja2'],
        'Jinja2': ['MarkupSafe'],
        'Werkzeug': [],
        'MarkupSafe': []
    }

    sorter = TopologicalSorter(graph)
    result = sorter.sort()
    
    print("--- Urutan Instalasi Terdeteksi ---")
    for i, pkg in enumerate(result, 1):
        print(f"{i}. Install {pkg}")