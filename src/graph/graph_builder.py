from src.database.connection import SessionLocal
from src.models.package import Package
from src.models.dependency import Dependency

class GraphBuilder:
    def __init__(self):
        self.db = SessionLocal()

    def build_adjacency_list(self):
        """
        Mengubah data database menjadi Adjacency List (Hash Map).
        Struktur: { 'PackageName': ['Dependency1', 'Dependency2'] }
        """
        adj_list = {}
        
        packages = self.db.query(Package).all()
        pkg_map = {pkg.id: pkg.name for pkg in packages}
        
        for pkg_name in pkg_map.values():
            adj_list[pkg_name] = []

        dependencies = self.db.query(Dependency).all()
        for dep in dependencies:
            parent_name = pkg_map.get(dep.package_id)
            child_name = pkg_map.get(dep.dependency_id)
            
            if parent_name and child_name:
                adj_list[parent_name].append(child_name)
        
        self.db.close()
        return adj_list

if __name__ == "__main__":
    builder = GraphBuilder()
    graph = builder.build_adjacency_list()
    print("--- Representasi Graph (Adjacency List) ---")
    for pkg, deps in graph.items():
        print(f"{pkg} -> {deps}")