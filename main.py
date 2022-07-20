from lexer import Lexer
from parsers import Parser
from interpreter import Interpreter, Context

def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_token()
    if error is not None:
        return None, error
    print(tokens)
    # 生成AST
    parser = Parser(tokens)
    ast = parser.parse()
    print("ast node", ast.node)
    print("ast error", ast.error)

    interpreter = Interpreter()
    context = Context('<program>')
    res = interpreter.visit(ast.node, context)

    return res.value, res.error


if __name__ == '__main__':
    while True:
        text = input("basic > ")
        res, err = run("<stdin>", text)
        if err:
            print(err.as_string())
            exit()
        else:
            print(res)