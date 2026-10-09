import ast
import astor
from typing import Optional

class ASTTransformer(ast.NodeTransformer):
    """Mutates Python Abstract Syntax Trees cleanly without regex breakage."""

    def __init__(self, target_func: str, new_decorator: Optional[str] = None):
        self.target_func = target_func
        self.new_decorator = new_decorator

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        """Injects decorators or alters function definitions at the AST level."""
        if node.name == self.target_func and self.new_decorator:
            decorator_ast = ast.Name(id=self.new_decorator, ctx=ast.Load())
            node.decorator_list.append(decorator_ast)
        self.generic_visit(node)
        return node

class ASTCodegenEngine:
    """Parses, mutates, and regenerates clean code using AST trees."""

    @staticmethod
    def add_decorator(source_code: str, target_function: str, decorator_name: str) -> str:
        """Safely injects a decorator into a function definition."""
        tree = ast.parse(source_code)
        transformer = ASTTransformer(target_func=target_function, new_decorator=decorator_name)
        modified_tree = transformer.visit(tree)
        ast.fix_missing_locations(modified_tree)
        return astor.to_source(modified_tree)
