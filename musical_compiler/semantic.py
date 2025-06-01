class SemanticError(Exception):
    pass

class SemanticAnalyzer:
    DURACION_TIEMPOS = {
        "redonda": 4,
        "blanca": 2,
        "negra": 1,
        "corchea": 0.5
    }

    COMPAS_TIEMPOS = {
        "2/4": 2,
        "3/4": 3,
        "4/4": 4
    }

    NOTAS_VALIDAS = {f"{n}{o}" for n in "ABCDEFG" for o in ["3", "4", "5"]}

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.compas_actual = "4/4"  # Valor por defecto si no se especifica

    def _actual(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def analizar(self):
        if not self.tokens:
            raise SemanticError("No hay tokens para analizar semánticamente.")

        tiempo_actual = 0  # Acumulador de tiempos para el compás actual

        while self.pos < len(self.tokens):
            token = self._actual()

            # Validar tempo
            if token.tipo == "PALABRA_CLAVE" and token.valor == "tempo":
                if self.pos + 1 >= len(self.tokens) or self.tokens[self.pos + 1].tipo != "NUMERO":
                    raise SemanticError("Falta número de tempo después de 'tempo'.")
                numero = int(self.tokens[self.pos + 1].valor)
                if not (1 <= numero <= 200):
                    raise SemanticError(f"Tempo fuera de rango (1-200): {numero}")
                self.pos += 2

            # Validar compás
            elif token.tipo == "PALABRA_CLAVE" and token.valor == "compas":
                if self.pos + 1 >= len(self.tokens) or self.tokens[self.pos + 1].tipo != "COMPAS":
                    raise SemanticError("Compás no válido o falta valor.")
                compas_valor = self.tokens[self.pos + 1].valor
                if compas_valor not in self.COMPAS_TIEMPOS:
                    raise SemanticError(f"Compás no válido: {compas_valor}")
                if tiempo_actual != 0:
                    raise SemanticError(f"Compás anterior incompleto o con exceso de tiempo: acumulado {tiempo_actual}")
                self.compas_actual = compas_valor
                self.pos += 2

            # Validar nota
            elif token.tipo == "PALABRA_CLAVE" and token.valor == "nota":
                if self.pos + 2 >= len(self.tokens):
                    raise SemanticError("Falta información para nota completa (nota + duración).")
                nota_token = self.tokens[self.pos + 1]
                duracion_token = self.tokens[self.pos + 2]
                if nota_token.tipo != "NOTA" or duracion_token.tipo != "DURACION":
                    raise SemanticError("Formato de nota inválido.")
                if nota_token.valor not in self.NOTAS_VALIDAS:
                    raise SemanticError(f"Nota inválida: {nota_token.valor}")
                duracion = duracion_token.valor
                tiempo_actual += self.DURACION_TIEMPOS.get(duracion, 0)
                self.pos += 3

            # Validar silencio
            elif token.tipo == "PALABRA_CLAVE" and token.valor == "silencio":
                if self.pos + 1 >= len(self.tokens) or self.tokens[self.pos + 1].tipo != "DURACION":
                    raise SemanticError("Silencio sin duración válida.")
                duracion = self.tokens[self.pos + 1].valor
                tiempo_actual += self.DURACION_TIEMPOS.get(duracion, 0)
                self.pos += 2

            # Separador
            elif token.tipo == "SEPARADOR":
                self.pos += 1
                # Validar si el compás debe cerrarse aquí
                if tiempo_actual == self.COMPAS_TIEMPOS[self.compas_actual]:
                    tiempo_actual = 0
                elif tiempo_actual > self.COMPAS_TIEMPOS[self.compas_actual]:
                    raise SemanticError(f"Tiempo acumulado excede el compás {self.compas_actual}: {tiempo_actual}")
                # Si es menor, seguimos acumulando

            else:
                raise SemanticError(f"Instrucción semántica no válida: {token}")

        # Verificar que el último compás esté cerrado
        if tiempo_actual != 0:
            raise SemanticError(f"El último compás está incompleto: tiempo acumulado {tiempo_actual}")
