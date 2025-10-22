# Tiny-compiler
---

## 🎯 Goals:
- Handle assignment statements  
- Parse arithmetic expressions  
- Support integer type  
- Generate three-address code

---

### 1. Tokenization:
Tokenization is the process of converting a sequence of characters into tokens (keywords, identifiers, operators, symbols).

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
### 3. AST (Abstract Syntax Tree):
### 4. Parser
### 5.Node Visitor & TAC Generator
### 6. Main Function
### 7. Compilation Stages

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
