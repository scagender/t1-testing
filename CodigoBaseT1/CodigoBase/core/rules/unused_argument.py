from ..rule import *
import ast
import pdb

# Clases que permiten detectar si un argumento no fue usado

class UnusedArgumentVisitor(WarningNodeVisitor):

    def __init__(self):
        super().__init__()
        self.warnings = []
    
    def visit_FunctionDef(self, node):
        used_args = set()
        # Recorre los nodos del cuerpo de la función
        for statement in node.body:
            used_args.update(self.get_used_args(statement))
        # Encuentra los argumentos no utilizados
        for arg in node.args.args:
            if arg.arg not in used_args and arg.arg != 'self':
                self.addWarning('UnusedArgument', node.lineno, f"{arg.arg} argument has not been used!")
                break
        self.generic_visit(node)

    def get_used_args(self, node):
        used_args = set()
        # Caso base: si el nodo es una llamada a función
        if isinstance(node, ast.Assign):
            # Recorre los argumentos de la llamada
            for target in node.targets:
                try: 
                    if isinstance(target, ast.Attribute):
                        used_args.add(node.value.id)
                except:
                    pass
        elif isinstance(node, ast.Call) or isinstance(node, ast.FunctionDef):
            # Recorre los argumentos de la llamada
            for arg in node.args:
                # Si es un nombre, lo agrega a los argumentos utilizados
                if isinstance(arg, ast.Name):
                    used_args.add(arg.id)
                elif isinstance(node, ast.Return):
                    used_args.add(node.value.id)
        # Si es un nodo compuesto, recorre sus hijos
        elif hasattr(node, 'body'):
            for child_node in node.body:
                used_args.update(self.get_used_args(child_node))

        elif isinstance(node, ast.Return):
            if isinstance(node.value, ast.BinOp):
                used_args.add(node.value.left.id)
                used_args.add(node.value.right.id)

        return used_args


class UnusedArgumentRule(Rule):

    def analyze(self, ast):
        visitor = UnusedArgumentVisitor()
        visitor.visit(ast)
        return visitor.warnings

    @classmethod
    def name(cls):
        return 'unused-arg'