from ast import *
from core.rewriter import RewriterCommand
import pdb

# Clases que permiten transformar código que contiene x = x <operador_aritmetico_binario> z a x <operador_aritmetico_binario>= z.

class OperatorEqualsTransformer(NodeTransformer):

    def __init__(self):
        super().__init__()

    def visit_Assign(self, node):
        if isinstance(node.value, BinOp) and isinstance(node.value.op, (Add, Sub, Mult, Div, Mod, Pow, FloorDiv)):
            return AugAssign(target=node.targets[0], op=node.value.op, value=node.value.right)
        return node.value


class OperatorEqualsCommand(RewriterCommand):

    def apply(self, ast):
        new_tree = fix_missing_locations(OperatorEqualsTransformer().visit(ast))
        return new_tree