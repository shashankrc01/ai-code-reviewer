# analyzer.py
import ast

class CodeAnalyzer:
    def __init__(self, filepath):
        self.filepath = filepath
        self.issues = []

    def analyze(self):
        with open(self.filepath, "r", encoding="utf-8") as f:
            code = f.read()
        
        # Parse the code into a Tree
        tree = ast.parse(code)
        
        # Walk through the tree looking for specific things
        self._check_function_lengths(tree)
        self._check_imports(tree)
        
        return self.issues

    def _check_function_lengths(self, tree):
        """Rule: Warn if a function is more than 15 lines long."""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Calculate function length (end line - start line)
                length = node.end_lineno - node.lineno
                
                if length > 15:
                    self.issues.append({
                        "type": "Bloat 🐳",
                        "message": f"Function '{node.name}' is too long ({length} lines). Keep it under 15.",
                        "line": node.lineno
                    })

    def _check_imports(self, tree):
        """Rule: Warn if 'import *' is used (it's bad practice)."""
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                # Check for "from module import *"
                for alias in node.names:
                    if alias.name == "*":
                        self.issues.append({
                            "type": "Risk ⚠️",
                            "message": f"Avoid using wildcards ('from {node.module} import *'). It pollutes the namespace.",
                            "line": node.lineno
                        })