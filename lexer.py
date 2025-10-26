import ply.lex as lex

# ------------------------------
# Palabras reservadas y tokens
# ------------------------------
palabras_reservadas = {
    'si': 'KW_SI',
    'sino': 'KW_SINO',
    'mientras': 'KW_MIENTRAS',
    'para': 'KW_PARA',
    'def': 'KW_DEF',
    'retorna': 'KW_RETORNA',
    'entero': 'KW_ENTERO',
    'flotante': 'KW_FLOTANTE',
    'imprimir': 'KW_IMPRIMIR'
}

tokens = [
    'ID', 'NUMERO', 'CADENA',
    'OP_SUMA', 'OP_RESTA', 'OP_MULT', 'OP_DIV',
    'OP_ASIGNACION',
    'OP_IGUALDAD', 'OP_DISTINTO', 'OP_MENOR', 'OP_MAYOR',
    'PAREN_ABRE', 'PAREN_CIERRA',
    'LLAVE_ABRE', 'LLAVE_CIERRA',
    'PUNTO_COMA', 'COMA',
    'ERROR_LEXICO'
] + list(palabras_reservadas.values())

# ------------------------------
# Reglas para tokens simples
# ------------------------------
t_OP_SUMA       = r'\+'
t_OP_RESTA      = r'-'
t_OP_MULT       = r'\*'
t_OP_DIV        = r'/'
t_OP_ASIGNACION = r'='
t_OP_IGUALDAD   = r'=='
t_OP_DISTINTO   = r'!='
t_OP_MENOR      = r'<'
t_OP_MAYOR      = r'>'
t_PAREN_ABRE    = r'\('
t_PAREN_CIERRA  = r'\)'
t_LLAVE_ABRE    = r'{'
t_LLAVE_CIERRA  = r'}'
t_PUNTO_COMA    = r';'
t_COMA          = r','
t_CADENA        = r'\".*?\"'

def t_NUMERO(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = palabras_reservadas.get(t.value, 'ID')
    return t

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_COMENTARIO(t):
    r'//.*'
    pass

def t_error(t):
    t.type = 'ERROR_LEXICO'
    t.value = t.value[0]
    t.lexer.skip(1)
    return t

# ------------------------------
# Crear lexer
# ------------------------------
lexer = lex.lex()

# ------------------------------
# Función para analizar código y devolver lista de tokens con características
# ------------------------------
def analizar_codigo(codigo):
    lexer.input(codigo)
    resultados = []
    for tok in lexer:
        # Determinar categoría general
        if tok.type in {"KW_SI","KW_SINO","KW_MIENTRAS","KW_PARA","KW_DEF",
                        "KW_RETORNA","KW_ENTERO","KW_FLOTANTE","KW_IMPRIMIR"}:
            categoria = "Palabra Reservada"
        elif tok.type == "ID":
            categoria = "Identificador"
        elif tok.type == "NUMERO":
            categoria = "Número"
        elif tok.type == "CADENA":
            categoria = "Cadena"
        elif tok.type in {"OP_SUMA","OP_RESTA","OP_MULT","OP_DIV","OP_ASIGNACION",
                          "OP_IGUALDAD","OP_DISTINTO","OP_MENOR","OP_MAYOR"}:
            categoria = "Operador"
        elif tok.type in {"LLAVE_ABRE","LLAVE_CIERRA","PAREN_ABRE","PAREN_CIERRA",
                          "PUNTO_COMA","COMA"}:
            categoria = "Delimitador"
        elif tok.type == "ERROR_LEXICO":
            categoria = "Error Léxico"
        else:
            categoria = "Otro"

        resultados.append({
            "linea": tok.lineno,
            "columna": tok.lexpos,
            "token": tok.type,
            "valor": tok.value,
            "categoria": categoria,
            "longitud": len(str(tok.value))
        })
    return resultados
