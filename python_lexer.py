from sly import Lexer

class python_lexer(Lexer):
    # Token yang akan digunakan

    tokens = { NAMA, ANGKA, STRING, NYETAK, MENAWA, PADHAKARO,  
               LIYANE, MULA, NJALANI, KANGGO, LEBIHSEKO, KURANGSEKO,
               ORAPODHO, MOD, FUNC, NGANTI, LSPK, KSPK}
    ignore = '\t '

    literals = { '=', '+', '-', '/', '*', '(', ')', ',', ';' }

    # Regular expression rules untuk tokens
    PADHAKARO          = r'=='
    LEBIHSEKO          = r'>'
    KURANGSEKO         = r'<'
    LSPK               = r'>='
    KSPK               = r'<='
    ORAPODHO           = r'!='
    MOD                = r'\%'

    NYETAK       = r"nyetak"
    MENAWA       = r'menawa'
    LIYANE       = r'liyane'
    MULA         = r'mula'
    NJALANI      = r'njalani'
    KANGGO       = r'kanggo'
    FUNC         = r'func'
    NGANTI       = r'nganti'

    STRING            = r'\".*?\"'
    NAMA              = r'[a-zA-Z_][a-zA-Z0-9_]*'

    @_(r'\d+')
    def ANGKA(self, t):
        t.value = int(t.value)
        return t

    # Abaikan komentar
    ignore_comment = r'\#.*'
    
    # Line numbers
    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')
    
    # Menghitung kolom
    def find_column(text, token):
        last_cr = text.rfind('\n', 0, token.index)
        if last_cr < 0:
            last_cr = 0
        column = (token.index - last_cr) + 1
        return column
    
    def __init__(self):
        self.nesting_level = 0
    
    @_(r'\%')
    def mod(self, t):
        t.type = '%'
        return t

    @_(r'\{')
    def bracel(self, t):
        t.type = '{'
        self.nesting_level += 1
        return t
    
    @_(r'\}')
    def bracer(self, t):
        t.type = '}'
        self.nesting_level -= 1
        return t
    
    def error(self, t):
        print('Baris %d: Karakter tidak ada %r' % (self.lineno, t.value[0]))
        self.index += 1

if __name__ == '__main__':
    lexer = python_lexer()
    env = {}
    while True:
        try:
            text = input('pythonlexer = ')
        except EOFError:
            break
        if text:
            lex = lexer.tokenize(text)
            for token in lex:
                print(token)
