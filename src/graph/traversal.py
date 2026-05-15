from collections import deque

class BFSTraversal:
    def __init__(self, adj_list):
        self.adj_list = adj_list

    def get_levels(self, start_node):
        if start_node not in self.adj_list:
            return []

        visited = set()
        queue = deque([(start_node, 0)]) 
        result = []

        while queue:
            current_node, depth = queue.popleft()
            
            if current_node not in visited:
                visited.add(current_node)
                result.append((current_node, depth))
                
                # Masukkan semua dependency ke antrian untuk diproses di level berikutnya
                for neighbor in self.adj_list.get(current_node, []):
                    if neighbor not in visited:
                        queue.append((neighbor, depth + 1))
        
        return result