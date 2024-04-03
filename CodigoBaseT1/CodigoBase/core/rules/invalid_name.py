from ..rule import *
import ast

# Clases que permiten detectar el uso de un nombre invalido en clases, metodos y funciones

class InvalidNameVisitor(WarningNodeVisitor):

    def __init__(self):
        super().__init__()
        self.warnings = []
        self.current_class = None  # Mantener un seguimiento de la clase actual

    def visit_ClassDef(self, node):
        self.current_class = node  # Establecer la clase actual
        # Verificar el nombre de la clase
        class_name = node.name
        if not class_name.isidentifier() or not class_name[0].isupper():
            self.addWarning('InvalidName', node.lineno, f'invalid class name {class_name}')
        self.generic_visit(node)  # Continuar la visita
        self.current_class = None  # Restablecer la clase actual

    def visit_FunctionDef(self, node):
        if self.current_class:
            # La función es un método de la clase actual
            method_name = node.name
            if not method_name.isidentifier() or not method_name[0].islower():
                self.addWarning('InvalidName', node.lineno, f'invalid method name {method_name}')
        else:
            # La función no es un método de una clase
            function_name = node.name
            if not function_name.isidentifier() or not function_name[0].islower():
                self.addWarning('InvalidName', node.lineno, f'invalid function name {function_name}')
        self.generic_visit(node)



class InvalidNameRule(Rule):
    def analyze(self, ast):
        visitor = InvalidNameVisitor()
        visitor.visit(ast)
        return visitor.warnings
    
    @classmethod
    def name(cls):
        return 'invalid-name'
