from parser import Parser, AST_Node

program = '{<81> {<82> <81> ({<85> {<86> <85> [{<87> {<88> {<89> <87> <88> (<88> <89>) }}}] <86> }} <82>) {<83> {<84> <84>}}}} {<77> {<78> <77> (<77> (<77> (<77> (<77> (<78>)))))}}{<79> {<80> <79> (<79> (<79> (<79> (<79> (<79> (<80>))))))}} {<x> "1" <x>} ""'

parser = Parser(program)
ast = parser.parse_all()


def call_lambda(var, body, arg):
    if body.node_type == Parser.VAR:
        if body.op1 == var.op1:
            return arg
        else:
            return body
    if body.node_type == Parser.STR or body.node_type == Parser.FORBIDDEN_BLOCK:
        return body
    if body.node_type == Parser.SCOPED_BLOCK:
        return AST_Node(Parser.SCOPED_BLOCK, call_lambda(var, body.op1, arg))

    if body.node_type == Parser.LAMBDA or body.node_type == Parser.SEQ:
        return AST_Node(body.node_type, call_lambda(var, body.op1, arg), call_lambda(var, body.op2, arg))


out_buffer = ''


def eval(ast):
    global out_buffer
    if ast.node_type == Parser.STR:
        out_buffer += ast.op1
        return
    if ast.node_type == Parser.SCOPED_BLOCK or ast.node_type == Parser.FORBIDDEN_BLOCK:
        return ast.op1

    if ast.node_type == Parser.SEQ:
        if ast.op1.node_type == Parser.LAMBDA:
            return call_lambda(ast.op1.op1, ast.op1.op2, ast.op2)
        elif ast.op1.node_type == Parser.STR:
            eval(ast.op1)
            return ast.op2
        else:
            return AST_Node(Parser.SEQ, eval(ast.op1), ast.op2)

    if ast.node_type == Parser.VAR or ast.node_type == Parser.LAMBDA:
        raise Exception("Evaluation error. Var or Lambda left")


def str_ast(ast):
    if ast.node_type == Parser.STR:
        return '"' + ast.op1 + '"'
    if ast.node_type == Parser.VAR:
        return ast.op1
    if ast.node_type == Parser.LAMBDA:
        return '{' + str_ast(ast.op1) + ' ' + str_ast(ast.op2) + '}'
    if ast.node_type == Parser.FORBIDDEN_BLOCK:
        return '[' + str_ast(ast.op1) + ']'
    if ast.node_type == Parser.SCOPED_BLOCK:
        return '(' + str_ast(ast.op1) + ')'
    if ast.node_type == Parser.SEQ:
        return str_ast(ast.op1) + ' ' + str_ast(ast.op2)


while ast is not None:
    print(str_ast(ast))
    ast = eval(ast)
print(out_buffer)
print(len(out_buffer))