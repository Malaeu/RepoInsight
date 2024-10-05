import ast
from collections import defaultdict

class CodeAnalyzer:
    def __init__(self):
        self.stats = defaultdict(int)

    def analyze_python_file(self, content):
        try:
            tree = ast.parse(content)
            self.visit(tree)
            return self.stats
        except SyntaxError as e:
            print(f"Syntax error in Python file: {e}")
            return None

    def visit(self, node):
        for child in ast.iter_child_nodes(node):
            self.visit(child)
        
        if isinstance(node, ast.FunctionDef):
            self.stats['functions'] += 1
        elif isinstance(node, ast.ClassDef):
            self.stats['classes'] += 1
        elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
            self.stats['imports'] += 1
        elif isinstance(node, ast.Assign):
            self.stats['assignments'] += 1

    def get_summary(self):
        return f"""
        Code Summary:
        - Number of functions: {self.stats['functions']}
        - Number of classes: {self.stats['classes']}
        - Number of imports: {self.stats['imports']}
        - Number of assignments: {self.stats['assignments']}
        """

# Usage example:
# analyzer = CodeAnalyzer()
# with open('example.py', 'r') as file:
#     content = file.read()
# analyzer.analyze_python_file(content)
# print(analyzer.get_summary())