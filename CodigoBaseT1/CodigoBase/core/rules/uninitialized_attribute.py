from ..rule import *
import ast

class UninitializedAttributeVisitor(WarningNodeVisitor):
    def __init__(self):
        super().__init__()
        self.current_class = None
        self.initialized_attributes = set()

    def visit_ClassDef(self, node):
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = None

    def visit_Assign(self, node):
        if self.current_class:
            for target in node.targets:
                if isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name) \
                        and target.value.id == 'self':
                    attr_name = target.attr
                    self.initialized_attributes.add(attr_name)

    def visit_Attribute(self, node):
        if self.current_class:
            if isinstance(node.value, ast.Name) and node.value.id == 'self':
                attr_name = node.attr
                if attr_name not in self.initialized_attributes:
                    self.addWarning("UninitializedAttribute", node.lineno, f"{attr_name} attribute was not initialized!")



class UninitializedAttributeRule(Rule):
    def analyze(self, ast):
        visitor = UninitializedAttributeVisitor()
        visitor.visit(ast)
        return visitor.warnings

    @classmethod
    def name(cls):
        return 'uninit-attr'