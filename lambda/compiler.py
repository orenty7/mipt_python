from parser import Parser


def l_list(*args):
    return '{<f> {<x> ' + _list(args) + '}}'


def _list(l):
    if len(l) == 0:
        return '<x>'
    return '<f> (' + l[0] + ') (' + _list(l[1::]) + ')'


l_generators = {
    'num': lambda x: '{<s> {<z> ' + '<s> (' * x + '<z>' + ')' * x + '}}',
    'list': l_list
}

l_functions = {
    'true': ['{<x> {<y> <x>}}', '<x>', '<y>'],
    'false': ['{<x> {<y> <y>}}', '<x>', '<y>'],
    'if': ['{<c> {<t> {<f> <c> <t> <f>}}}', '<c>', '<t>', '<f>'],

    'not': ['{<x> `if` <x> `false` `true`}', '<x>'],
    'and': ['{<x> {<y> `if` <x> <y> `true`}}', '<x>', '<y>'],
    'or': ['{<x> {<y> `if` <x> `true` <y>}}', '<x>', '<y>'],
    'nor': [' {<x> {<y>  (`and` (`or` <x> <y>) (`not` (`and` <x> <y>)) ) }}', '<x>', '<y>'],

    '(+1)': ['{<n> {<s> {<z> <n> <s> (<s> <z>) }}}', '<n>', '<s>', '<z>'],
    'sum': ['{<m> {<n> <m> [`(+1)`] <n> }}', '<m>', '<n>'],
    'mul': ['{<m> {<n> <m> (`sum` <n>) `false`}}', '<m>', '<n>']
}
counter = 0
compiled_functions = {}


def replace_var_names(command: str, vars: [str]) -> (str, [str]):
    global counter
    new_vars = []
    for var in vars:
        command = command.replace(var, '<' + str(counter) + '>')
        new_vars.append('<' + str(counter) + '>')
        counter += 1
    return command, new_vars


def l_compiler():
    global counter, l_functions, l_generators, compiled_functions

    for key in l_functions.keys():
        command = l_functions[key][0]
        new_command, new_vars = replace_var_names(command, l_functions[key][1::])
        compiled_functions[key] = [new_command] + new_vars

        for fn in l_functions.keys():
            while '`' + fn + '`' in compiled_functions[key][0]:
                function, vars = compiled_functions[key][0], compiled_functions[key][1::]
                sub_function, sub_vars = compiled_functions[fn][0], compiled_functions[fn][1::]
                sub_function, sub_vars = replace_var_names(sub_function, sub_vars)
                function = function.replace('`' + fn + '`', sub_function, 1)
                vars.extend(sub_vars)
                compiled_functions[key] = [function] + vars


def compile_simple_l_expression(l_expression, ):
    for fn in compiled_functions.keys():
        while '`' + fn + '`' in l_expression:
            sub_function, sub_vars = compiled_functions[fn][0], compiled_functions[fn][1::]
            sub_function, sub_vars = replace_var_names(sub_function, sub_vars)
            l_expression = l_expression.replace('`' + fn + '`', sub_function, 1)

    return l_expression


l_compiler()
xor = compile_simple_l_expression('`mul` ' + replace_var_names(l_generators['num'](5), ['<s>', '<z>'])[0] +
                                  replace_var_names(l_generators['num'](6), ['<s>', '<z>'])[0] + ' {<x> "1" <x>} ""')



print(xor)


class Compiler:
    def __init__(self, program):
        parser = Parser(program)
        self.ast = parser.parse()

    def compile(self, node):
        pass
