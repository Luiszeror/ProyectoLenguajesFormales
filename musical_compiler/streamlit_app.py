import tempfile
from music21 import midi, environment
from lexer import Lexer
from parser import Parser, ParserError
from semantic import SemanticAnalyzer, SemanticError
from bombeo import Bombeo
from generator import MusicGenerator
import glob
import os
import streamlit as st

# Configuración de LilyPond (ajusta según tu instalación)
us = environment.UserSettings()


us['lilypondPath'] = r'C:\Users\hack\Downloads\lilypond-2.24.4\bin\lilypond.exe'

def main():
    st.title("🎼 Compilador Musical")

    lexer = Lexer()

    st.header("1. Entrada del código fuente")
    metodo = st.radio("Selecciona el método de entrada:", ["Escribir manualmente", "Subir archivo (.txt)"])
    codigo = ""

    if metodo == "Escribir manualmente":
        codigo = st.text_area("Introduce tu código:", height=200)
    else:
        archivo = st.file_uploader("Carga un archivo .txt", type=["txt"])
        if archivo is not None:
            contenido = archivo.read().decode("utf-8")
            st.text_area("Contenido del archivo:", value=contenido, height=200)
            codigo = contenido

    if st.button("Analizar"):
        try:
            # Limpieza opcional de PNGs antiguos
            for file in glob.glob("*-page*.png"):
                os.remove(file)

            # 1. Léxico
            tokens = lexer.analizar(codigo)
            st.success("✅ Análisis léxico completado")
            st.markdown("### Tokens reconocidos:")
            for token in tokens:
                st.code(str(token), language="text")

            # 2. Sintáctico
            parser = Parser(tokens)
            parser.parse()
            st.success("✅ Análisis sintáctico completado")

            # 3. Semántico
            sem = SemanticAnalyzer(tokens)
            resultado_semantico = sem.analizar()
            st.success("✅ Análisis semántico completado")

            # Mostrar salidas de Mealy y Moore
            st.markdown("### 🤖 Máquinas de Estado")
            st.subheader("🛠️ Máquina de Mealy (acciones)")
            for accion in sem.get_acciones_mealy():
                st.code(accion)

            st.subheader("📟 Máquina de Moore (salidas)")
            for salida in sem.get_salidas_moore():
                st.code(salida)

            # 4. Bombeo (con notación musical)
            st.markdown("---")
            st.header("📚 Lema del Bombeo")

            st.markdown(
                "El **lema del bombeo** establece que si un lenguaje es regular, "
                "entonces cualquier secuencia suficientemente larga puede dividirse como `x`, `y`, `z`, "
                "de manera que `x y^n z` también pertenezca al lenguaje."
            )

            bomba = Bombeo(tokens, p=5)
            resultado = bomba.analizar()

            if isinstance(resultado, dict):
                st.markdown(f"**División:**")
                st.code(f"x = {resultado['x']}")
                st.code(f"y = {resultado['y']}")
                st.code(f"z = {resultado['z']}")

                st.markdown("**Ejemplos bombeados:**")
                for linea in resultado['ejemplos']:
                    st.code(linea)

                st.info(resultado['conclusion'])
            else:
                st.warning(resultado)

            # 5. Generación musical
            st.markdown("---")
            st.header("🎼 Partitura y Audio")

            generator = MusicGenerator(tokens)
            musica_stream, debug_log = generator.generar()

            with st.expander("🎼 Ver partitura (todas las páginas)"):
                try:
                    lilypond_path = musica_stream.write('lilypond.png')
                    base_name = os.path.splitext(lilypond_path)[0]
                    if base_name.endswith(".ly"):
                        base_name = base_name[:-3]

                    png_files = sorted(glob.glob(f"{base_name}-page*.png"))
                    if not png_files:
                        png_files = [lilypond_path]

                    for i, png_path in enumerate(png_files):
                        with open(png_path, "rb") as img_file:
                            st.image(img_file.read(), caption=f"Página {i + 1}", use_column_width=True)
                except Exception as e:
                    st.warning("⚠️ No se pudo generar la partitura con LilyPond.")
                    st.code(str(e))

            with st.expander("🔍 Depuración: cómo se construyó la partitura"):
                for paso in debug_log:
                    st.markdown(f"• {paso}")

            # Descargar audio MIDI
            with st.expander("⬇️ Descargar audio MIDI"):
                try:
                    mf = midi.translate.streamToMidiFile(musica_stream)
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mid") as tmp:
                        mf.open(tmp.name, 'wb')
                        mf.write()
                        mf.close()

                        st.success("✅ Archivo MIDI generado.")
                        with open(tmp.name, "rb") as f:
                            st.download_button("⬇️ Descargar archivo MIDI", f, file_name="melodia.mid", mime="audio/midi")

                except Exception as e:
                    st.warning("⚠️ No se pudo generar el audio.")
                    st.code(str(e))

        except (ValueError, ParserError, SemanticError) as e:
            st.error("❌ Error detectado:")
            st.code(str(e), language="text")

if __name__ == "__main__":
    main()
