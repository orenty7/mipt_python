from parser import Parser, AST_Node
from l_functions import *


class Compiler:
    variables = {}
    var_counter = 0

    def __init__(self, program):
        parser = Parser(program)
        self.ast = parser.parse_all()

    def error(self, msg):
        raise Exception('Compiler error:', msg)

    def map_var_memory(self, node):
        if type(node) != AST_Node:
            return

        if node.node_type == Parser.VAR:
            if node.op1 not in self.variables:
                self.variables[node.op1] = self.var_counter
                self.var_counter += 1
            return

        self.map_var_memory(node.op1)
        self.map_var_memory(node.op2)
        self.map_var_memory(node.op3)

    def set_var(self, varname, value):
        return '(' + l_generators['set_k'](self.var_counter, self.variables[varname]) + ' <memory> (' + str(value) + '))'

    def get_var(self, varname):
        return '(' + l_generators['get_k'](self.var_counter, self.variables[varname]) + ' <memory>)'

    def compile_expression(self, ast):
        if ast.node_type == Parser.NUM:
            return l_generators['num'](ast.op1)
        elif ast.node_type == Parser.STR:
            return '"' + ast.op1 + '"'
        elif ast.node_type == Parser.VAR:
            return self.get_var(ast.op1)
        elif ast.node_type == Parser.ADD:
            return compile_simple_l_expression('(`add` (' +
                                               self.compile_expression(ast.op1) + ') (' +
                                               self.compile_expression(ast.op2) + '))')
        elif ast.node_type == Parser.SUB:
            return compile_simple_l_expression('(`sub` (' +
                                               self.compile_expression(ast.op1) + ') (' +
                                               self.compile_expression(ast.op2) + '))')
        elif ast.node_type == Parser.MUL:
            return compile_simple_l_expression('(`mul` (' +
                                               self.compile_expression(ast.op1) + ') (' +
                                               self.compile_expression(ast.op2) + '))')
        elif ast.node_type == Parser.EQ:
            return compile_simple_l_expression('(`eq` (' +
                                               self.compile_expression(ast.op1) + ') (' +
                                               self.compile_expression(ast.op2) + '))')
        elif ast.node_type == Parser.NEQ:
            return compile_simple_l_expression('(`neq` (' +
                                               self.compile_expression(ast.op1) + ') (' +
                                               self.compile_expression(ast.op2) + '))')
        elif ast.node_type == Parser.LT:
            return compile_simple_l_expression('(`lt` (' +
                                               self.compile_expression(ast.op1) + ') (' +
                                               self.compile_expression(ast.op2) + '))')
        elif ast.node_type == Parser.GT:
            return compile_simple_l_expression('(`gt` (' +
                                               self.compile_expression(ast.op1) + ') (' +
                                               self.compile_expression(ast.op2) + '))')
        else:
            self.error('Unexpected node in expression. node_type:' + ast.node_type)

    def compile_command(self, node):
        res = '[{<memory> '
        if node.node_type == Parser.SET:
            res += self.set_var(node.op1.op1, self.compile_expression(node.op2))
        elif node.node_type == Parser.IF:
            res += self.compile_expression(node.op1) + ' (' + self.compile_command(node.op2) + ' <memory>) ("")'
        elif node.node_type == Parser.IF_ELSE:
            res += self.compile_expression(node.op1) + ' (' + \
                   self.compile_command(node.op2) + ' <memory>) (' + \
                   self.compile_command(node.op3) + ' <memory>)'
        elif node.node_type == Parser.WHILE:
            res += compile_simple_l_expression('`while` <memory> (' + self.compile_expression(node.op1) + ') (' + self.compile_command(node.op2) + ')')
        elif node.node_type == Parser.SEQ:
            res += self.compile_command(node.op2) + ' (' + self.compile_command(node.op1) + ' <memory>)'
        else:
            res += '"very sad ;("'
        res += '}]'
        return res

    def compile(self):
        self.map_var_memory(self.ast)
        commands = self.compile_command(self.ast)
        memory = '(' + l_generators['n_plet'](self.var_counter) + ' ("")' * self.var_counter + ')'
        return '[{<mem> (<mem> {<a> <a>}) {x "1" x} ""}] (' + commands + ' ' + memory + ')'


program = '''
a = 5
if a < 4 {
    a = 10
} else {
    a = 3
}
'''
compiler = Compiler(program)
print(compiler.compile(), file=open('./program.lm', 'w') )
