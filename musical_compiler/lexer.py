class Token:
    def __init__(self, tipo, valor, posicion):
        self.tipo = tipo
        self.valor = valor
        self.posicion = posicion

    def __repr__(self):
        return f"<{self.tipo}: {self.valor} @ {self.posicion}>"

class Lexer:
    def __init__(self):
        self.palabras_clave = {"nota", "silencio", "tempo", "compas"}
        self.duraciones = {"redonda", "blanca", "negra", "corchea"}
        self.notas_validas = {f"{n}{o}" for n in "ABCDEFG" for o in ["3", "4", "5"]}
        self.compases_validos = {"2/4", "3/4", "4/4"}

    def analizar(self, texto):
        tokens = []
        errores = []
        palabras = texto.replace(";", " ; ").split()

        i = 0
        while i < len(palabras):
            palabra = palabras[i]

            # tempo 120 → PALABRA_CLAVE "tempo" + NUMERO
            if palabra == "tempo":
                tokens.append(Token("PALABRA_CLAVE", palabra, i))
                i += 1
                if i < len(palabras) and palabras[i].isdigit():
                    tokens.append(Token("NUMERO", palabras[i], i))
                    i += 1
                else:
                    errores.append(f"Se esperaba un número después de 'tempo' en posición {i}")
                continue

            # compas 4/4 → PALABRA_CLAVE "compas" + COMPAS
            if palabra == "compas":
                tokens.append(Token("PALABRA_CLAVE", palabra, i))
                i += 1
                if i < len(palabras) and palabras[i] in self.compases_validos:
                    tokens.append(Token("COMPAS", palabras[i], i))
                    i += 1
                else:
                    errores.append(f"Compás inválido después de 'compas' en posición {i}")
                continue

            # palabras clave sueltas
            if palabra in self.palabras_clave:
                tokens.append(Token("PALABRA_CLAVE", palabra, i))
                i += 1
                continue

            # nota válida (Ej: C4, A5)
            if palabra in self.notas_validas:
                tokens.append(Token("NOTA", palabra, i))
                i += 1
                continue

            # duración musical
            if palabra in self.duraciones:
                tokens.append(Token("DURACION", palabra, i))
                i += 1
                continue

            # separador
            if palabra == ";":
                tokens.append(Token("SEPARADOR", palabra, i))
                i += 1
                continue

            # número aislado
            if palabra.isdigit():
                tokens.append(Token("NUMERO", palabra, i))
                i += 1
                continue

            # símbolo no reconocido
            errores.append(f"Simb. no reconocido '{palabra}' en posición {i}")
            i += 1

        if errores:
            raise ValueError("\n".join(errores))

        return tokens
