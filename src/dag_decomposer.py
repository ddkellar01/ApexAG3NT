import networkx as nx
from typing import Dict, List

class DAGRouter:
    """Parses Planner output into an executable Directed Acyclic Graph."""
    
    def __init__(self):
        self.graph = nx.DiGraph()

    def build_graph(self, proposed_dag: Dict[str, List[str]]):
        """Builds a dependency graph to optimize parallel vs sequential task execution."""
        nodes = proposed_dag.get("nodes", [])
        
        for i, node in enumerate(nodes):
            # Assigning models dynamically based on task naming (mock logic)
            assigned_model = "gpt-5-3-codex" if "refactor" in node else "grok-4-7-router"
            
            self.graph.add_node(node, model=assigned_model, status="pending")
            
            # Simple sequential dependency for this mock
            if i > 0:
                self.graph.add_edge(nodes[i-1], node)
                
    def get_execution_order(self) -> List[str]:
        """Returns the topologically sorted execution path."""
        try:
            return list(nx.topological_sort(self.graph))
        except nx.NetworkXUnfeasible:
            raise ValueError("Cycle detected in Planner DAG. Self-healing required.")
