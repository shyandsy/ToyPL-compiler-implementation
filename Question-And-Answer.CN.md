# Question And Answer

## 03 - 语法分析器

在UofM读书几年，唯一一门没学懂的课程，就是CS3030-Automata Theory and Formal Languages。
整学期从有限状态机开始，到context-free-language，再到图灵机。天天各种推导。然而一学期下来，我问自己学了个啥，啥也不是。
我还记得当初我问教授，这个语法为啥这么写，而不是那么写（请忽略细节先）。教授回答，记下他慢慢体会。

这个视频我也遇到了完全一样的问题，为啥要这么定义grammar
```
expr -> term (( PLUS | MINUS ) term)*
term -> factor （( MUL | DIV ) factor)*
factor -> INT | FLOAT
    -> (PLUS | MINUS ) factor
    -> LPAREN expr RPAREN
```
而不是
```
term -> factor （( MUL | DIV ) factor)*
expr -> term (( PLUS | MINUS ) term)*
factor -> INT | FLOAT
    -> (PLUS | MINUS ) factor
    -> LPAREN expr RPAREN
```

好在视频作者在04视频开头给出了答案。
> 怎么写都可以，但这是经验和功力的提现

也就是说，在学习之初必然会遇到"为什么不这么写"的问题.

回到问题本身。之所以这么定义grammar，是因为我们在设计数学计算器

比如：+1 * 2, 我们必然是先计算 \*，再去计算 +
再比如：+1 * (2 + 4)，也必然是先计算 \*，再计算(2 + 4)
而我们的grammar定义，其实是递归的，也就是说最下面的最先执行。因此PLUS | MINUS必须在第一行