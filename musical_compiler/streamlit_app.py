
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

# 🔧 Configuración de LilyPond (debe ir antes de usar music21)
us = environment.UserSettings()
us['lilypondPath'] = r'C:\Users\hack\Downloads\lilypond-2.24.4\bin\lilypond.exe'  # AJUSTA si está en otra carpeta

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
            # 1. Análisis Léxico
            tokens = lexer.analizar(codigo)
            st.success("✅ Análisis léxico completado con éxito")
            st.markdown("### Tokens reconocidos:")
            for token in tokens:
                st.code(str(token), language="text")

            # 2. Análisis Sintáctico
            parser = Parser(tokens)
            parser.parse()
            st.success("✅ Análisis sintáctico completado con éxito")

            # 3. Análisis Semántico
            sem = SemanticAnalyzer(tokens)
            sem.analizar()
            st.success("✅ Análisis semántico completado con éxito")

            # 4. Lema del Bombeo
            st.markdown("---")
            st.header("📚 Lema del Bombeo (Lenguajes Regulares)")
            st.markdown(
                "El **lema del bombeo** establece que si un lenguaje es regular, "
                "entonces cualquier cadena suficientemente larga en ese lenguaje puede "
                "ser dividida en tres partes `x`, `y`, `z` cumpliendo ciertas condiciones, "
                "de modo que al repetir ('bombear') la parte `y`, la cadena resultante sigue en el lenguaje."
            )

            texto_para_bombeo = codigo.replace(" ", "").replace(";", "").replace("\n", "")
            bomba = Bombeo(texto_para_bombeo, 10)
            resultado = bomba.analizar()

            if isinstance(resultado, dict):
                st.markdown(f"**División:**  \n`x` = `{resultado['x']}`  \n`y` = `{resultado['y']}`  \n`z` = `{resultado['z']}`")
                st.markdown("**Cadenas bombeadas (x yⁿ z):**")
                for linea in resultado['ejemplos']:
                    st.code(linea)
                st.info(resultado['conclusion'])
            else:
                st.warning(resultado)

            # 5. Generación Musical
            st.markdown("---")
            st.header("🎼 Partitura y 🔊 Audio Generados")

            generator = MusicGenerator(tokens)
            musica_stream = generator.generar()

            with st.expander("🎼 Ver partitura (todas las páginas)"):
                try:
                    # Esto genera los PNG (puede devolver solo el primero)
                    first_png_path = musica_stream.write('lily.png')
                    # Busca todos los PNG generados en la carpeta temporal
                    base_name = os.path.splitext(first_png_path)[0]
                    png_files = sorted(glob.glob(f"{base_name}-page*.png"))
                    if not png_files:
                        # Si solo hay uno (sin -pageN), muestra ese
                        png_files = [first_png_path]
                    for png_path in png_files:
                        st.image(png_path, caption=os.path.basename(png_path), use_column_width=True)
                except Exception as e:
                    st.warning("⚠️ No se pudo generar la partitura con LilyPond.")
                    st.code(str(e))

            # Reproducir Audio MIDI
            with st.expander("🔊 Escuchar audio"):
                try:
                    mf = midi.translate.streamToMidiFile(musica_stream)

                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mid") as tmp:
                        mf.open(tmp.name, 'wb')
                        mf.write()
                        mf.close()

                        with open(tmp.name, "rb") as f:
                            st.audio(f.read(), format="audio/midi")
                except Exception as e:
                    st.warning("⚠️ No se pudo generar el audio.")
                    st.code(str(e))

        except (ValueError, ParserError, SemanticError) as e:
            st.error("❌ Error detectado:")
            st.code(str(e), language="text")

if __name__ == "__main__":
    main()
