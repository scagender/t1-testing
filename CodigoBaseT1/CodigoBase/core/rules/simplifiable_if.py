from ..rule import *
import ast
import pdb
# Clases que permiten detectar el uso de if statements o if ternarios que 
# se pueden simplificar por la condición o la condición negada.

class SimplifiableIfVisitor(WarningNodeVisitor):

    def __init__(self):
        super().__init__()
        self.warnings = []

        
## CAMBIAR CONSTANT POR NAMECONSTANT
    def visit_If(self, node):
        # Check for simplifiable if statement
        if (isinstance(node.test, ast.Compare) and
            isinstance(node.body[0], ast.Assign) and
            isinstance(node.orelse[0], ast.Assign) and
            node.body[0].targets[0].id == node.orelse[0].targets[0].id and
            isinstance(node.body[0].value, ast.Constant) and
            isinstance(node.orelse[0].value, ast.Constant) and
            node.body[0].value.value != node.orelse[0].value.value):
            self.addWarning('SimplifiableIf', node.lineno, 'if statement can be replaced with a bool(test)')

        elif (isinstance(node.test, ast.Compare) and
                isinstance(node.body[0], ast.Return) and
                isinstance(node.orelse[0], ast.Return) and
                isinstance(node.body[0].value, ast.Constant) and
                isinstance(node.orelse[0].value, ast.Constant) and
                node.body[0].value.value != node.orelse[0].value.value):
                self.addWarning('SimplifiableIf', node.lineno, 'if statement can be replaced with a bool(test)')

        # Continue visiting child nodes
        self.generic_visit(node)
        

    def visit_Module(self, node):
        
        # Check for simplifiable ternary if
        
        if (## If terneario
            isinstance(node.body[0], ast.Return) and
            isinstance(node.body[0].value, ast.IfExp) and
            isinstance(node.body[0].value.body, ast.Constant) and
            isinstance(node.body[0].value.orelse, ast.Constant) and
            node.body[0].value.body.value != node.body[0].value.orelse.value):
            self.addWarning('SimplifiableIf', node.body[0].lineno, 'if statement can be replaced with a bool(test)')
        
        elif (isinstance(node.body[0], ast.Assign) and
            isinstance(node.body[0].value, ast.IfExp) and
            isinstance(node.body[0].value.body, ast.Constant) and
            isinstance(node.body[0].value.orelse, ast.Constant) and
            node.body[0].value.body.value != node.body[0].value.orelse.value):
            self.addWarning('SimplifiableIf', node.body[0].lineno, 'if statement can be replaced with a bool(test)')

        # Continue visiting child nodes
        self.generic_visit(node)


class SimplifiableIfRule(Rule):
    def analyze(self, ast):
        visitor = SimplifiableIfVisitor()
        
        visitor.visit(ast)
        return visitor.warnings

    
    @classmethod
    def name(cls):
        return 'simpl-if'
