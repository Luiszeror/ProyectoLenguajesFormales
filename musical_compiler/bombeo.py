# bombeo.py

class Bombeo:
    """
    Clase que aplica el Lema del Bombeo para lenguajes regulares a una cadena dada.
    Esta herramienta se usa con fines educativos para ilustrar la división de la cadena en x, y, z,
    y mostrar los efectos de bombear la subcadena y.
    """
    def __init__(self, cadena, longitud_p):
        self.cadena = cadena
        self.p = longitud_p  # Longitud mínima garantizada por el lema del bombeo

    def analizar(self):
        if len(self.cadena) < self.p:
            return "La cadena es demasiado corta para aplicar el lema del bombeo."

        # Intentamos encontrar una partición s = x + y + z que cumpla las condiciones del lema
        for i in range(1, self.p + 1):
            x = self.cadena[:i]
            for j in range(1, self.p - i + 1):
                y = self.cadena[i:i + j]
                z = self.cadena[i + j:]

                if y == "":
                    continue

                # Verificamos algunas repeticiones de y (bombear)
                resultados = []
                for n in range(4):  # Bombeamos y 0, 1, 2, 3 veces
                    bombeado = x + (y * n) + z
                    resultados.append(f"n = {n}: {bombeado}")

                return {
                    "x": x,
                    "y": y,
                    "z": z,
                    "ejemplos": resultados,
                    "conclusion": (
                        "Este resultado muestra cómo se puede aplicar el lema del bombeo "
                        "para observar el comportamiento de la cadena al bombear la subcadena 'y'.\n\n"
                        "⚠️ Nota: Cumplir el lema **no garantiza** que el lenguaje sea regular, "
                        "pero si una cadena **no puede dividirse** adecuadamente, "
                        "eso indica que el lenguaje **no es regular**."
                    )
                }

        return "No se encontró una partición adecuada para aplicar el lema del bombeo."
