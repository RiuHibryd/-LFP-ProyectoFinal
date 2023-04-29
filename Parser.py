from scanner import Scanner

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

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

    def expect(self, expected_type):
        if self.pos >= len(self.tokens):
            raise Exception("Error inesperado: fin de archivo")

        token_type, token_value, line_num, start_pos, end_pos = self.tokens[self.pos]

        if token_type == expected_type:
            self.pos += 1
            return token_value
        else:
            raise Exception(f"Error inesperado: {token_type} en la línea {line_num}")
    def parse_json_content(self):
            json_content = []
            while self.pos < len(self.tokens) and self.tokens[self.pos][0] != "RPAREN":
                if self.tokens[self.pos][0] == "ID":
                    json_content.append(f'"{self.tokens[self.pos][1]}"')
                elif self.tokens[self.pos][0] == "DOLLAR":
                    json_content.append('$')
                elif self.tokens[self.pos][0] == "JSON_CONTENT":
                    json_content.append(self.tokens[self.pos][1].strip().replace('\'', '"'))
                else:
                    json_content.append(self.tokens[self.pos][1])
                self.pos += 1
            if json_content:
                return "".join(json_content).strip()
            else:
                raise SyntaxError(f"Se esperaba contenido JSON en la línea {self.tokens[self.pos][2]}")

    def parse(self):
        statements = []
        try:
            while self.pos < len(self.tokens):
                if self.accept("CREATE_DB"):
                    self.expect("STRING")
                    self.expect("EQUALS")
                    self.expect("NEW")
                    self.expect("CREATE_DB")
                    self.expect("LPAREN")
                    self.expect("RPAREN")
                    self.expect("SEMICOLON")
                    statements.append(("CREATE_DB", self.tokens[self.pos - 8][1]))

                elif self.accept("DROP_DB"):
                    self.expect("EQUALS")
                    self.expect("NEW")
                    self.expect("DROP_DB")
                    self.expect("LPAREN")
                    self.expect("RPAREN")
                    self.expect("SEMICOLON")
                    statements.append(("DROP_DB",))

                elif self.accept("CrearColeccion"):
                    self.expect("EQUALS")
                    self.expect("nueva")
                    self.expect("CrearColeccion")
                    self.expect("LPAREN")
                    self.expect("DQUOTE")
                    collection_name = self.tokens[self.pos][1]
                    self.expect("STRING")
                    self.expect("DQUOTE")
                    self.expect("RPAREN")
                    self.expect("SEMICOLON")
                    statements.append(("CREATE_COLLECTION", collection_name))

                elif self.accept("EliminarColeccion"):
                    self.expect("EQUALS")
                    self.expect("nueva")
                    self.expect("EliminarColeccion")
                    self.expect("LPAREN")
                    self.expect("DQUOTE")
                    collection_name = self.tokens[self.pos][1]
                    self.expect("STRING")
                    self.expect("DQUOTE")
                    self.expect("RPAREN")
                    self.expect("SEMICOLON")
                    statements.append(("DROP_COLLECTION", collection_name))

                elif self.accept("INSERT_ONE"):
                    self.expect("EQUALS")
                    self.expect("nueva")
                    self.expect("INSERTAR_UNICO")
                    self.expect("LPAREN")
                    self.expect("DQUOTE")
                    collection_name = self.tokens[self.pos][1]
                    self.expect("STRING")
                    self.expect("DQUOTE")
                    self.expect("COMMA")
                    self.expect("SQUOTE")
                    json_content = self.parse_json_content()
                    self.expect("SQUOTE")
                    self.expect("RPAREN")
                    self.expect("SEMICOLON")
                    statements.append(("INSERT_ONE", collection_name, json_content))

                elif self.accept("UPDATE_ONE"):
                    self.expect("EQUALS")
                    self.expect("nueva")
                    self.expect("ACTUALIZAR_UNICO")
                    self.expect("LPAREN")
                    self.expect("DQUOTE")
                    collection_name = self.tokens[self.pos][1]
                    self.expect("STRING")
                    self.expect("DQUOTE")
                    self.expect("COMMA")
                    self.expect("SQUOTE")
                    json_filter = self.parse_json_content()
                    self.expect("SQUOTE")
                    self.expect("COMMA")
                    self.expect("SQUOTE")
                    json_update = self.parse_json_content()
                    self.expect("SQUOTE")
                    self.expect("RPAREN")
                    self.expect("SEMICOLON")
                    statements.append(("UPDATE_ONE", collection_name, json_filter, json_update))

                elif self.accept("DELETE_ONE"):
                    self.expect("EQUALS")
                    self.expect("nueva")
                    self.expect("ELIMINAR_UNICO")
                    self.expect("LPAREN")
                    self.expect("DQUOTE")
                    collection_name = self.tokens[self.pos][1]
                    self.expect("STRING")
                    self.expect("DQUOTE")
                    self.expect("COMMA")
                    json_filter = self.parse_json_content()
                    self.expect("RPAREN")
                    self.expect("SEMICOLON")
                    statements.append(("DELETE_ONE", collection_name, json_filter))

                elif self.accept("BUSCAR_TODO"):
                    self.expect("EQUALS")
                    self.expect("nueva")
                    self.expect("BUSCAR_TODO")
                    self.expect("LPAREN")
                    self.expect("DQUOTE")
                    collection_name = self.tokens[self.pos][1]
                    self.expect("STRING")
                    self.expect("DQUOTE")
                    self.expect("RPAREN")
                    self.expect("SEMICOLON")
                    statements.append(("FIND_ALL", collection_name))

                elif self.accept("BUSCAR_UNICO"):
                    self.expect("EQUALS")
                    self.expect("nueva")
                    self.expect("BUSCAR_UNICO")
                    self.expect("LPAREN")
                    self.expect("DQUOTE")
                    collection_name = self.tokens[self.pos][1]
                    self.expect("STRING")
                    self.expect("DQUOTE")
                    self.expect("RPAREN")
                    self.expect("SEMICOLON")
                    statements.append(("FIND_ONE", collection_name))

                else:
                    raise SyntaxError(f"Error inesperado: {self.tokens[self.pos][0]} en la línea {self.tokens[self.pos][2]}")

        except SyntaxError as e:
            print(e)

        return statements

if __name__ == "__main__":
    with open("input.txt", "r") as file:
        input_str = file.read()

    scanner = Scanner(input_str)
    tokens = scanner.tokenize()

    parser = Parser(tokens)
    parse_tree = parser.parse()

    print(parse_tree)