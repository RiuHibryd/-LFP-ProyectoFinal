from scanner import Scanner

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.statements = []

    def next(self):
        self.token = self.tokens.pop(0)

    def match(self, expected):
        if self.token[0] == expected:
            t = self.token
            self.next()
            return t
        else:
            raise RuntimeError(f'Se esperaba {expected!r}, pero se encontró {self.token!r}')

    def parse(self):
        while self.peek() is not None:
            if self.peek()[0] == "---":  # Agregamos el manejo de comentarios
                self.consume("---")
                self.statements.append("---")
            else:
                self.statements.append(self.parse_stmt())
        return self.statements

    def consume(self, expected_type=None):
        if expected_type is not None:
            if self.peek()[0] == expected_type:
                token = self.tokens[self.pos]
                self.pos += 1
                return token
            else:
                raise RuntimeError(f"Error inesperado: {self.peek()[0]} en la línea {self.peek()[2]}. Se esperaba {expected_type}.")
        else:
            token = self.tokens[self.pos]
            self.pos += 1
            return token

    def parse_comment(self):
        while self.token is not None and self.token[0] != 'NEWLINE':
            self.pos += 1
            self.token = self.tokens[self.pos]
        if self.token is not None:
            self.pos += 1
            self.token = self.tokens[self.pos]

    def parse_statement(self):
        if self.token[0] == 'CREATE_DB':
            self.parse_create_db()
        elif self.token[0] == 'DROP_DB':
            self.parse_drop_db()
        # Add the rest of the statements here, similar to the examples above
        elif self.token[0] == 'SPACE':
            self.parse_comment()
        else:
            raise RuntimeError(f'Sentencia desconocida {self.token!r}')

    def parse_create_db(self):
        self.match('CREATE_DB')
        id = self.match('ID')
        self.match('EQUALS')
        self.match('NEW')
        self.match('CREATE_DB')
        self.match('LPAREN')
        self.match('RPAREN')
        self.match('SEMICOLON')
        print(f'use {id[1]}')  # Print the generated statement

    def parse_drop_db(self):
        self.match('DROP_DB')
        id = self.match('ID')
        self.match('EQUALS')
        self.match('NEW')
        self.match('DROP_DB')
        self.match('LPAREN')
        self.match('RPAREN')
        self.match('SEMICOLON')
        print(f'db.{id[1]}.dropDatabase()')

    def accept(self, token_type):
        if self.pos < len(self.tokens) and self.tokens[self.pos][0] == token_type:
            token_value = self.tokens[self.pos][1]
            self.pos += 1
            return token_value
        return None

    def accept_json_content(self):
        json_content = []
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] != "SEMICOLON":
            json_content.append(self.tokens[self.pos][1])
            self.pos += 1
        if json_content:
            return "".join(json_content)
        else:
            raise SyntaxError(f"Se esperaba contenido JSON en la línea {self.tokens[self.pos][2]}")

    def expect(self, *expected_types):
        if self.pos >= len(self.tokens):
            raise Exception("Error inesperado: fin de archivo")

        token_type, token_value, line_num, start_pos, end_pos = self.tokens[self.pos]

        if token_type in expected_types:
            self.pos += 1
            return token_value
        else:
            expected_str = " o ".join(expected_types)
            raise Exception(f"Error inesperado: {token_type} en la línea {line_num}. Se esperaba {expected_str}.")

    def parse_string(self):
        quote_type = self.token[1]  # Get the current quote type (single or double quote)
        self.next()
        start = self.token[3]
        while self.token is not None and (self.token[1] != quote_type):
            self.next()
        if self.token is None:
            raise RuntimeError('Se esperaba una comilla de cierre')
        if self.token[1] != quote_type:
            raise RuntimeError(f'Error inesperado: {self.token[1]!r} en la línea {self.token[2]}. Se esperaba {quote_type!r}.')
        end = self.token[4]
        s = self.scanner.input_str[start:end - 1]
        self.next()
        return s

    def parse_quotes(self):
        quote_token = self.accept("SQUOTE") or self.accept("DQUOTE")
        if not quote_token:
            raise Exception(f"Se esperaba una comilla simple o doble en la línea {self.tokens[self.pos][2]}")
        return quote_token

    def skip_whitespace(self):
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] == "SPACE":
            self.pos += 1

    def parse(self):
        statements = []
        try:
            while self.pos < len(self.tokens):
                if self.accept("CREATE_DB"):
                    self.expect("ID")
                    self.expect("EQUALS")
                    self.expect("NEW")
                    self.expect("CREATE_DB")
                    self.expect("LPAREN")
                    self.expect("RPAREN")
                    self.expect("SEMICOLON")
                    statements.append(("CREATE_DB", self.tokens[self.pos - 8][1]))

                elif self.accept("DROP_DB"):
                    self.expect("ID")
                    self.skip_whitespace()
                    self.expect("EQUALS")
                    self.expect("NEW")
                    self.expect("DROP_DB")
                    self.expect("LPAREN")
                    self.expect("RPAREN")
                    self.expect("SEMICOLON")
                    statements.append(("DROP_DB",))

                elif self.accept("CREATE_COLLECTION"):
                    self.expect("ID")
                    self.skip_whitespace()
                    self.expect("EQUALS")
                    self.expect("NEW")
                    self.expect("CREATE_COLLECTION")
                    self.expect("LPAREN")                    
                    collection_name = self.expect("DQUOTE", "SQUOTE")
                    self.expect("ID")
                    collection_name = self.tokens[self.pos - 1][1]
                    self.expect("DQUOTE", "SQUOTE")
                    self.expect("RPAREN")
                    self.expect("SEMICOLON")
                    statements.append(("CREATE_COLLECTION", collection_name))

                elif self.accept("DROP_COLLECTION"):
                    self.expect("ID")
                    self.skip_whitespace()
                    self.expect("EQUALS")
                    self.expect("NEW")
                    self.expect("DROP_COLLECTION")
                    self.expect("LPAREN")
                    collection_name = self.expect("DQUOTE", "SQUOTE")
                    self.expect("ID")
                    collection_name = self.tokens[self.pos - 1][1]
                    self.expect("DQUOTE", "SQUOTE")
                    self.expect("RPAREN")
                    self.expect("SEMICOLON")
                    statements.append(("DROP_COLLECTION", collection_name))

                elif self.accept("INSERT_ONE"):
                    self.expect("ID")
                    self.skip_whitespace()
                    self.expect("EQUALS")
                    self.expect("NEW")
                    self.expect("INSERT_ONE")
                    self.expect("LPAREN")
                    self.expect("DQUOTE")
                    self.expect("ID")
                    self.expect("DQUOTE")
                    self.expect("COMMA")
                    self.expect("DQUOTE") or self.expect("DQUOTE")
                    self.expect("LBRACE")
                    self.expect("DQUOTE")
                    self.expect("ID")
                    self.expect("DQUOTE")
                    self.expect("COLON")
                    self.expect("DQUOTE")
                    self.expect("ID")
                    self.expect("ID")
                    self.expect("DQUOTE")
                    self.expect("COMMA")
                    self.expect("DQUOTE")
                    self.expect("ID")
                    self.expect("DQUOTE")
                    self.expect("COLON")
                    self.expect("DQUOTE")
                    self.expect("ID")
                    self.expect("ID")
                    self.expect("DQUOTE")
                    self.expect("RBRACE")
                    self.expect("DQUOTE") or self.expect("DQUOTE")
                    self.expect("RPAREN")
                    self.expect("SEMICOLON")
                    self.skip_whitespace()
                    json_content = self.accept_json_content()
                    statements.append(("INSERT_ONE", json_content))

                elif self.accept("UPDATE_ONE"):
                    self.skip_whitespace()
                    self.expect("EQUALS")
                    self.expect("NEW")
                    self.expect("UPDATE_ONE")
                    self.expect("LPAREN")
                    json_query = self.accept_json_content()
                    self.expect("COMMA")
                    json_update = self.accept_json_content()
                    self.expect("RPAREN")
                    self.expect("SEMICOLON")
                    statements.append(("UPDATE_ONE", json_query, json_update))

                elif self.accept("DELETE_ONE"):
                    self.skip_whitespace()
                    self.expect("EQUALS")
                    self.expect("NEW")
                    self.expect("DELETE_ONE")
                    self.expect("LPAREN")
                    json_query = self.accept_json_content()
                    self.expect("RPAREN")
                    self.expect("SEMICOLON")
                    statements.append(("DELETE_ONE", json_query))

                elif self.accept("FIND_ALL"):
                    self.skip_whitespace()
                    self.expect("EQUALS")
                    self.expect("NEW")
                    self.expect("FIND_ALL")
                    self.expect("LPAREN")
                    self.expect("RPAREN")
                    self.expect("SEMICOLON")
                    statements.append(("FIND_ALL",))

                elif self.accept("FIND_ONE"):
                    self.skip_whitespace()
                    self.expect("EQUALS")
                    self.expect("NEW")
                    self.expect("FIND_ONE")
                    self.expect("LPAREN")
                    json_query = self.accept_json_content()
                    self.expect("RPAREN")
                    self.expect("SEMICOLON")
                    statements.append(("FIND_ONE", json_query))

                elif self.accept("ID"):
                    self.skip_whitespace()
                    self.expect("EQUALS")
                    self.skip_whitespace()
                    self.expect("ID")
                    self.skip_whitespace()
                    self.expect("SEMICOLON")
                    statements.append(("ASSIGNMENT", self.tokens[self.pos - 3][1], self.tokens[self.pos - 1][1]))

                else:
                    raise SyntaxError(f"Error de sintaxis en la línea {self.tokens[self.pos][2]}")

        except Exception as e:
            print(f"Error: {e}")

        return statements

if __name__ == '__main__':
    input_str = """
    # (Your input file content goes here)
    """
    scanner = Scanner(input_str)
    tokens = scanner.tokenize()
    parser = Parser(tokens)
    parser.parse()