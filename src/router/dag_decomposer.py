import networkx as nx
from typing import Dict, Any, List

class DAGRouter:
    """Converts the Planner's JSON proposal into an executable NetworkX Directed Graph."""

    def __init__(self):
        self.graph = nx.DiGraph()

    def build_graph(self, proposed_plan: Dict[str, Any]) -> None:
        """Constructs the DAG from proposed nodes and edges."""
        self.graph.clear()
        
        nodes = proposed_plan.get("nodes", [])
        edges = proposed_plan.get("edges", [])

        for node in nodes:
            # Assigning specific execution models to node types
            model_assignment = "gpt-5-3-codex" if "ast" in node or "code" in node else "gemini-2.5-pro"
            self.graph.add_node(node, model=model_assignment, status="pending")

        for edge in edges:
            if len(edge) == 2:
                self.graph.add_edge(edge[0], edge[1])

    def get_execution_order(self) -> List[str]:
        """Returns the topologically sorted order of tasks."""
        if len(self.graph.nodes) == 0:
            return []
        try:
            return list(nx.topological_sort(self.graph))
        except nx.NetworkXUnfeasible:
            raise ValueError("Proposed plan contains circular dependencies (not a DAG).")
