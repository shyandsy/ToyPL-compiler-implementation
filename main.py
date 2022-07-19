from lexer import Lexer
from parsers import Parser


def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_token()
    if error is not None:
        return None, error
    print(tokens)
    # 生成AST
    parser = Parser(tokens)
    ast = parser.parse()
    return ast.node, ast.error


if __name__ == '__main__':
    while True:
        text = input("basic > ")
        res, err = run("<stdin>", text)
        if err:
            print(err.as_string())
            exit()
        else:
            print(res)