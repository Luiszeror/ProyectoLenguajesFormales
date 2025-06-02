from music21 import stream, note, meter, tempo

class MusicGenerator:
    def __init__(self, tokens):
        self.tokens = tokens

    def generar(self):
        s = stream.Stream()
        debug_log = []

        dur_map = {
            "redonda": 4.0,
            "blanca": 2.0,
            "negra": 1.0,
            "corchea": 0.5
        }

        i = 0
        while i < len(self.tokens):
            token = self.tokens[i]

            if token.tipo == "PALABRA_CLAVE":
                # 🎵 TEMPO
                if token.valor == "tempo" and i+1 < len(self.tokens) and self.tokens[i+1].tipo == "NUMERO":
                    bpm = int(self.tokens[i+1].valor)
                    s.append(tempo.MetronomeMark(number=bpm))
                    debug_log.append(f"[TEMPO] Token: {token.valor} → BPM = {bpm} (Token siguiente: {self.tokens[i+1].valor})")
                    i += 2
                    continue

                # 🎼 COMPÁS
                elif token.valor == "compas" and i+1 < len(self.tokens) and self.tokens[i+1].tipo == "COMPAS":
                    compas = self.tokens[i+1].valor
                    s.append(meter.TimeSignature(compas))
                    debug_log.append(f"[COMPÁS] Token: {token.valor} → Compás agregado: {compas} (Token siguiente: {self.tokens[i+1].valor})")
                    i += 2
                    continue

                # 🎶 NOTA
                elif token.valor == "nota" and i+2 < len(self.tokens):
                    if self.tokens[i+1].tipo == "NOTA" and self.tokens[i+2].tipo == "DURACION":
                        tono = self.tokens[i+1].valor
                        duracion = self.tokens[i+2].valor
                        dur = dur_map.get(duracion, 1.0)
                        s.append(note.Note(tono, quarterLength=dur))
                        debug_log.append(
                            f"[NOTA] Token: {token.valor} → Nota = {tono}, Duración = {duracion} ({dur})"
                        )
                        i += 3
                        continue

                # 🤫 SILENCIO
                elif token.valor == "silencio" and i+1 < len(self.tokens) and self.tokens[i+1].tipo == "DURACION":
                    duracion = self.tokens[i+1].valor
                    dur = dur_map.get(duracion, 1.0)
                    s.append(note.Rest(quarterLength=dur))
                    debug_log.append(
                        f"[SILENCIO] Token: {token.valor} → Silencio de duración {duracion} ({dur})"
                    )
                    i += 2
                    continue

            i += 1

        return s, debug_log
