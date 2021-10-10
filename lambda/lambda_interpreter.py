from enum import Enum
from typing import TypedDict
import time
# from time import sleep, clock
from datetime import datetime


class ExpressionType(Enum):
    STRING = 0
    LAMBDA = 1


allowed_name_symbols = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz1234567890"


class Lambda:
    def __init__(self, var_name, body):
        for i in var_name:
            if i not in allowed_name_symbols:
                raise Exception("Incorrect name error")

        self.var_name = var_name
        self.body = body

    def _is_var(self, i):
        if self.body[i:i + len(self.var_name):] != self.var_name:
            return False
        if ((i > 0 and self.body[i - 1] in allowed_name_symbols) or
                (i + len(self.var_name) < len(self.body) and self.body[
                    i + len(self.var_name)] in allowed_name_symbols)):
            return False
        return True

    def eval(self, arg):
        result = ''
        i = 0
        while i < len(self.body):
            if i + len(self.var_name) <= len(self.body) and self._is_var(i):
                result += arg
                i += len(self.var_name)
            else:
                result += self.body[i]
                i += 1

        return result


# program = input()


def remove_spaces(string):
    while len(string) > 0 and string[0] == ' ':
        string = string[1::]
    while len(string) > 0 and string[-1] == ' ':
        string = string[:-1:]

    i = 0
    prev_space = False
    in_literal = False
    while i < len(string):
        if string[i] == '"':
            in_literal = not in_literal
        if in_literal:
            i += 1
            continue
        if string[i] == ' ':
            if prev_space:
                string = string[:i:] + string[i + 1::]
            else:
                prev_space = True
                i += 1
        else:
            prev_space = False
            i += 1

    return string


out_buffer = ""


def parse(program):
    global out_buffer
    program = remove_spaces(program)
    if program[0] == '"':
        expr = {
            'type': ExpressionType.STRING,
            'literal': ''
        }
        for i in range(1, len(program)):
            if program[i] == '"':
                break
            expr['literal'] += program[i]

        return expr, program[i + 1::]

    elif program[0] == "(":
        expr = {
            'type': ExpressionType.LAMBDA,
            'expression': ''
        }
        brackets = 0
        i = 0
        while i < len(program):
            expr['expression'] += program[i]
            if program[i] == '(':
                brackets += 1
            elif program[i] == ')':
                brackets -= 1

            if brackets == 0:
                break

            if brackets < 0:
                raise Exception("mismatched brackets in l-expression")
            i += 1
        else:
            if brackets != 0:
                raise Exception("mismatched brackets in l-expression")
        program = program[i + 1::]
        i = 1
        var_name = ''
        while i < len(expr['expression']) and expr['expression'][i] in allowed_name_symbols:
            var_name += expr['expression'][i]
            i += 1

        body = expr['expression'][i:len(expr['expression']) - 1:]
        expr['lambda'] = Lambda(var_name, body)
        return expr, program

    else:
        raise Exception("Wrong l-expression error")


def eval(program):
    global out_buffer
    expr, rest = parse(program)
    if expr['type'] == ExpressionType.STRING:
        out_buffer += expr['literal']
        return rest
    else:
        expr2, rest = parse(rest)
        if expr2['type'] == ExpressionType.STRING:
            return expr['lambda'].eval('"' + expr2['literal'] + '"') + rest
        else:
            return expr['lambda'].eval(expr2['expression']) + rest


if __name__ == "__main__":
    EPS = 5
    program = '(a1 (a2 (a3 a1 a2 a3))) (a5 (a6 (a7 a5 a6 a7))) (x (y y))  (a8(a9 a9)) (a10(a11 a10)) "FALSE" "TRUE"'
    time_millis = time.time_ns() / 10 ** 6


    def tick():
        global time_millis
        time_to_next_tick = time_millis + 1000 / EPS - time.time_ns() / 10 ** 6
        if time_to_next_tick > 0:
            time.sleep(time_to_next_tick / 1000)
        time_millis = time.time_ns() / 10 ** 6


    while program != '':
        print(program)
        program = eval(program)

        tick()
