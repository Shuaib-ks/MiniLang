from token_types import TOKENS
from ast_nodes import Number, Var, BinOp, Assign, Print, Block, If, AssignmentNode, String

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos]

    def comparison(self):
        # Start by parsing the left-hand side (this could be a number or identifier)
        left = self.equality()  # First, handle equality, then handle relational comparisons

        # Now, we check for relational operators
        while self.current().type in [TOKENS['LT'], TOKENS['LE'], TOKENS['GT'], TOKENS['GE']]:
            op_token = self.current()  # Save the operator token
            self.eat(op_token.type)  # Consume the operator
            right = self.equality()  # Get the right-hand side of the comparison
            left = BinOp(left, op_token.value, right)  # Build a binary operation node

        return left


    def eat(self, token_type):
        if self.current().type == token_type:
            self.pos += 1
        else:
            raise Exception(f"Expected {token_type}, got {self.current().type}")

    def parse(self):
        nodes = []
        while self.current().type != TOKENS['EOF']:
            if self.current().type == TOKENS['IF']:
                nodes.append(self.if_stmt())
            elif self.current().type == TOKENS['PRINT']:
                nodes.append(self.print_stmt())
            else:
                nodes.append(self.assignment())
        return nodes

    def print_stmt(self):
        self.eat(TOKENS['PRINT'])  # eat 'print'
        self.eat(TOKENS['LPAREN']) # eat '('
        expr = self.expr()         # parse inside expression
        self.eat(TOKENS['RPAREN']) # eat ')'
        return Print(expr)
    
    def if_stmt(self):
        self.eat(TOKENS['IF'])  # Consume 'if'

        # Parse the condition directly (no parentheses required)
        condition = self.comparison()

        self.eat(TOKENS['COLON'])  # Expect ':' after the condition

        # Parse the true block (statements to execute if condition is true)
        true_block = self.block()

        # Optional: handle the 'else' block
        false_block = None
        if self.current().type == TOKENS['ELSE']:
            self.eat(TOKENS['ELSE'])     # Consume 'else'
            self.eat(TOKENS['COLON'])    # Expect ':' after else
            false_block = self.block()

        return If(condition, true_block, false_block)

    
    def block(self):
        if self.current().type == TOKENS['PRINT']:
            return Block([self.print_stmt()])
        else:
            return Block([self.assignment()])


    def assignment(self):
        identifier_token = self.current()  # Get the identifier (variable name)
        if identifier_token.type != TOKENS['IDENT']:
            raise Exception(f"Expected IDENTIFIER, got {identifier_token.type}")
        
        self.eat(TOKENS['IDENT'])  # Consume the identifier token

        if self.current().type != TOKENS['ASSIGN']:
            raise Exception(f"Expected '=', got {self.current().type}")
        
        self.eat(TOKENS['ASSIGN'])  # Consume the assignment operator '='

        # Parse the value (it could be a number or identifier)
        # NEW code – parses a full expression tree
        expr_node = self.expr()                # or self.comparison() if you prefer
        return AssignmentNode(identifier_token.value, expr_node)



    def expr(self):
        left = self.term()

        while self.current().type in (TOKENS['PLUS'], TOKENS['MINUS']):
            op = self.current().type
            self.eat(op)
            right = self.term()
            left = BinOp(left, op, right)

        return left
    def equality(self):
        # Start by parsing the left-hand side (equality can be part of comparisons)
        left = self.term()  # This can be a basic expression

        # Check for equality operator '=='
        while self.current().type == TOKENS['EQ']:
            op_token = self.current()
            self.eat(TOKENS['EQ'])  # Consume the '==' token
            right = self.term()  # Parse the right-hand side of the equality
            left = BinOp(left, op_token, right)  # Create a binary operation node for '=='

        return left


    def term(self):
        token = self.current()
        
        if token.type == TOKENS['NUMBER']:
            self.eat(TOKENS['NUMBER'])
            return Number(token.value)

        elif token.type == TOKENS['IDENT']:
            self.eat(TOKENS['IDENT'])
            return Var(token.value)

        elif token.type == TOKENS['STRING']:  # ✅ handle string literals here
            self.eat(TOKENS['STRING'])
            return String(token.value)

        else:
            raise Exception(f"Unexpected token {token}")
