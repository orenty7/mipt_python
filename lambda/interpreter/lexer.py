class Lexer:
    LBRACKET, RBRACKET, LBRACE, RBRACE, LSQBRACKET, RSQBRACKET, IDENT, STR, EOF = \
        'LBRACKER, RBRACKET, LBRACE, RBRACE, LSQBRACKET, RSQBRACKET, IDENT, STR, EOF'.split(', ')

    def __init__(self, program):
        self.program = program
        self.i = 0
        self.getchar()

    def error(self, msg):
        raise Exception("Lexer error:", msg)

    def getchar(self):
        self.ch = self.program[self.i] if self.i < len(self.program) else ''
        self.i += 1

    def putback(self):
        self.i -= 1
        self.ch = self.program[self.i] if self.i < len(self.program) else ''

    allowed_var_name_symbols = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz1234567890<>'

    def next_token(self):
        self.t_type = None
        self.t_value = None
        while self.t_type is None:

            if self.ch == '':
                self.t_type = Lexer.EOF
            elif self.ch == ' ':
                self.getchar()
            elif self.ch == '(':
                self.t_type = Lexer.LBRACKET
            elif self.ch == ')':
                self.t_type = Lexer.RBRACKET
            elif self.ch == '{':
                self.t_type = Lexer.LBRACE
            elif self.ch == '}':
                self.t_type = Lexer.RBRACE
            elif self.ch == '[':
                self.t_type = Lexer.LSQBRACKET
            elif self.ch == ']':
                self.t_type = Lexer.RSQBRACKET
            elif self.ch == '"':
                self.t_type = Lexer.STR
                self.t_value = ''
                self.getchar()
                while self.ch != '"':
                    self.t_value += self.ch
                    self.getchar()

            elif self.ch in Lexer.allowed_var_name_symbols:
                self.t_type = Lexer.IDENT
                self.t_value = ''
                while self.ch in Lexer.allowed_var_name_symbols:
                    self.t_value += self.ch
                    self.getchar()

                self.putback()
            else:
                self.error('Unexpected symbol: ' + self.ch)
        self.getchar()