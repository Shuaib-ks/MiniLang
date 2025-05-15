import re
from token_types import TOKENS

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"{self.type}:{self.value}" if self.value else f"{self.type}"

class Lexer:
    def __init__(self, code):
        self.code = code
        self.pos = 0
        self.tokens = []

    def tokenize(self):
        while self.pos < len(self.code):
            current = self.code[self.pos]

            if current.isspace():
                self.pos += 1
                continue
            elif current.isdigit():
                self.tokens.append(self.number())
            elif current == ':':
                self.tokens.append(Token(TOKENS['COLON'], ':'))
                self.pos += 1
            elif current.isalpha():
                self.tokens.append(self.identifier())
            elif current == '+':
                self.tokens.append(Token(TOKENS['PLUS']))
                self.pos += 1
            elif current == '-':
                self.tokens.append(Token(TOKENS['MINUS']))
                self.pos += 1
            elif current == '*':
                self.tokens.append(Token(TOKENS['MULT']))
                self.pos += 1
            elif current == '/':
                self.tokens.append(Token(TOKENS['DIV']))
                self.pos += 1
            elif current == '=':
                if self.peek() == '=':
                    self.tokens.append(Token(TOKENS['EQ']))
                    self.pos += 2
                else:
                    self.tokens.append(Token(TOKENS['ASSIGN']))
                    self.pos += 1
            elif current == '!':
                if self.peek() == '=':
                    self.tokens.append(Token(TOKENS['NE']))
                    self.pos += 2
                else:
                    raise Exception("Invalid character !")
            elif current == '<':
                if self.peek() == '=':
                    self.tokens.append(Token(TOKENS['LE']))
                    self.pos += 2
                else:
                    self.tokens.append(Token(TOKENS['LT']))
                    self.pos += 1
            elif current == '>':
                if self.peek() == '=':
                    self.tokens.append(Token(TOKENS['GE']))
                    self.pos += 2
                else:
                    self.tokens.append(Token(TOKENS['GT']))
                    self.pos += 1
            elif current == '(':
                self.tokens.append(Token(TOKENS['LPAREN']))
                self.pos += 1
            elif current == ')':
                self.tokens.append(Token(TOKENS['RPAREN']))
                self.pos += 1
            else:
                raise Exception(f"Unknown character: {current}")

        self.tokens.append(Token(TOKENS['EOF']))
        return self.tokens

    def peek(self):
        return self.code[self.pos + 1] if self.pos + 1 < len(self.code) else '\0'

    def number(self):
        num_str = ''
        while self.pos < len(self.code) and self.code[self.pos].isdigit():
            num_str += self.code[self.pos]
            self.pos += 1
        return Token(TOKENS['NUMBER'], int(num_str))

    def identifier(self):
        id_str = ''
        while self.pos < len(self.code) and (self.code[self.pos].isalnum() or self.code[self.pos] == '_'):
            id_str += self.code[self.pos]
            self.pos += 1
        if id_str in ['if', 'else', 'while', 'print']:
            return Token(TOKENS[id_str.upper()])
        return Token(TOKENS['IDENT'], id_str)
