from ..rule import *
import ast

# Clases que permiten detectar si algun atributo no fue inicializado.
# A veces se usan algunos atributos que no estan inicializados y esto genera errores.

class UninitializedAttributeVisitor(WarningNodeVisitor):

    def __init__(self):
        super().__init__()
        self.warnings = []
        self.current_class = None  # Mantener un seguimiento de la clase actual

    def visit_ClassDef(self, node):
        self.current_class = node  # Establecer la clase actual
        self.generic_visit(node)  # Continuar la visita
        self.current_class = None  # Restablecer la clase actual

    def visit_Assign(self, node):
        if self.current_class:
            # Verificar asignaciones dentro de la clase
            for target in node.targets:
                if isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name) \
                        and target.value.id == 'self':
                    # Es una asignación a un atributo de la clase
                    attr_name = target.attr
                    self.addWarning('UninitializedAttribute', node.lineno,
                                    f'{attr_name} attribute was not initialized!')


class UninitializedAttributeRule(Rule):

    def analyze(self, ast):
        visitor = UninitializedAttributeVisitor()
        visitor.visit(ast)
        return visitor.warnings


    @classmethod
    def name(cls):
        return 'uninit-attr'