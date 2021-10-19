def l_list(*args):
    return '[{<f> {<x> ' + _list(args) + '}}]'


def _list(l):
    if len(l) == 0:
        return '<x>'
    return '<f> (' + str(l[0]) + ') (' + _list(l[1::]) + ')'


def pair_list(args):
    if len(args) == 0:
        return '""'
    if len(args) >= 1:
        return '`pair` (' + args[0] + ') (' + pair_list(args[1::]) + ')'


def replace_var_names(command: str, vars: [str]) -> (str, [str]):
    global counter
    new_vars = []
    for var in vars:
        command = command.replace(var, '<' + str(counter) + '>')
        new_vars.append('<' + str(counter) + '>')
        counter += 1
    return command, new_vars


def n_plet(n):
    res = ''
    for i in range(n):
        res += '{<' + str(i) + '> '
    res += '{<f> <f> '
    for i in range(n):
        res += '<' + str(i) + '> '
    res += '}'
    for i in range(n):
        res += '}'
    return res


def plet_get_k(n, k):
    res = '{<plet> <plet>'
    for i in range(n):
        res += '{<' + str(i) + '> '

    res += '<' + str(k) + '>'
    for i in range(n):
        res += '}'

    res += '}'
    return res


def plet_set_k(n, k):
    res = '{<plet> {<val> ' + l_generators['n_plet'](n)

    for i in range(n):
        if i != k:
            res += '(' + l_generators['get_k'](n, i) + ' <plet>)'
        else:
            res += '(<val>)'

    res += '}}'
    return res


l_generators = {
    'num': lambda x: replace_var_names('[{<s> {<z> ' + '<s> (' * x + '<z>' + ')' * x + '}}]', ['<s>', '<z>'])[0],
    'list': lambda *args: replace_var_names(l_list(*args), ['<x>', '<f>'])[0],
    'pair_list': lambda *args: pair_list(args),
    'n_plet': lambda n: replace_var_names(n_plet(n), ['<' + str(i) + '>' for i in range(n)])[0],
    'get_k': lambda n, k: replace_var_names(plet_get_k(n, k), ['<plet>'] + ['<' + str(i) + '>' for i in range(n)])[0],
    'set_k': lambda n, k:
    replace_var_names(plet_set_k(n, k), ['<plet>', '<val>'] + ['<' + str(i) + '>' for i in range(n)])[0]
}

l_functions = {
    'true': ['{<x> {<y> <x>}}', '<x>', '<y>'],
    'false': ['{<x> {<y> <y>}}', '<x>', '<y>'],
    'if': ['{<c> {<t> {<f> (<c> <t> <f>)}}}', '<c>', '<t>', '<f>'],

    'not': ['{<x> `if` <x> `false` `true`}', '<x>'],
    'and': ['{<x> {<y> `if` <x> <y> `false`}}', '<x>', '<y>'],
    'or': ['{<x> {<y> `if` <x> `true` <y>}}', '<x>', '<y>'],
    'nor': ['{<x> {<y>  (`and` (`or` <x> <y>) (`not` (`and` <x> <y>)) ) }}', '<x>', '<y>'],

    'pair': ['{<x> {<y> {<f> <f> <x> <y>}}}', '<x>', '<y>', '<f>'],
    'fst': ['{<p> <p> `true`}', '<p>'],
    'snd': ['{<p> <p> `false`}', '<p>'],

    'triplet': ['{<x> {<y> {<z> {<f> <f> <x> <y> <z> }}}}', '<x>', '<y>', '<z>', '<f>'],
    'fst_t': ['{<t> <t> [{<1> {<2> {<3> <1>}}}] }', '<t>'],
    'snd_t': ['{<t> <t> [{<1> {<2> {<3> <2>}}}] }', '<t>'],
    'thd_t': ['{<t> <t> [{<1> {<2> {<3> <3>}}}] }', '<t>'],

    'Y': ['{<f> <f> <f>}', '<f>'],

    '0': ['`false`'],
    '(+1)': ['{<n> {<s> {<z> <n> <s> (<s> <z>) }}}', '<n>', '<s>', '<z>'],
    '(-1)': ['{<num> `fst` (<num>  [{<p> `pair` (`snd` <p>) (`(+1)`(`snd` <p>))}] (`pair` `0` `0`) )}', '<num>', '<p>'],
    'add': ['{<m> {<n> <m> `(+1)` <n> }}', '<m>', '<n>'],
    'sub': ['{<m> {<n> <n> `(-1)` <m>}}', '<m>', '<n>'],
    'mul': ['{<m> {<n> <m> (`add` <n>) `0`}}', '<m>', '<n>'],

    'ez': ['{<n> <n> {<_> `false`} `true`}', '<n>', '<_>'],
    'leq': ['{<m> {<n> (`ez` (`sub` <m> <n>)) }}', '<m>', '<n>'],
    'geq': ['{<m> {<n> (`ez` (`sub` <n> <m>)) }}', '<m>', '<n>'],

    'lt': ['{<m> {<n> (`leq` (`(+1)` <m>) <n>) }}', '<m>', '<n>'],
    'gt': ['{<m> {<n> (`geq` <m> (`(+1)` <n>)) }}', '<m>', '<n>'],

    'eq':  ['{<m> {<n> (`and` (`leq` <m> <n>) (`geq` <m> <n>)) }}', '<m>', '<n>'],
    'neq': ['{<m> {<n> (`or`  (`lt`  <m> <n>) (`gt`  <m> <n>)) }}', '<m>', '<n>'],

    'while': ['''(`Y` [{<while> {<memory> {<condition> {<code> 
                     ((<condition> <memory>) ((`Y` <while>) (<code> <memory>) (<condition>) (<code>)) (<memory>))
                }}}}])
    ''', '<while>', '<memory>', '<condition>', '<code>'],

    'l_head': ['[{<l> <l> [{<x>{<acc> <x>}}] "" }', '<l>', '<x>', '<acc>'],

    'for_i': ['''{<code> {<i>  
                    (`Y` [{<f> {<l> (`fst` <l>) (<f> <f> (`snd` <l>)) }}])
                    (`fst_t`
                        (<i>
                            [{<t> 
                                (`triplet` 
                                    (`pair` ((`snd_t` <t>) (`thd_t` <t>)) (`fst_t` <t>))
                                    (`snd_t` <t>) 
                                    (`(+1)` (`thd_t` <t>) ) 
                                )   
                            }]
                            (`triplet` ("") (<code>) `0`)
                        )
                    )
                }}
            '''
        , '<code>', '<i>', '<f>', '<t>'],

    'head': ['{<l> `fst` <l>}', '<l>'],
    'tail': ['{<l> `snd` <l>}', '<l>'],
    'take_i': ['{<l> {<i> `pair`  }}}'],
    'get_i': ['{<l> {<i> `fst` (<i> `snd` <l>) }}', '<l>', '<i>'],
    'set_i': ['{<l> {<i> {<var> <i> [{<l> `pair` (`fst` <l>) (`snd` <l>) }]  }}}', '<l>', '<i>', '<var>']
}
counter = 0
compiled_functions = {}


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
                function = function.replace('`' + fn + '`', '[' + sub_function + ']', 1)
                vars.extend(sub_vars)
                compiled_functions[key] = [function] + vars


def compile_simple_l_expression(l_expression, vars = []):
    l_expression, vars = replace_var_names(l_expression, vars)
    for fn in compiled_functions.keys():
        while '`' + fn + '`' in l_expression:
            l_expression, vars = replace_var_names(l_expression, vars)
            sub_function, sub_vars = compiled_functions[fn][0], compiled_functions[fn][1::]
            sub_function, sub_vars = replace_var_names(sub_function, sub_vars)
            l_expression = l_expression.replace('`' + fn + '`', '[' + sub_function + ']', 1)

    return l_expression


l_compiler()
