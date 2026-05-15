from rich.tree import Tree
from rich.console import Console
from src.graph.graph_builder import GraphBuilder
from src.graph.traversal import BFSTraversal

class TreeCommand:
    def __init__(self):
        self.builder = GraphBuilder()
        self.console = Console()

    def run(self, package_name):
        adj_list = self.builder.build_adjacency_list()
        
        if package_name not in adj_list:
            self.console.print(f"[bold red]❌ Error:[/bold red] Paket '{package_name}' tidak terdaftar di repository.")
            return

        traverser = BFSTraversal(adj_list)
        bfs_data = traverser.get_levels(package_name)

        self.console.print(f"\n[bold blue]🔍 Logika BFS (Level-by-Level Analysis):[/bold blue]")
        for pkg, depth in bfs_data:
            self.console.print(f"   Kedalaman {depth}: [cyan]{pkg}[/cyan]")

        self.console.print(f"\n[bold green]🌳 Dependency Tree for {package_name}:[/bold green]")
        
        root_visual = Tree(f"[bold cyan]{package_name}[/bold cyan]")
        self._generate_visual_branches(root_visual, package_name, adj_list)
        
        self.console.print(root_visual)
        self.console.print("\n")

    def _generate_visual_branches(self, tree_node, current_pkg, adj_list, visited=None):
        """Helper rekursif untuk membangun cabang visual pada Rich Tree"""
        if visited is None:
            visited = set()
        
        visited.add(current_pkg)
        
        for dep in adj_list.get(current_pkg, []):
            branch = tree_node.add(f"[white]{dep}[/white]")
            if dep not in visited:
                self._generate_visual_branches(branch, dep, adj_list, visited.copy())

if __name__ == "__main__":
    cmd = TreeCommand()
    cmd.run("Flask")