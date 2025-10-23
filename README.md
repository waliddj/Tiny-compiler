# Tiny-compiler
---

## 🎯 Goals:
- Handle assignment statements  
- Parse arithmetic expressions  
- Support integer type  
- Generate three-address code

---

### 1. Tokenization:
**Tokenization** is the process of converting a sequence of characters from source code 
into a sequence of tokens. Tokens are the smallest units of meaning, such as 
keywords, identifiers, operators, and symbols. 

#### Steps in Tokenization: 
- Define Token Specification: This involves defining patterns for different 
types of tokens using regular expressions. For example, a pattern for 
recognizing numbers, identifiers, operators, and keywords. 
- Matching Tokens: The source code is scanned, and characters are matched 
against these patterns to identify tokens. 
- Handling Whitespaces and Errors: Whitespace is typically ignored, and any 
unexpected characters are handled as errors or mismatches. 


In the provided code, the token specification is defined as a list of tuples, each 
containing a token name and its corresponding regex pattern. The tokenize function 
uses these patterns to scan the input code and produce a list of tokens. 
Example:
```c
x = a + b;
```

| Lexeme | Token      |
| ------ | ---------- |
| x      | identifier |
| =      | operator   |
| a      | identifier |
| +      | operator   |
| b      | identifier |

```c
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value
```
### 2. Lexer (Lexical Analyzer):
The Lexer class converts the input text into tokens. 
The Lexer class converts the input text into tokens. 
- ```advance()```: Moves to the next character in the input. 
- ```skip_whitespace()```: Skips over any whitespace characters. 
- ```integer()```: Constructs an integer token. 
- ```_id()```: Constructs an identifier token. 
- ```get_next_token()```: Tokenizes the next meaningful character sequence.

#### Methods:
- ```__init__(self, text)```: Initializes the lexer with the input text and sets the current 
character. 
- ```advance(self)```: Moves to the next character in the input. 
- ```skip_whitespace(self)```: Skips over any whitespace characters. 
- ```integer(self)```: Constructs an integer token. 
- ```_id(self)```: Constructs an identifier token. 
- ```get_next_token(self)```: Tokenizes the next meaningful character sequence.
```c
class Lexer: 
    def __init__(self, text): 
        self.text = text 
        self.pos = 0 
        self.current_char = self.text[self.pos] 
 
    def advance(self): 
        self.pos += 1 
        if self.pos > len(self.text) - 1: 
            self.current_char = None 
        else: 
            self.current_char = self.text[self.pos] 
 
    def skip_whitespace(self): 
        while self.current_char is not None and self.current_char.isspace(): 
            self.advance() 
 
    def integer(self): 
        result = '' 
        while self.current_char is not None and self.current_char.isdigit(): 
            result += self.current_char 
            self.advance() 
        return int(result)  
 
    def _id(self): 
        result = '' 
        while self.current_char is not None and self.current_char.isalnum(): 
            result += self.current_char 
            self.advance() 
        return result 
 
    def get_next_token(self): 
        while self.current_char is not None: 
            if self.current_char.isspace(): 
                self.skip_whitespace() 
                continue 
            if self.current_char.isdigit(): 
                return Token(INTEGER, self.integer()) 
            if self.current_char.isalpha(): 
                return Token(ID, self._id()) 
            if self.current_char == '+': 
                self.advance() 
                return Token(PLUS, '+') 
            if self.current_char == '-': 
                self.advance() 
                return Token(MINUS, '-') 
            if self.current_char == '*': 
                self.advance() 
                return Token(MUL, '*') 
            if self.current_char == '/': 
                self.advance() 
                return Token(DIV, '/') 
            if self.current_char == '=': 
                self.advance() 
                return Token(ASSIGN, '=') 
            if self.current_char == '(': 
                self.advance() 
                return Token(LPAREN, '(') 
            if self.current_char == ')': 
                self.advance() 
                return Token(RPAREN, ')') 
            raise Exception('Error parsing input') 
        return Token(EOF, None) 
```
### 3. AST (Abstract Syntax Tree):
An **Abstract Syntax Tree (AST)** is a hierarchical tree representation of the abstract 
syntactic structure of source code. Each node in the tree represents a construct 
occurring in the source code.

#### Components of AST: 
- **Node Classes:** Different types of nodes represent different language 
constructs such as expressions, statements, and operations. Examples include```BinOp``` for binary operations, ```Num``` for numbers, ```Assign``` for assignment 
statements, etc.
- **Hierarchical Structure:** The tree structure captures the nested nature of 
programming constructs, reflecting the syntax of the source code.


In the code, various classes (```ASTNode```, ```BinOp```, ```Num```, ```Assign```, ```Identifier```, ```While```, ```If```) 
are defined to represent different parts of the language. These classes store the 
necessary information and relationships between different components of the source 
code. 


Nodes in the AST represent the grammatical structure of the parsed input. 
- ```BinOp```: Represents a binary operation (like addition or multiplication). 
- ``` Num```: Represents a number. 
- ```Assign```: Represents an assignment. 
- ```Var```: Represents a variable. 
    pass 
 ```c
class BinOp(AST): 
    def __init__(self, left, op, right): 
        self.left = left 
        self.op = op 
        self.right = right 
 
class Num(AST): 
    def __init__(self, value): 
        self.value = value 
 
class Assign(AST): 
    def __init__(self, left, op, right): 
        self.left = left 
        self.op = op 
        self.right = right 
 
class Var(AST): 
    def __init__(self, value): 
        self.value = value
```
Nodes in the AST represent the grammatical structure of the parsed input. 
#### Classes: 
- AST: Base class for all AST nodes.
- BinOp: Represents a binary operation (like addition or multiplication). 
- Num: Represents a number. 
- Assign: Represents an assignment. 
- Var: Represents a variable.
  
### 4. Parser
The Parser class turns a sequence of tokens into an AST. 
- ```error()```: Raises an exception for invalid syntax. 
- ```eat()```: Consumes a token if it matches the expected type. 
- ```factor()```, ```term()```, ```expr()```: These methods handle parsing of factors, terms, 
and expressions respectively. 
- ```assignment()```: Handles parsing of assignment statements. 
- ```parse()```: The main parsing function, returning the root of the AST. 
The Parser class turns a sequence of tokens into an AST. 
Methods: 
- ```__init__(self, lexer)```: Initializes the parser with a lexer and fetches the first 
token. 
- ```error(self)```: Raises an exception for invalid syntax. 
- ```eat(self, token_type)```: Consumes a token if it matches the expected type. 
- ```factor(self)```, ```term(self)```, ```expr(self)```: These methods handle parsing of factors, 
terms, and expressions respectively. 
- ```assignment(self)```: Handles parsing of assignment statements. 
- ```parse(self)```: The main parsing function, returning the root of the AST.


  Example:
  
S -> id = F ;

F -> A+B|F,  A|F,  B|F 

F->id

<img width="354" height="292" alt="image" src="https://github.com/user-attachments/assets/8f8af54c-c4e9-4533-af19-03dc4b2add97" />


```c  
      def __init__(self, lexer): 
        self.lexer = lexer 
        self.current_token = self.lexer.get_next_token() 
 
    def error(self): 
        raise Exception('Invalid syntax') 
 
    def eat(self, token_type): 
        if self.current_token.type == token_type: 
            self.current_token = self.lexer.get_next_token() 
        else: 
            self.error() 
 
    def factor(self): 
        token = self.current_token 
        if token.type == INTEGER: 
            self.eat(INTEGER) 
            return Num(token.value) 
        elif token.type == LPAREN: 
            self.eat(LPAREN) 
            node = self.expr() 
            self.eat(RPAREN) 
            return node 
        elif token.type == ID:
            self.eat(ID) 
            return Var(token.value) 
 
    def term(self): 
        node = self.factor() 
        while self.current_token.type in (MUL, DIV): 
            token = self.current_token 
            if token.type == MUL: 
                self.eat(MUL) 
            elif token.type == DIV: 
                self.eat(DIV) 
            node = BinOp(left=node, op=token, right=self.factor()) 
        return node 
 
    def expr(self): 
        node = self.term() 
        while self.current_token.type in (PLUS, MINUS): 
            token = self.current_token 
            if token.type == PLUS: 
                self.eat(PLUS) 
            elif token.type == MINUS: 
                self.eat(MINUS) 
            node = BinOp(left=node, op=token, right=self.term()) 
        return node 
 
    def assignment(self): 
        var = self.current_token 
        self.eat(ID) 
        token = self.current_token 
        self.eat(ASSIGN) 
        expr = self.expr() 
        return Assign(left=Var(var.value), op=token, right=expr) 
 
    def parse(self): 
        return self.assignment() 
```
### 5.Node Visitor  
The NodeVisitor class traverses the AST to generate three-address code. 
- ```visit()```: General method to visit nodes. 
- ```generic_visit()```: Raises an error if a visit method is not defined for a node 
type.
#### Methods: 
- ```visit(self, node)```: General method to visit nodes. 
- ```generic_visit(self, node)```: Raises an error if a visit method is not defined for a 
node type.

```c
class NodeVisitor: 
    def visit(self, node): 
        method_name = 'visit_' + type(node).__name__ 
        visitor = getattr(self, method_name, self.generic_visit) 
        return visitor(node) 
 
    def generic_visit(self, node): 
        raise Exception('No visit_{} method'.format(type(node).__name__)) 
```
### 6. TAC Generator
Generates **three-address code** by traversing the AST. 
**Three-Address Code:** A type of intermediate code used in compilers where each 
instruction has at most three operands. It simplifies optimization and code generation. 
Example: 

t1 = 10 - 4 

t2 = 3 * t1 

t3 = 5 + t2 

a = t3

Handling Different Constructs: The code generator traverses the AST and generates 
the corresponding three-address code for assignments, expressions, loops, and 
conditional statements. 


In the code, the CodeGenerator class: 


• Generates three-address code from the AST. 
• Uses temporary variables to store intermediate results. 
• Produces labels for control flow constructs like loops and conditionals.


Methods: 
- ```__init__(self)```: Initializes the TAC generator. 
- ```new_temp(self)```: Generates a new temporary variable name. 
- ```visit_Assign(self, node)```: Handles assignment nodes. 
- ```visit_BinOp(self, node)```: Handles binary operation nodes. 
- ```visit_Num(self, node)```: Handles number nodes. 
- ```visit_Var(self, node)```: Handles variable nodes. 
```c
class TACGenerator(NodeVisitor): 
    def __init__(self): 
        self.temp_count = 0 
        self.code = [] 
 
    def new_temp(self): 
        self.temp_count += 1 
        return 't{}'.format(self.temp_count) 
 
    def visit_Assign(self, node): 
        right = self.visit(node.right) 
        self.code.append('{} = {}'.format(node.left.value, right)) 
 
    def visit_BinOp(self, node): 
        left = self.visit(node.left) 
        right = self.visit(node.right) 
        temp = self.new_temp() 
        self.code.append('{} = {} {} {}'.format(temp, left, node.op.value, right)) 
        return temp 
 
    def visit_Num(self, node): 
        return str(node.value) 
 
    def visit_Var(self, node): 
        return node.value 
```

### 7. Main Function:
```c
def main(): 
   text = input('Enter an assignment statement: ') 
    lexer = Lexer(text)
    parser = Parser(lexer) 
    tree = parser.parse() 
 
    tac_generator = TACGenerator() 
    tac_generator.visit(tree) 
 
    for line in tac_generator.code: 
        print(line)
```

1) Lexical Analysis (Tokenization)
2) Syntax Analysis (Parsing)
3) Semantic Analysis (not covered)
4) Code Generation (Three-Address Code)

### 8.Test Cases

| Input                  | Output (TAC)                                             |
| ---------------------- | -------------------------------------------------------- |
| `x = 2 + 3`            | `t1 = 2 + 3` → `x = t1`                                  |
| `y = 4 * (2 + 3)`      | `t1 = 2 + 3` → `t2 = 4 * t1` → `y = t2`                  |
| `a = 5 + 3 * (10 - 4)` | `t1 = 10 - 4` → `t2 = 3 * t1` → `t3 = 5 + t2` → `a = t3` |

## Conclusien:

- Tokens identify elements of input

- Lexer turns input into tokens

- Parser builds AST

- NodeVisitor and TACGenerator produce three-address code

- Main function manages the compilation flow
