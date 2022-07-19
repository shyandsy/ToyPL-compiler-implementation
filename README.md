# ToyPL - Compiler Implementation
toy programming language

implementation for a simple compiler, follow the video list on youtube

- [中文版文档](https://github.com/shyandsy/ToyPL-compiler-implementation/blob/main/README-CN.md)
- [问答](https://github.com/shyandsy/ToyPL-compiler-implementation/blob/main/Question-And-Answer.CN.md)


source:
- [play list] https://www.youtube.com/channel/UCkyrFlOF7I6U-IMUxum9HrA/videos
- [first video] https://www.youtube.com/watch?v=xqcd6hZD6MY

This document looks messy at the moment. I will revise it with the learning progress.
> "premature optimization is the root of all evil". 



## 01 Introduction to the compiler


## 02 Lexical Analysis
implemented in ***basic.py***

Lexer = code -> lexer -> Tokens

```
if xxx:
    xxx:
else:
    xxx
```

The compiler read the source code from a file as a large string shows below
```
if xxx: \n xxx \n else: xxx
```

tokenizer -> split the code into a list of token

token: lexical unit => <token-name, attribute-value>

实现目标算术器：
- 1 + 1 - 2 + 4 = 4
- (1 + 1) * 2 = 4
- 1 *+ 1 = Error

## 03 Syntactic analysis
implemented in ***grammar.py***

Usage
```shell
python main.py
```

tokens -> AST
[] -> 递归 -> tree

文法: 语言的规则，toypl

BNF(巴科斯范式)
context-free-grammar, 上下文无关文法，可以递归嵌套

Grammar
```
expr -> term (( PLUS | MINUS ) term)*
term -> factor （( MUL | DIV ) factor)*
factor -> INT | FLOAT
    -> (PLUS | MINUS ) factor
    -> LPAREN expr RPAREN
```

解释:
- ‘*’ 表示匹配0或者多次
- expr -> term (( PLUS | MINUS ) term)*
  - exp表达式，包括两部分
  - 表达式1：一个term表达式，
  - 表达式2：一个操作(PLUS或者MINUS)在连接一个表达式term
  - 表达式2可以出现0次或者多次
- term -> factor ( MUL | DIV ) factor)*
  - term表达式，包含两部分
  - 表达式：一个factor表达式
  - 表达式2：( MUL | DIV ) factor)*
- factor -> INT | FLOAT
    -> (PLUS | MINUS ) factor
    -> LPAREN expr RPAREN
  - 可以有一个int或者float
  - 可以有一个PLUS | MINUS
  - 可以有 '(' + 一个expr表达式 + ')'

## 04 Interpreter