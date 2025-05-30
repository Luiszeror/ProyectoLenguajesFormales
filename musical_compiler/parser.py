class ParserError(Exception):
    pass

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def _actual(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def _match(self, tipo):
        if self._actual() and self._actual().tipo == tipo:
            self.pos += 1
        else:
            raise ParserError(f"Se esperaba token tipo '{tipo}', se encontró: {self._actual()}")

    def parse(self):
        if not self.tokens:
            raise ParserError("No hay tokens para analizar.")

        while self._actual():
            self._parse_instruccion()
            self._match("SEPARADOR")

    def _parse_instruccion(self):
        token = self._actual()

        if token.tipo == "PALABRA_CLAVE":
            if token.valor == "nota":
                self._parse_nota()
            elif token.valor == "silencio":
                self._parse_silencio()
            elif token.valor == "tempo":
                self._parse_tempo()
            elif token.valor == "compas":
                self._parse_compas()
            else:
                raise ParserError(f"Palabra clave desconocida: '{token.valor}'")
        else:
            raise ParserError(f"Token inesperado al inicio de instrucción: {token}")

    def _parse_nota(self):
        self._match("PALABRA_CLAVE")  # nota
        self._match("NOTA")           # C4, D3, etc.
        self._match("DURACION")       # blanca, negra...

    def _parse_silencio(self):
        self._match("PALABRA_CLAVE")  # silencio
        self._match("DURACION")

    def _parse_tempo(self):
        self._match("PALABRA_CLAVE")  # tempo
        self._match("NUMERO")         # 60–200

    def _parse_compas(self):
        self._match("PALABRA_CLAVE")  # compas
        self._match("COMPAS")         # 2/4, 3/4, 4/4
