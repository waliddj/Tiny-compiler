import re
class ASTNode:
    pass

class BinOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Num(ASTNode):
    def __init__(self, value):
        self.value = value

class Assign(ASTNode):
    def __init__(self, identifier, value):
        self.identifier = identifier
        self.value = value

class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name

class While(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class If(ASTNode):
    def __init__(self, condition, then_body, else_body=None):
        self.condition = condition
        self.then_body = then_body
        self.else_body = else_body
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        return self.statement()

    def consume(self, expected_type):
        token = self.tokens[self.pos]
        if token[0] == expected_type:
            self.pos += 1
            return token
        raise Exception(f'Expected {expected_type}, got {token[0]}')

    def statement(self):
        if self.pos < len(self.tokens) and self.tokens[self.pos][0] == 'WHILE':
            return self.while_statement()
        elif self.pos < len(self.tokens) and self.tokens[self.pos][0] == 'IF':
            return self.if_statement()
        else:
            node = self.assignment()
            self.consume('END')
            return node

    def assignment(self):
        identifier = self.consume('ID')
        self.consume('ASSIGN')
        expr = self.expr()
        return Assign(Identifier(identifier[1]), expr)

    def while_statement(self):
        self.consume('WHILE')
        self.consume('LPAREN')
        condition = self.expr()
        self.consume('RPAREN')
        body = self.statement()
        return While(condition, body)

    def if_statement(self):
        self.consume('IF')
        self.consume('LPAREN')
        condition = self.expr()
        self.consume('RPAREN')
        then_body = self.statement()
        else_body = None
        if self.pos < len(self.tokens) and self.tokens[self.pos][0] == 'ELSE':
            self.consume('ELSE')
            else_body = self.statement()
        return If(condition, then_body, else_body)

    def expr(self):
        node = self.term()
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] == 'OP':
            token = self.consume('OP')
            node = BinOp(left=node, op=token[1], right=self.term())
        return node

    def term(self):
        token = self.tokens[self.pos]
        if token[0] == 'NUMBER':
            self.consume('NUMBER')
            return Num(value=token[1])
        elif token[0] == 'ID':
            self.consume('ID')
            return Identifier(name=token[1])
        else:
            raise Exception(f'Unexpected token: {token[0]}')
class CodeGenerator:
    def __init__(self):
        self.instructions = []
        self.temp_count = 0

    def new_temp(self):
        self.temp_count += 1
        return f't{self.temp_count}'

    def generate(self, node):
        if isinstance(node, BinOp):
            left = self.generate(node.left)
            right = self.generate(node.right)
            temp = self.new_temp()
            self.instructions.append(f'{temp} = {left} {node.op} {right}')
            return temp
        elif isinstance(node, Num):
            return node.value
        elif isinstance(node, Assign):
            value = self.generate(node.value)
            self.instructions.append(f'{node.identifier.name} = {value}')
        elif isinstance(node, Identifier):
            return node.name
        elif isinstance(node, While):
            start_label = self.new_temp()
            end_label = self.new_temp()
            self.instructions.append(f'{start_label}:')
            condition = self.generate(node.condition)
            self.instructions.append(f'if not {condition} goto {end_label}')
            self.generate(node.body)
            self.instructions.append(f'goto {start_label}')
            self.instructions.append(f'{end_label}:')
        elif isinstance(node, If):
            then_label = self.new_temp()
            end_label = self.new_temp()
            condition = self.generate(node.condition)
            self.instructions.append(f'if {condition} goto {then_label}')
            if node.else_body:
                self.generate(node.else_body)
            self.instructions.append(f'goto {end_label}')
            self.instructions.append(f'{then_label}:')
            self.generate(node.then_body)
            self.instructions.append(f'{end_label}:')
        else:
            raise Exception('Unknown node type')

        return self.instructions

def compile_code(source_code):
    tokens = tokenize(source_code)
    parser = Parser(tokens)
    ast = parser.parse()
    codegen = CodeGenerator()
    instructions = codegen.generate(ast)
    return instructions

source_code = '''
x= 10;
if (x == 10):
x = 5
'''
instructions = compile_code(source_code)
for instr in instructions:
    print(instr)

