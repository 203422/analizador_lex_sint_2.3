import ply.lex as lex

# Lista de tokens
tokens = [
    'IDENTIFIER', 'NUMBER', 'STRING',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'ASSIGN',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'SEMI', 'DOT'
]

# Palabras reservadas
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

# Añadir las palabras reservadas a los tokens
tokens = tokens + list(reserved.values())

# Expresiones regulares para tokens simples
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_ASSIGN = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMI = r';'
t_DOT = r'\.'

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Expresión regular para identificadores
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')  # Check for reserved words
    return t

# Expresión regular para números
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Expresión regular para cadenas de texto
def t_STRING(t):
    r'\".*?\"'
    t.value = t.value[1:-1]  # Remover las comillas
    return t

# Contador de líneas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Manejo de errores
def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()

# Probar el lexer
data = '''
public class HolaMundo {
    public static void main(String[] args) {
        System.out.println("Hola mundo");
    }
}
'''

lexer.input(data)

while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)
