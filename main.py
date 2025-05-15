from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from ast_nodes import *



code = """
print("Hello World!")
"""


# Run pipeline
tokens = Lexer(code).tokenize()
ast = Parser(tokens).parse()


interpreter = Interpreter()
for node in ast:
    interpreter.eval(node)
