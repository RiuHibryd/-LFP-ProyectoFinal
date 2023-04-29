import re

class Scanner:
    def __init__(self, input_str):
        self.input_str = input_str
        self.tokens = []

def tokenize(self):
        self.tokens = []
        token_specs = [
            ("JSON_CONTENT", r'(?:\"(?:[^"\\]|\\.)*\"|\{|\}|\:|\\)'),
            ("KEYWORD", r"\b(?:nueva|CrearBD|EliminarBD|CrearColeccion|EliminarColeccion|InsertarUnico|ActualizarUnico|EliminarUnico|BuscarTodo|BuscarUnico)\b"),
            ("DELIMITER", r"[{}()\-=,.;'\":$]"),
            ("ID", r"\b[a-zA-Z_][a-zA-Z_0-9]*\b"),
            ("NUMBER", r"\d+(\.\d*)?"),
            ("WS", r"\s+"),
            ("MISMATCH", r".")
        ]

        keywords = {
            "nueva": "NEW",
            "CrearBD": "CREATE_DB",
            "EliminarBD": "DROP_DB",
            "CrearColeccion": "CREATE_COLLECTION",
            "EliminarColeccion": "DROP_COLLECTION",
            "InsertarUnico": "INSERT_ONE",
            "ActualizarUnico": "UPDATE_ONE",
            "EliminarUnico": "DELETE_ONE",
            "BuscarTodo": "FIND_ALL",
            "BuscarUnico": "FIND_ONE"
        }

        delimiters = {
            '{': 'LBRACE',
            '}': 'RBRACE',
            '(': 'LPAREN',
            ')': 'RPAREN',
            '=': 'EQUALS',
            ',': 'COMMA',
            '.': 'DOT',
            ';': 'SEMICOLON',
            '"': 'DQUOTE',
            "'": 'SQUOTE',
            ':': 'COLON',
            '$': 'DOLLAR'
        }

        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specs)
        line_num = 1
        line_start = 0

        for mo in re.finditer(tok_regex, self.input_str, re.DOTALL):
            kind = mo.lastgroup
            value = mo.group()
            column = mo.start() - line_start
            if kind == 'KEYWORD':
                kind = keywords[value]
            elif kind == 'DELIMITER':
                kind = delimiters[value]
            elif kind == 'WS':
                if '\n' in value:
                    line_start = mo.end()
                    line_num += 1
                continue
            elif kind == 'MISMATCH':
                raise RuntimeError(f'{value!r} inesperado en la línea {line_num}')

            elif kind == 'JSON_CONTENT':
                value = value.replace('"', "'")

            self.tokens.append((kind, value, line_num, mo.start(), mo.end()))

        return self.tokens

if __name__ == '__main__':
    with open('input.txt', 'r', encoding='utf-8') as file:
        input_str = file.read()

    scanner = Scanner(input_str)
    tokens = scanner.tokenize()

    for token in tokens:
        print(token)
# input_str = "INSERT INTO users (id, username, email, age) VALUES (1, 'Alice', 'alice@example.com', 30);"
# tokens = lex(input_str)
# print(tokens)