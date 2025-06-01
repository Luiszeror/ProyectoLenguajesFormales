from music21 import stream, note, meter, tempo
import streamlit as st

class MusicGenerator:
    def __init__(self, tokens):
        self.tokens = tokens

    def generar(self):
        s = stream.Stream()
        dur_map = {
            "redonda": 4.0,
            "blanca": 2.0,
            "negra": 1.0,
            "corchea": 0.5
        }
        log = []  # Para mostrar en Streamlit

        i = 0
        while i < len(self.tokens):
            token = self.tokens[i]
            # Log para consola y Streamlit
            print(f"[MusicGenerator] Token[{i}]: {token}")
            log.append(f"Token[{i}]: {token}")

            if token.tipo == "PALABRA_CLAVE":
                if token.valor == "tempo":
                    if i+1 < len(self.tokens) and self.tokens[i+1].tipo == "NUMERO":
                        try:
                            s.append(tempo.MetronomeMark(number=int(self.tokens[i+1].valor)))
                            log.append(f"  -> Agregado tempo {self.tokens[i+1].valor}")
                        except Exception as e:
                            log.append(f"  -> Error agregando tempo: {e}")
                        i += 2
                        continue
                elif token.valor == "compas":
                    if i+1 < len(self.tokens) and self.tokens[i+1].tipo == "COMPAS":
                        try:
                            s.append(meter.TimeSignature(self.tokens[i+1].valor))
                            log.append(f"  -> Agregado compás {self.tokens[i+1].valor}")
                        except Exception as e:
                            log.append(f"  -> Error agregando compás: {e}")
                        i += 2
                        continue
                elif token.valor == "nota":
                    if (
                        i+2 < len(self.tokens)
                        and self.tokens[i+1].tipo == "NOTA"
                        and self.tokens[i+2].tipo == "DURACION"
                    ):
                        try:
                            tono = self.tokens[i+1].valor
                            duracion = self.tokens[i+2].valor
                            dur = dur_map.get(duracion, 1.0)
                            s.append(note.Note(tono, quarterLength=dur))
                            log.append(f"  -> Agregada nota {tono} ({duracion}, {dur})")
                        except Exception as e:
                            log.append(f"  -> Error agregando nota: {e}")
                        i += 3
                        continue
                elif token.valor == "silencio":
                    if i+1 < len(self.tokens) and self.tokens[i+1].tipo == "DURACION":
                        try:
                            dur = dur_map.get(self.tokens[i+1].valor, 1.0)
                            s.append(note.Rest(quarterLength=dur))
                            log.append(f"  -> Agregado silencio ({self.tokens[i+1].valor}, {dur})")
                        except Exception as e:
                            log.append(f"  -> Error agregando silencio: {e}")
                        i += 2
                        continue
            # Omitir separadores y otros
            i += 1

        # Mostrar los logs en Streamlit
        st.markdown("### [Depuración] Tokens procesados en MusicGenerator:")
        for linea in log:
            st.text(linea)

        return s