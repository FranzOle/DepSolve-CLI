from src.database.connection import SessionLocal
from src.models.package import Package
from src.models.dependency import Dependency
from src.models.installed_package import InstalledPackage
from src.graph.graph_builder import GraphBuilder
from src.graph.cycle_detection import CycleDetector
from src.graph.topological_sort import TopologicalSorter
from src.resolver.version_validator import VersionValidator

class DependencyResolver:
    def __init__(self):
        self.db = SessionLocal()
        self.builder = GraphBuilder()
        self.validator = VersionValidator()

    def resolve_installation(self, target_package_name):
        """
        Alur Logika Sesuai Dokumen Teknis:
        1. Bangun Graph & Cek Cycle (DFS).
        2. Validasi Kompatibilitas Versi (ERD min_version check).
        3. Tentukan Urutan (Topological Sort).
        4. Filter yang belum terinstal.
        """

        adj_list = self.builder.build_adjacency_list()
        
        if target_package_name not in adj_list:
            return None, f"❌ Error: Package '{target_package_name}' tidak ditemukan di repository."

        detector = CycleDetector(adj_list)
        if detector.has_cycle():
            return None, "❌ Error: Terdeteksi circular dependency! Proses dihentikan demi keamanan sistem."

        all_deps = self.db.query(Dependency).all()
        all_pkgs = self.db.query(Package).all()
        pkg_data = {p.id: {"name": p.name, "version": p.version} for p in all_pkgs}

        for dep in all_deps:
            parent = pkg_data.get(dep.package_id)
            child = pkg_data.get(dep.dependency_id)
            if parent and child:
                is_ok = self.validator.is_compatible(child['version'], dep.min_version)
                if not is_ok:
                    return None, f"❌ Konflik Versi: {parent['name']} butuh {child['name']} {dep.min_version}, tapi di DB cuma ada versi {child['version']}"

        sorter = TopologicalSorter(adj_list)
        sorted_packages = sorter.sort()

        needed = self._get_reachable_nodes(target_package_name, adj_list)

        installed_query = self.db.query(Package.name).join(InstalledPackage).all()
        already_installed = {p[0] for p in installed_query}

        final_queue = [pkg for pkg in sorted_packages if pkg in needed and pkg not in already_installed]

        self.db.close()
        return final_queue, "Sukses"

    def _get_reachable_nodes(self, start_node, adj_list):
        """Mencari semua node yang terhubung (dependency tree) dari target"""
        visited = set()
        stack = [start_node]
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                stack.extend(adj_list.get(node, []))
        return visited

if __name__ == "__main__":
    resolver = DependencyResolver()
    
    print("--- Simulasi Resolving: Flask ---")
    queue, message = resolver.resolve_installation("Flask")
    
    if queue:
        print(f"✅ Rencana Instalasi Terverifikasi:")
        for i, pkg in enumerate(queue, 1):
            print(f"   {i}. {pkg} (Versi kompatibel)")
    else:
        print(message)