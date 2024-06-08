from flask import Flask, request, render_template
import ply.lex as lex
import ply.yacc as yacc

app = Flask(__name__)

tokens = [
    'IDENTIFIER', 'STRING',
    'TIMES', 'DIVIDE', 'ASSIGN',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'SEMI', 'DOT',
    'LBRACKET', 'RBRACKET'
]

reserved = {
    'public': 'PUBLIC',
    'class': 'CLASS',
    'static': 'STATIC',
    'void': 'VOID',
    'main': 'MAIN',
    'String': 'STRING_TYPE',
    'System': 'SYSTEM',
    'out': 'OUT',
    'println': 'PRINTLN'
}

tokens = tokens + list(reserved.values())

t_TIMES = r'\*'
t_DIVIDE = r'/'
t_ASSIGN = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMI = r';'
t_DOT = r'\.'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'

t_ignore = ' \t'

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

def t_STRING(t):
    r'\".*?\"'
    t.value = t.value[1:-1]
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

def build_lexer():
    return lex.lex()

def build_parser():
    def p_program(p):
        'program : class_declaration'
        pass

    def p_class_declaration(p):
        'class_declaration : PUBLIC CLASS IDENTIFIER LBRACE method_declarations RBRACE'
        pass

    def p_method_declarations(p):
        '''method_declarations : method_declaration
                               | method_declarations method_declaration'''
        pass

    def p_method_declaration(p):
        'method_declaration : PUBLIC STATIC VOID MAIN LPAREN STRING_TYPE LBRACKET RBRACKET IDENTIFIER RPAREN LBRACE statement RBRACE'
        pass

    def p_statement(p):
        'statement : SYSTEM DOT OUT DOT PRINTLN LPAREN STRING RPAREN SEMI'
        pass

    def p_error(p):
        if p:
            line_number = p.lineno
            error_message = f"Error de sintaxis en '{p.value}' en la línea {line_number}"
            raise SyntaxError(error_message)
        else:
            raise SyntaxError("Error de sintaxis en EOF")

    return yacc.yacc()

@app.route('/', methods=['GET', 'POST'])
def index():
    tokens = []
    syntax_error = None

    if request.method == 'POST':
        code = request.form['code']
        lexer = build_lexer()
        lexer.input(code)

        while True:
            tok = lexer.token()
            if not tok:
                break
            tokens.append(f"{tok.type}('{tok.value}', Línea {tok.lineno}, Posición {tok.lexpos})")

        parser = build_parser()
        try:
            parser.parse(code, lexer=lexer)
        except SyntaxError as e:
            syntax_error = str(e)

    return render_template('index.html', tokens=tokens, syntax_error=syntax_error)

if __name__ == '__main__':
    app.run(debug=True)
