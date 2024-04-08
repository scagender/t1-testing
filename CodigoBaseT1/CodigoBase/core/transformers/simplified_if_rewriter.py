from ast import *
from core.rewriter import RewriterCommand


# Clases que permiten transformar if ternarios que puedan ser simplificados usando la condicion o su negacion.

"""class SimplifiedIfTransformer(NodeTransformer):
    def __init__(self):
        super().__init__()

    def visit_IfExp(self, node):
        if isinstance(node.test, ast.Compare):
            comparison = node.test
            if len(comparison.ops) == 1 and isinstance(comparison.ops[0], ast.Gt):
                if isinstance(comparison.left, ast.Name) and isinstance(comparison.comparators[0], ast.Name):
                    if comparison.left.id == comparison.comparators[0].id:
                        if isinstance(node.body, ast.Name):
                            return ast.Name(id="True", ctx=ast.Load())
                        elif isinstance(node.orelse, ast.Name):
                            return ast.Name(id="False", ctx=ast.Load())
                elif isinstance(comparison.left, ast.Name) and isinstance(comparison.comparators[0], ast.Constant):
                    if comparison.comparators[0].value == 0:
                        if isinstance(node.body, ast.Name):
                            return comparison.left
                        elif isinstance(node.orelse, ast.Name):
                            return ast.UnaryOp(op=ast.Not(), operand=comparison.left)
            elif len(comparison.ops) == 1 and isinstance(comparison.ops[0], ast.Eq):
                if isinstance(comparison.left, ast.Name) and isinstance(comparison.comparators[0], ast.Name):
                    if comparison.left.id == comparison.comparators[0].id:
                        if isinstance(node.body, ast.Name):
                            return comparison.left
                        elif isinstance(node.orelse, ast.Name):
                            return ast.UnaryOp(op=ast.Not(), operand=comparison.left)
        return node """

class SimplifiedIfTransformer(NodeTransformer):
    def visit_IfExp(self, node):
        if isinstance(node.test, ast.Compare) and len(node.test.ops) == 1:
            if_comp = node.test
            if isinstance(if_comp.ops[0], (ast.Gt, ast.Eq)) and len(if_comp.comparators) == 1:
                left, right = if_comp.left, if_comp.comparators[0]
                if isinstance(left, ast.Name) and isinstance(right, (ast.Name, ast.Constant)):
                    if isinstance(node.body, ast.Name):
                        return left if isinstance(comp.ops[0], ast.Eq) else ast.NameConstant(value=True)
                    elif isinstance(node.orelse, ast.Name):
                        return ast.NameConstant(value=False) if isinstance(if_comp.ops[0], ast.Eq) else ast.UnaryOp(op=ast.Not(), operand=left)
        return node


class SimplifiedIfCommand(RewriterCommand):
    def apply(self, ast):
        transformer = SimplifiedIfTransformer()
        return transformer.visit(ast)
