from lexer import Lexer


class AST_Node:
    def __init__(self, node_type, op1=None, op2=None, op3=None):
        self.node_type = node_type
        self.op1 = op1
        self.op2 = op2
        self.op3 = op3


class Parser:
    SET, IF, IF_ELSE, WHILE, VAR, ADD, SUB, MUL, EQ, NEQ, LT, GT, STR, NUM, SEQ, AND, OR, NOT = \
        'SET, IF, IF_ELSE, WHILE, VAR, ADD, SUB, MUL, EQ, NEQ, LT, GT, STR, NUM, SEQ, AND, OR, NOT'.split(', ')

    def __init__(self, program):
        self.lexer = Lexer(program)
        self.lexer.next_token()

    def error(self, msg):
        raise Exception('Parser error: ', msg)

    def parse_expression_operand(self):
        if self.lexer.t_type == Lexer.NUM:
            return AST_Node(Parser.NUM, self.lexer.t_value)
        elif self.lexer.t_type == Lexer.STR:
            return AST_Node(Parser.STR, self.lexer.t_value)
        elif self.lexer.t_type == Lexer.IDENT:
            return AST_Node(Parser.VAR, self.lexer.t_value)
        else:
            self.error("Expected num, string literal or variable")

    def parse_expression(self):
        if self.lexer.t_type == Lexer.NOT:
            self.lexer.next_token()
            expression = AST_Node(Lexer.NOT, self.parse_expression_operand())
        else:
            expression = self.parse_expression_operand()

        self.lexer.next_token()
        while self.lexer.t_type != Lexer.NEWL and self.lexer.t_type != Lexer.LBRACE:
            if self.lexer.t_type == Lexer.EQ:
                operation = Parser.EQ
            elif self.lexer.t_type == Lexer.NEQ:
                operation = Parser.NEQ
            elif self.lexer.t_type == Lexer.LT:
                operation = Parser.LT
            elif self.lexer.t_type == Lexer.GT:
                operation = Parser.GT
            elif self.lexer.t_type == Lexer.PLUS:
                operation = Parser.ADD
            elif self.lexer.t_type == Lexer.MINUS:
                operation = Parser.SUB
            elif self.lexer.t_type == Lexer.MUL:
                operation = Parser.MUL
            elif self.lexer.t_type == Lexer.NOT:
                operation = Parser.NOT
            elif self.lexer.t_type == Lexer.AND:
                operation = Parser.AND
            elif self.lexer.t_type == Lexer.OR:
                operation = Parser.OR
            else:
                self.error('Unknown operation')

            self.lexer.next_token()
            expression = AST_Node(operation, expression, self.parse_expression_operand())
            self.lexer.next_token()

        return expression

    def _remove_nl(self):
        while self.lexer.t_type == Lexer.NEWL:
            self.lexer.next_token()

    def parse_braced_block(self):
        self._remove_nl()
        if self.lexer.t_type != Lexer.LBRACE:
            self.error('Expected "{" after operator')

        self.lexer.next_token()
        self._remove_nl()

        if self.lexer.t_type == Lexer.RBRACE:
            return None
        body = self.parse()
        self._remove_nl()
        while self.lexer.t_type != Lexer.RBRACE:
            body = AST_Node(Parser.SEQ, body, self.parse())
            self._remove_nl()

        return body

    def parse_all(self):
        command = self.parse()
        if command is None:
            return command

        next_command = self.parse()
        while next_command is not None:
            command = AST_Node(Parser.SEQ, command, next_command)
            next_command = self.parse()

        return command

    def parse(self):
        if self.lexer.t_type == Lexer.IDENT:
            var = AST_Node(Parser.VAR, self.lexer.t_value)
            self.lexer.next_token()
            if self.lexer.t_type != Lexer.ASSGN:
                self.error('Expected assignment after var name')
            self.lexer.next_token()
            ast_node = AST_Node(Parser.SET, op1=var, op2=self.parse_expression())

        elif self.lexer.t_type == Lexer.IF:
            self.lexer.next_token()

            condition = self.parse_expression()

            if_body = self.parse_braced_block()

            self.lexer.next_token()
            if self.lexer.t_type == Lexer.ELSE:
                self.lexer.next_token()
                else_body = self.parse_braced_block()
                self.lexer.next_token()
                ast_node = AST_Node(Parser.IF_ELSE, condition, if_body, else_body)
            else:
                ast_node = AST_Node(Parser.IF, condition, if_body)

        elif self.lexer.t_type == Lexer.WHILE:
            self.lexer.next_token()

            condition = self.parse_expression()

            while_body = self.parse_braced_block()
            self.lexer.next_token()
            ast_node = AST_Node(Parser.WHILE, condition, while_body)
        elif self.lexer.t_type == Lexer.NEWL:
            self._remove_nl()
            return self.parse()
        elif self.lexer.t_type == Lexer.EOF:
            return None
        else:
            self.error('Unexpected token: ' + self.lexer.t_type)

        return ast_node
