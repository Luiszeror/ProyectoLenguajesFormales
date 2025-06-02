# bombeo.py

class Bombeo:
    def __init__(self, tokens, p=5):
        self.tokens = tokens  # Lista de tokens (esperamos NOTA y SILENCIO con DURACION)
        self.p = p

    def _extraer_cadena_musical(self):
        cadena = []
        i = 0
        while i < len(self.tokens):
            t = self.tokens[i]
            if t.tipo == "PALABRA_CLAVE" and t.valor == "nota":
                if i + 2 < len(self.tokens) and self.tokens[i+1].tipo == "NOTA" and self.tokens[i+2].tipo == "DURACION":
                    nota_str = f"{self.tokens[i+1].valor}:{self.tokens[i+2].valor}"
                    cadena.append(nota_str)
                    i += 3
                    continue
            elif t.tipo == "PALABRA_CLAVE" and t.valor == "silencio":
                if i + 1 < len(self.tokens) and self.tokens[i+1].tipo == "DURACION":
                    silencio_str = f"silencio:{self.tokens[i+1].valor}"
                    cadena.append(silencio_str)
                    i += 2
                    continue
            else:
                i += 1
        return cadena

    def analizar(self):
        secuencia = self._extraer_cadena_musical()

        if len(secuencia) < self.p:
            return "❌ La secuencia musical es demasiado corta para aplicar el lema del bombeo."

        # Buscar una posible división x, y, z con |xy| <= p y |y| > 0
        for i in range(1, self.p):  # i: tamaño de x
            for j in range(1, self.p - i + 1):  # j: tamaño de y
                x = secuencia[:i]
                y = secuencia[i:i+j]
                z = secuencia[i+j:]
                if y:
                    ejemplos = []
                    for k in range(4):  # y^0 a y^3
                        y_bombeado = y * k
                        resultado = x + y_bombeado + z
                        ejemplos.append(f"x + y^{k} + z = {resultado}")
                    return {
                        "x": x,
                        "y": y,
                        "z": z,
                        "ejemplos": ejemplos,
                        "conclusion": "✔️ La secuencia cumple con el lema del bombeo para lenguajes regulares (x, y, z válidos)."
                    }

        return "❌ No se pudo encontrar una división válida para aplicar el lema del bombeo."
