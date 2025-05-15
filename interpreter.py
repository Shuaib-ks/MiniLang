from ast_nodes import Number, Var, BinOp, Assign, Print
from ast_nodes import If, Block, String
from ast_nodes import AssignmentNode as Assignment
from token_types import TOKENS





class Interpreter:
    def __init__(self):
        self.env = {}

    def eval(self, node):
        if isinstance(node, Number):
            return node.value

        elif isinstance(node, Var):
            if node.name in self.env:
                value = self.env[node.name]
                #print(f"Variable lookup: {node.name} = {value}")  # Debug print
                return value
            else:
                raise Exception(f"Undefined variable '{node.name}'")
        elif isinstance(node, BinOp):
            left = self.eval(node.left)
            right = self.eval(node.right)

            #print(f"DEBUG: BinOp with operator: {repr(node.op)}")
            #print(f"DEBUG: left = {left}, right = {right}")
            op = str(node.op).strip()

            if op == '==':
                result = left == right
                #print(f"Returning {result} from BinOp == comparison")
                return result
            elif op == '+':
                return left + right
            elif op == '-':
                return left - right
            else:
                raise Exception(f"Unsupported operator {op}")

        elif isinstance(node, Block):
            for stmt in node.statements:
                self.eval(stmt)

        elif isinstance(node, If):
            cond_value = self.eval(node.condition)
            #print(f"DEBUG: If condition evaluated to: {cond_value} (type: {type(cond_value)})")
            if cond_value:
                self.eval(node.true_block)
            elif node.false_block:
                self.eval(node.false_block)

        elif isinstance(node, Assignment):
            value = self.eval(node.value)
            self.env[node.var_name] = value
            #print(f"Assigned {node.var_name} = {value}")

        elif isinstance(node, String):
            return node.value


        elif isinstance(node, Assign):
            value = self.eval(node.value)
            self.env[node.name] = value

        elif isinstance(node, Print):
            value = self.eval(node.expr)
            print(value)

        else:
            raise Exception(f"Unknown node type: {node}")
