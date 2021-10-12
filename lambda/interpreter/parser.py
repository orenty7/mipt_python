from lexer import Lexer


class AST_Node:
    def __init__(self, node_type, op1=None, op2=None):
        self.node_type = node_type
        self.op1 = op1
        self.op2 = op2


class Parser:
    LAMBDA, SCOPED_BLOCK, FORBIDDEN_BLOCK, STR, VAR, SEQ = \
        'LAMBDA, SCOPED_BLOCK, FORBIDDEN_BLOCK, STR, VAR, SEQ'.split(', ')

    def __init__(self, program):
        self.lexer = Lexer(program)

    def error(self, msg):
        raise Exception('Parser error: ', msg)

    def parse_block(self, stop_symbol) -> AST_Node:
        self.lexer.next_token()
        block_body = self.parse()
        self.lexer.next_token()
        while self.lexer.t_type != stop_symbol:
            block_body = AST_Node(Parser.SEQ, block_body, self.parse())
            self.lexer.next_token()
        return block_body

    def parse_all(self) -> AST_Node:
        return self.parse_block(Lexer.EOF)

    def parse(self) -> AST_Node:
        if self.lexer.t_type == Lexer.LBRACE:
            self.lexer.next_token()
            if self.lexer.t_type != Lexer.IDENT:
                self.error('Expected variable name after "(" symbol')
            var = AST_Node(Parser.VAR, self.lexer.t_value)

            ast_node = AST_Node(Parser.LAMBDA, var, self.parse_block(Lexer.RBRACE))

        elif self.lexer.t_type == Lexer.LBRACKET:
            ast_node = AST_Node(Parser.SCOPED_BLOCK, self.parse_block(Lexer.RBRACKET))

        elif self.lexer.t_type == Lexer.LSQBRACKET:
            ast_node = AST_Node(Parser.FORBIDDEN_BLOCK, self.parse_block(Lexer.RSQBRACKET))

        elif self.lexer.t_type == Lexer.STR:
            ast_node = AST_Node(Parser.STR, self.lexer.t_value)
        elif self.lexer.t_type == Lexer.IDENT:
            ast_node = AST_Node(Parser.VAR, self.lexer.t_value)
        else:
            self.error('Unexpected token: ' + self.lexer.t_type)

        return ast_node
