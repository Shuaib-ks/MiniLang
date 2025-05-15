class AssignmentNode:
    def __init__(self, var_name, value):
        self.var_name = var_name  # the name of the variable being assigned
        self.value = value        # the value being assigned to the variable

    def __repr__(self):
        return f"Assignment({self.var_name} = {self.value})"


class Block:
    def __init__(self, statements):
        self.statements = statements
    def __repr__(self):
        return f"Block({self.statements})"

class If:
    def __init__(self, condition, true_block, false_block=None):
        self.condition = condition
        self.true_block = true_block
        self.false_block = false_block
    def __repr__(self):
        return f"If({self.condition}, {self.true_block}, {self.false_block})"



class Number:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"Number({self.value})"

class Var:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"Var({self.name})"

class BinOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    def __repr__(self):
        return f"BinOp({self.left}, '{self.op}', {self.right})"

class Assign:
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def __repr__(self):
        return f"Assign({self.name}, {self.value})"

class Print:
    def __init__(self, expr):
        self.expr = expr
    def __repr__(self):
        return f"Print({self.expr})"
