# Universidad San Carlos de Guatemala
## Manual Tecnico


Lenguajes Formales y de Programacion
Seccion B+
Auxiliar: Diego Obin
Estudiante: Oscar Alfredo Sierra Sofianos
Carnet:  201908320
## Introduccion

El siguiente documento describira el codigo realizado y sus especificaciones tecnicas para el correcto funcionamiento 


## Requerimientos

- Windows 11 : Se recomienda utilizar esta version debido a que fue esta en la cual fue desarrollada
- Python 3.11.0
- Visual Studio Code 64 Bits
- 8Gb de RAM


## Instalacion de Requerimientos 

Para poder instalar Python deberemos de ir  a la pagina oficial de Python buscandola en el navegador y accediendo a la direccion web

Ya dentro de la pagina nos iremos al apartado de descargas en la seccion de Windows, esto nos redigira a las ultimas versiones de Python descargable, en nuestro caso seleccionaremos Python 3.11

Se procedera a ejecutar el ejecutable y a instalarlo



## Codigo 

#### Main,py 

El primero archivo perteneciente al codigo seria main.py el cual seria la interfaz principal la cual contendra todo lo necesario para el correcto funcionamiento de la interfaz grafica, importado de las funciones en scanner.py y parser.py 

#### Imports Necesarios
Los imports necesarios para el proyecto para el correcto funcionamiento de las funciones serian scanner y Parser los cuales mandan a llamar las funciones en dichos archivos, el import Sys E¡es una lista de directorios/carpetas donde Python busca los módulos cuando realizamos un import y finalmente PyQt5 nos permite tener un ambiente grafico parecido al que podriamos generar con Tkinter.

import sys
import scanner
from scanner import Scanner
from Parser import Parser
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QDockWidget,
                             QMenu, QMenuBar, QAction, QFileDialog, QVBoxLayout,
                             QWidget, QPlainTextEdit, QLabel, QTableWidget, QTableWidgetItem,
                             QTabWidget, QSplitter, QHBoxLayout)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

**Class MainWindows**: En esta clase va contenido lo que seria la ventana del proyecto

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Ventana principal
        self.setWindowTitle('Analizador 2.0')
        self.setGeometry(100, 100, 1200, 800)

        # Estilo personalizado
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2c3e50;
            }
            QPlainTextEdit {
                background-color: #34495e;
                color: #ecf0f1;
                border: 1px solid #7f8c8d;
            }
            QTextEdit {
                background-color: #34495e;
                color: #ecf0f1;
                border: 1px solid #7f8c8d;
            }
            QTableWidget {
                background-color: #34495e;
                color: #ecf0f1;
                border: 1px solid #7f8c8d;
                gridline-color: #7f8c8d;  # Cambiar el color de las líneas de separación aquí
            }
            QHeaderView::section {
                background-color: #2c3e50;
                color: #ecf0f1;
                border: 1px solid #7f8c8d;
                padding: 4px;
            }
            QMenuBar {
                background-color: #2c3e50;
            }
            QMenuBar::item {
                color: #ecf0f1;
                padding: 3px 10px;
            }
            QMenuBar::item:selected {
                background-color: #34495e;
            }
            QMenu {
                background-color: #2c3e50;
                color: #ecf0f1;
                border: 1px solid #7f8c8d;
            }
            QMenu::item:selected {
                background-color: #34495e;
            }
            QDockWidget {
                color: #ecf0f1;
            }
            QDockWidget::title {
                background-color: #2c3e50;
                text-align: center;
                padding: 5px;
            }
        """)

        # Agregar widgets y configuraciones adicionales para la interfaz de usuario
        self.init_ui()


##### Menu y Opciones 
Esta parte del codigo ayuda al correcto funcionamiento de las pestañas y de los menu desplegables
def init_ui(self):
        # Layout principal
        main_layout = QHBoxLayout()

        # Editor de código
        self.code_editor = QPlainTextEdit()
        self.code_editor.setFont(QFont("Courier", 12))

        # Área de resultados y errores
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.South)

        # Área de visualización de sentencias
        self.sentences_viewer = QTextEdit()
        self.sentences_viewer.setReadOnly(True)
        self.tabs.addTab(self.sentences_viewer, "Sentencias Generadas")

        # Tabla de tokens
        self.tokens_table = QTableWidget()
        self.tokens_table.setColumnCount(4)
        self.tokens_table.setHorizontalHeaderLabels(['No.', 'Tipo', 'Linea', 'Lexema'])
        self.tabs.addTab(self.tokens_table, "Tokens")

        # Área de errores
        self.errors_table = QTableWidget()
        self.errors_table.setColumnCount(5)
        self.errors_table.setHorizontalHeaderLabels(['Tipo', 'Linea', 'Columna', 'Token', 'Descripcion'])
        self.tabs.addTab(self.errors_table, "Errores")

        # Separador
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.code_editor)
        splitter.addWidget(self.tabs)
        splitter.setSizes([600, 600])
        main_layout.addWidget(splitter)

        # Crear widget central y establecer el layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Crear menú
        self.create_menu()

    def create_menu(self):
        # Menú Archivo
        self.menu_archivo = QMenu("Archivo", self)
        self.menu_analisis = QMenu("Análisis", self)
        self.menu_ver = QMenu("Ver", self)

        # Menú Archivo acciones
        self.action_nuevo = QAction("Nuevo", self)
        self.action_abrir = QAction("Abrir", self)
        self.action_guardar = QAction("Guardar", self)
        self.action_guardar_como = QAction("Guardar como", self)
        self.action_salir = QAction("Salir", self)

        self.menu_archivo.addAction(self.action_nuevo)
        self.menu_archivo.addAction(self.action_abrir)
        self.menu_archivo.addAction(self.action_guardar)
        self.menu_archivo.addAction(self.action_guardar_como)
        self.menu_archivo.addSeparator()
        self.menu_archivo.addAction(self.action_salir)

        # Menú Análisis acciones
        self.action_analizar = QAction("Generar sentencias MongoDB", self)
        self.menu_analisis.addAction(self.action_analizar)

        # Menú Ver acciones
        self.action_ver_tokens = QAction("Tokens", self)
        self.menu_ver.addAction(self.action_ver_tokens)

        # Añadir menús a la barra de menú
        self.menu_bar = QMenuBar(self)
        self.menu_bar.addMenu(self.menu_archivo)
        self.menu_bar.addMenu(self.menu_analisis)
        self.menu_bar.addMenu(self.menu_ver)
        self.setMenuBar(self.menu_bar)

        # Conectar acciones a funciones
        self.action_abrir.triggered.connect(self.open_file)
        self.action_guardar.triggered.connect(self.save_file)
        self.action_guardar_como.triggered.connect(self.save_file_as)
        self.action_nuevo.triggered.connect(self.new_file)
        self.action_salir.triggered.connect(self.close)
        self.action_analizar.triggered.connect(self.analyze_code)
        self.action_ver_tokens.triggered.connect(self.show_tokens)


##### Funciones Auxiliares

Las siguientes funciones son las necesarias para el correcto funcionamiento de las funciones asociadas al codigo utilizando los parametros de Scanner y Parser para lograr el funcionamiento 

    def new_file(self):
        if self.code_editor.document().isModified():
            pass 

        self.code_editor.clear()

    def open_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Abrir archivo", "", "Text Files (*.txt);;All Files (*)", options=options)

        if file_name:
            with open(file_name, 'r', encoding='utf-8') as file:
                self.code_editor.setPlainText(file.read())

    def save_file(self):
        if not self.code_editor.document().isModified():
            return

        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Guardar archivo", "", "Text Files (*.txt);;All Files (*)", options=options)

        if file_name:
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(self.code_editor.toPlainText())

    def save_file_as(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Guardar archivo como", "", "Text Files (*.txt);;All Files (*)", options=options)

        if file_name:
            with open(file_name, 'w') as file:
                file.write(self.code_editor.toPlainText())

    def analyze_code(self):
        input_str = self.code_editor.toPlainText()
        scanner_instance = scanner.Scanner(input_str)
        tokens = scanner_instance.tokenize()  # Obtener los tokens
        parser = Parser(tokens)  # Crear una instancia del analizador con los tokens

        try:
            result = parser.parse()
            print(result)

            mongodb_statements = []
            for stmt in result:
                if stmt[0] == "CREATE_DB":
                    mongodb_statements.append("use " + stmt[1])
                    print("CREATE_DB:", stmt[1])
                elif stmt[0] == "DROP_DB":
                    mongodb_statements.append("db.dropDatabase()")
                    print("DROP_DB")
                elif stmt[0] == "CREATE_COLLECTION":
                    mongodb_statements.append(f"db.createCollection('{stmt[1]}')")
                    print("CREATE_COLLECTION:", stmt[1])
                    mongodb_statements.append(f"db.createCollection('{stmt[1]}')")
                elif stmt[0] == "DROP_COLLECTION":
                    mongodb_statements.append(f"db.{stmt[1]}.drop()")
                elif stmt[0] == "INSERT_ONE":
                    mongodb_statements.append(f"db.{stmt[1]}.insertOne({stmt[2]})")
                elif stmt[0] == "UPDATE_ONE":
                    mongodb_statements.append(f"db.{stmt[1]}.updateOne({stmt[2]}, {stmt[3]})")
                elif stmt[0] == "DELETE_ONE":
                    mongodb_statements.append(f"db.{stmt[1]}.deleteOne({stmt[2]})")
                elif stmt[0] == "FIND_ALL":
                    mongodb_statements.append(f"db.{stmt[1]}.find()")
                elif stmt[0] == "FIND_ONE":
                    mongodb_statements.append(f"db.{stmt[1]}.findOne({stmt[2]})")

            self.sentences_viewer.setPlainText("\n".join(mongodb_statements))
            self.show_tokens(parser.tokens)
            self.tokens_table.update()
        except Exception as e:
            self.update_error_table(f"Error inesperado: {str(e)}")
            self.errors_table.update()
        print("Result:", result)

    def update_error_table(self, error_msg):
        self.errors_table.setRowCount(1)
        self.errors_table.setItem(0, 0, QTableWidgetItem("Error"))
        self.errors_table.setItem(0, 1, QTableWidgetItem("-"))
        self.errors_table.setItem(0, 2, QTableWidgetItem("-"))
        self.errors_table.setItem(0, 3, QTableWidgetItem("-"))
        self.errors_table.setItem(0, 4, QTableWidgetItem(error_msg))

    def show_tokens(self, tokens):
        scanner = Scanner(self.code_editor.toPlainText())
        tokens = scanner.tokenize()
        print("Tokens:", tokens)  # Imprime la variable tokens aquí para ver su valor
        
        if isinstance(tokens, list):
            self.tokens_table.setRowCount(len(tokens))
            for i, token in enumerate(tokens):
                self.tokens_table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
                self.tokens_table.setItem(i, 1, QTableWidgetItem(token[0]))
                self.tokens_table.setItem(i, 2, QTableWidgetItem(str(token[2])))
                self.tokens_table.setItem(i, 3, QTableWidgetItem(token[1]))
        else:
            print("Error: tokens no es una lista")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
    
## Scanner,py
El siguiente es el de Scanner.py el cual contiene la lista de palabras reservadas asignadas a las acciones correspondientes en el listado de "Tokens" que puede hacer MongoDB asi mismo el analisis de dicho texto

def is_alpha(c):
    return c.isalpha()

def is_alnum_or_underscore(c):
    return c.isalnum() or c == '_'

def is_delimiter(c):
    return c in r'{}()=,.;"\'\':}-$“”-* /'

def is_quote(c):
    return c in "\"'"


TRANSITION_TABLE = {
    'S0': {
        'is_alpha': 'S1',
        'is_delimiter': 'S2',
        'is_quote': 'S3',
    },
    'S1': {
        'is_alnum_or_underscore': 'S1',
        'not_is_alnum_or_underscore': 'S0'
    },
    'S2': {
        'not_is_delimiter': 'S0'
    },
    'S3': {
        'is_quote': 'S3_end',
    },
    'S3_end': {
        'not_is_quote': 'S0'
    },
}

def is_comment_start(input_str, i):
    return input_str[i:i+3] == '---'

class Scanner:
    def __init__(self, input_str):
        self.input_str = input_str
        self.tokens = []
        self.keywords = {
            "CrearBD": "CREATE_DB",
            "nueva": "NEW",
            "EliminarBD": "DROP_DB",
            "CrearColeccion": "CREATE_COLLECTION",
            "EliminarColeccion": "DROP_COLLECTION",
            "InsertarUnico": "INSERT_ONE",
            "ActualizarUnico": "UPDATE_ONE",
            "EliminarUnico": "DELETE_ONE",
            "BuscarTodo": "FIND_ALL",
            "BuscarUnico": "FIND_ONE"
        }

        self.delimiters = {
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
            '$': 'DOLLAR',
            '“': 'OPEN_QUOTE',
            '”': 'CLOSE_QUOTE',
            '-': 'SPACE',
            '*': 'ASTERISK',
            '/': 'BAR'
        }

    def is_identifier(self, s):
        if s[0].isalpha() or s[0] == '_':
            return all(c.isalnum() or c == '_' for c in s[1:])
        return False

    def tokenize(self):
        self.tokens = []
        state = 'S0'
        line_num = 1
        line_start = 0
        i = 0
        n = len(self.input_str)

        while i < n:
            c = self.input_str[i]

            if is_comment_start(self.input_str, i):
                while i < n and self.input_str[i] != '\n':
                    i += 1
                continue

            if state == 'S0':
                if is_alpha(c):
                    start = i
                    state = TRANSITION_TABLE[state]['is_alpha']
                elif c.isspace():
                    if c == '\n':
                        line_num += 1
                        line_start = i + 1
                    i += 1
                    continue
                elif is_delimiter(c):
                    state = TRANSITION_TABLE[state]['is_delimiter']
                    self.tokens.append((self.delimiters[c], c, line_num, i, i+1))
                elif is_quote(c):
                    start = i
                    state = TRANSITION_TABLE[state]['is_quote']
                else:
                    raise RuntimeError(f'{c!r} inesperado en la línea {line_num}')

            elif state == 'S1':
                if is_alnum_or_underscore(c):
                    state = TRANSITION_TABLE[state]['is_alnum_or_underscore']
                else:
                    token = self.input_str[start:i]
                    if token in self.keywords:
                        self.tokens.append((self.keywords[token], token, line_num, start, i))
                        if token == "nueva":
                            while self.input_str[i].isspace():
                                i += 1
                            if self.input_str[i:i+1] == "=":
                                i += 1
                                self.tokens.append(('EQUALS', '=', line_num, i-1, i))
                            else:
                                i -= 1  # Revert the index back to handle the next token properly
                    elif self.is_identifier(token):
                        self.tokens.append(('ID', token, line_num, start, i))
                    else:
                        raise RuntimeError(f'{token!r} no es una palabra clave ni un identificador válido en la línea {line_num}')
                    state = 'S0'
                    continue

            elif state == 'S2':
                state = 'S0'
                continue

            elif state == 'S3':
                if is_quote(c):
                    state = TRANSITION_TABLE[state]['is_quote']
                i += 1

            if state == 'S3_end':
                token = self.input_str[start + 1:i - 1]
                self.tokens.append(('STRING', token, line_num, start, i))
                state = 'S0'
                i += 1
            else:
                i += 1

        return self.tokens + [None]
        
El cual sigue las siguientes sintaxis Semantica 
    LEXICO:
    CrearDB
    EliminarDB
    CrearColeccion
    EliminarColeccion
    InsertarUnico
    ActualizarUnico
    EliminarUnico
    BuscarTodo
    BuscarUnico
    nueva
    (
    )
    ;
    =
    ID -> [a-z_A-Z_][a-z_A-Z_0-9]*
    NUMERO -> [0-9]+
    STRING -> "[^"]*"
    IGNORE -> \t\r
    COMENTARIOS -> //.*
                | /\([^]|\+[^/])\+/
    
Y la siguiente Sintaxis
SINTACTICO:
    init : instrucciones

    instrucciones : instruccion instrucciones
                | instruccion

    instruccion : crearDB ;
                | eliminarDB ; 
                | crearColeccion ;
                | eliminarColeccion ;
                | insertarUnico ;
                | actualizarUnico ;
                | eliminarUnico ;
                | buscarTodo ;
                | buscarUnico ;

    crearDB : CrearDB ID = nueva CrearDB ( )

    eliminarDB : EliminarDB ID = nueva EliminarDB ( )

    crearColeccion : CrearColeccion ID = nueva CrearColeccion ( STRING )

    eliminarColeccion : EliminarColeccion ID = nueva EliminarColeccion ( STRING )

    insertarUnico : InsertarUnico ID = nueva InsertarUnico ( STRING , STRING )

    actualizarUnico : ActualizarUnico ID = nueva ActualizarUnico ( STRING , STRING )

    eliminarUnico : EliminarUnico ID = nueva EliminarUnico ( STRING )

    buscarTodo : BuscarTodo ID = nueva BuscarTodo ( STRING )

    buscarUnico : BuscarUnico ID = nueva BuscarUnico ( STRING )
    
## Parser,py
    En este apartado Parser.py su funcion principal es recibir el codigo, apoyandose en scanner.py para leer las palabras reservadas y hacer su debido analisis antes de pasarlo a main.py


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
