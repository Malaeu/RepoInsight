import ast
import logging
from typing import Optional, Dict

logger = logging.getLogger(__name__)

class CodeAnalyzer(ast.NodeVisitor):
    """
    Analyzes Python code content and gathers statistics on functions, classes, imports, and assignments.
    """

    def __init__(self):
        self.stats = {
            'functions': 0,
            'classes': 0,
            'imports': 0,
            'assignments': 0
        }

    def analyze_python_file(self, content: str) -> Optional[Dict[str, int]]:
        """
        Analyze a Python file's content and gather statistics.

        Args:
            content (str): The content of the Python file.

        Returns:
            Optional[Dict[str, int]]: A dictionary with counts of various code elements or None if a syntax error occurs.
        """
        self.reset_stats()
        try:
            tree = ast.parse(content)
            self.visit(tree)
            return self.stats.copy()
        except SyntaxError as e:
            logger.error(f"Syntax error in Python file: {e.text.strip()} at line {e.lineno}")
            return None

    def reset_stats(self):
        """
        Resets the statistics counters.
        """
        self.stats = {
            'functions': 0,
            'classes': 0,
            'imports': 0,
            'assignments': 0
        }

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """
        Count function definitions.

        Args:
            node (ast.FunctionDef): The function definition node.
        """
        self.stats['functions'] += 1
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        """
        Count async function definitions.

        Args:
            node (ast.AsyncFunctionDef): The async function definition node.
        """
        self.stats['functions'] += 1
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        """
        Count class definitions.

        Args:
            node (ast.ClassDef): The class definition node.
        """
        self.stats['classes'] += 1
        self.generic_visit(node)

    def visit_Import(self, node: ast.Import):
        """
        Count import statements.

        Args:
            node (ast.Import): The import statement node.
        """
        self.stats['imports'] += 1
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        """
        Count import-from statements.

        Args:
            node (ast.ImportFrom): The import-from statement node.
        """
        self.stats['imports'] += 1
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign):
        """
        Count assignment statements.

        Args:
            node (ast.Assign): The assignment statement node.
        """
        self.stats['assignments'] += 1
        self.generic_visit(node)

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