from pyclbr import Function
from sly import Parser

class python_parser(Parser):

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

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS'),
    )

    def __init__(self):
        self.env = { }
        
    # Grammar rules
    @_('')
    def statement(self, p):
        pass

    @_('NAMA')
    def expr(self, p):
        return ('nama', p.NAMA)

    @_('ANGKA')
    def expr(self, p):
        return ('angka', p.ANGKA)

    @_('expr')
    def statement(self, p):
        return(p.expr)

    @_('expr "+" expr')
    def expr(self, p):
        return ('tambah', p.expr0, p.expr1)
    
    @_('expr "-" expr')
    def expr(self, p):
        return ('kurang', p.expr0, p.expr1)

    @_('expr "*" expr')
    def expr(self, p):
        return ('kali', p.expr0, p.expr1)
    
    @_('expr "/" expr')
    def expr(self, p):
        return ('bagi', p.expr0, p.expr1)

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return p.expr
    
    @_('KANGGO assign NGANTI expr MULA statement')
    def statement(self, p):
        return('for_loop', ('for_loop_setup', p.assign, p.expr), p.statement)

    @_('MENAWA condition MULA statement LIYANE statement')
    def statement(self, p):
        return('if_stmt', p.condition, ('branch', p.statement0, p.statement1))
    
    @_('FUNC NAMA "(" ")" NJALANI statement')
    def statement(self, p):
        return('func_def', p.NAMA, p.statement)
    
    @_('NAMA "(" ")"')
    def statement(self, p):
        return('func_call', p.NAMA)
    
    @_('expr PADHAKARO expr')
    def condition(self, p):
        return('condition_padhakaro', p.expr0, p.expr1)

    @_('assign')
    def statement(self, p):
        return p.assign
    
    @_('NAMA "=" expr')
    def assign(self, p):
        return('assign', p.NAMA, p.expr)
    
    @_('NAMA "=" STRING')
    def assign(self, p):
        return('nama_assign', p.NAMA, p.STRING)
    
    @_('NYETAK expr')
    def expr(self, p):
        return('nyetak', p.expr)
    
    @_('NYETAK STRING')
    def statement(self, p):
        return('nyetak', p.STRING)

    @_('expr LSPK expr')
    def expr(self, p):
        return('lspk', p.expr0, p.expr1)
    
    @_('expr KSPK expr')
    def expr(self, p):
        return('kspk', p.expr0, p.expr1)
    
    @_('expr LEBIHSEKO expr')
    def expr(self, p):
        return('lebihseko', p.expr0, p.expr1)

    @_('expr KURANGSEKO expr')
    def expr(self, p):
        return('kurangseko', p.expr0, p.expr1)

    @_('expr ORAPODHO expr')
    def expr(self, p):
        return('orapodho', p.expr0, p.expr1)
    
    @_('expr MOD expr')
    def expr(self, p):
        return('mod', p.expr0, p.expr1)

if __name__ == '__main__':
    lexer = python_lexer()
    parser = python_parser()
    env = {}

    while True:
        try:
            text = input('pythonparser > ')
        except EOFError:
            break
        if text:
            tree = parser.parse(lexer.tokenize(text))
            print(tree)
