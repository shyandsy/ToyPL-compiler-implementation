# compiler-implementation
ToyPL, toy programming language, 视频作者设计的玩具编程语言

跟着youtube视频，实现一个简单的编译器

原视频:
- [视频列表] https://www.youtube.com/channel/UCkyrFlOF7I6U-IMUxum9HrA/videos
- [第一个视频] https://www.youtube.com/watch?v=xqcd6hZD6MY

这份文档目前看起来很乱，随着理解加深，我会在后续持续重构它
> 过早优化是万恶之源

## 01 
介绍编译原理

## 02
实现词法分析器，实现在***basic.py***

词法分析器 = 代码 -> **词法分析** -> Token列表
```
if xxx:
    xxx:
else:
    xxx
```

编译器从文件读取源代码，得到一个字符串
```
if xxx: \n xxx \n else: xxx
```

分词 -> 一句代码切分成token

token: 词法单元 => <token-name, attribute-value>

实现目标算术器：
- 1 + 1 - 2 + 4 = 4
- (1 + 1) * 2 = 4
- 1 *+ 1 = Error

## 03
实现语法分析器，实现在grammar.py

运行
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

