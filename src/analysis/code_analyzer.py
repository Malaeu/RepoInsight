import ast
import logging
from collections import defaultdict
from typing import Optional, Dict

logger = logging.getLogger(__name__)

class CodeAnalyzer:
    def __init__(self):
        self.reset_stats()

    def reset_stats(self):
        self.stats = defaultdict(int)

    def analyze_python_file(self, content: str) -> Optional[Dict[str, int]]:
        """
        Analyze a Python file's content and gather statistics on functions, classes, imports, and assignments.

        Args:
            content (str): The content of the Python file.

        Returns:
            Optional[Dict[str, int]]: A dictionary with counts of various code elements or None if a syntax error occurs.
        """
        self.reset_stats()
        try:
            tree = ast.parse(content)
            self.visit(tree)
            return dict(self.stats)
        except SyntaxError as e:
            logger.error(f"Syntax error in Python file: {e}")
            return None

    def visit(self, node: ast.AST):
        """
        Recursively visit AST nodes to count functions, classes, imports, and assignments.

        Args:
            node (ast.AST): The current AST node.
        """
        for child in ast.iter_child_nodes(node):
            self.visit(child)
        
        if isinstance(node, ast.FunctionDef):
            self.stats['functions'] += 1
        elif isinstance(node, ast.AsyncFunctionDef):
            self.stats['functions'] += 1  # Counting async functions as well
        elif isinstance(node, ast.ClassDef):
            self.stats['classes'] += 1
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            self.stats['imports'] += 1
        elif isinstance(node, ast.Assign):
            self.stats['assignments'] += 1

    def get_summary(self) -> str:
        """
        Generate a summary of the analyzed code statistics.

        Returns:
            str: A formatted summary string.
        """
        return (
            "Code Summary:\n"
            f"- Number of functions: {self.stats.get('functions', 0)}\n"
            f"- Number of classes: {self.stats.get('classes', 0)}\n"
            f"- Number of imports: {self.stats.get('imports', 0)}\n"
            f"- Number of assignments: {self.stats.get('assignments', 0)}"
        )