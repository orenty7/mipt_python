from parser import Parser, AST_Node

with open('../program.lm', 'r') as file:
    program = file.read()

parser = Parser(program)
ast = parser.parse_all()
out_buffer = ''
