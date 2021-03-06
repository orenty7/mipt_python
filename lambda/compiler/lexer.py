class Lexer:
    NUM, STR, IDENT, ASSGN, IF, ELSE, WHILE, LBRACKET, RBRACKET, LBRACE, RBRACE, EQ, NEQ, LT, GT, PLUS, MINUS, MUL, EOF, NEWL, AND, OR, NOT = \
        "NUM, STR, IDENT, ASSGN, IF, ELSE, WHILE, LBRACKET, RBRACKET, LBRACE, RBRACE, EQ, NEQ, LT, GT, PLUS, MINUS, MUL, EOF, NEWL, AND, OR, NOT".split(
            ', ')

    ch = ''

    def __init__(self, program: str):
        self.program = program
        self.i = 0
        self.token = None
        self.t_type = None
        self.t_value = None

    def getchar(self):
        self.ch = self.program[self.i] if self.i < len(self.program) else ''
        self.i += 1

    def putback(self):
        self.i -= 1
        self.ch = self.program[self.i] if self.i < len(self.program) else ''

    def next_token(self):
        # token = (type, value)
        t_type = None
        t_value = None
        self.getchar()
        while t_type is None:
            if len(self.ch) == 0:
                t_type = Lexer.EOF
            elif self.ch == ' ':
                self.getchar()
            elif self.ch == '\n':
                t_type = Lexer.NEWL
            elif self.ch == '(':
                t_type = Lexer.LBRACKET
            elif self.ch == ')':
                t_type = Lexer.RBRACKET
            elif self.ch == '{':
                t_type = Lexer.LBRACE
            elif self.ch == '}':
                t_type = Lexer.RBRACE
            elif self.ch == '<':
                t_type = Lexer.LT
            elif self.ch == '>':
                t_type = Lexer.GT
            elif self.ch == '+':
                t_type = Lexer.PLUS
            elif self.ch == '-':
                t_type = Lexer.MINUS
            elif self.ch == '*':
                t_type = Lexer.MUL
            elif self.ch == '&':
                t_type = Lexer.AND
            elif self.ch == '|':
                t_type = Lexer.OR
            elif self.ch == '=':
                self.getchar()
                if self.ch == '=':
                    t_type = Lexer.EQ
                else:
                    t_type = Lexer.ASSGN
                    self.putback()
            elif self.ch == '!':
                self.getchar()
                if self.ch == '=':
                    t_type = Lexer.NEQ
                else:
                    t_type = Lexer.NOT
                    self.putback()

            elif self.ch.isdigit():
                t_type = Lexer.NUM
                t_value = 0
                while self.ch.isdigit():
                    t_value = t_value * 10 + int(self.ch)
                    self.getchar()
                self.putback()

            elif self.ch == '"':
                t_type = Lexer.STR
                t_value = ''
                self.getchar()
                while self.ch != '"':
                    t_value += self.ch
                    self.getchar()
            elif self.ch.isalpha():
                t_value = ''
                while self.ch.isalnum():
                    t_value += self.ch
                    self.getchar()
                if t_value == 'if':
                    t_type = Lexer.IF
                elif t_value == 'else':
                    t_type = Lexer.ELSE
                elif t_value == 'while':
                    t_type = Lexer.WHILE
                else:
                    t_type = Lexer.IDENT
                self.putback()

        self.t_type = t_type
        self.t_value = t_value
        self.token = (t_type, t_value)
        return self.token
