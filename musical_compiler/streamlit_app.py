# app.py
import streamlit as st
from lexer import Lexer
from parser import Parser  # Asegúrate de tener este módulo creado

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
            tokens = lexer.analizar(codigo)
            st.success("✅ Análisis léxico completado con éxito")

            st.markdown("### Tokens reconocidos:")
            for token in tokens:
                st.code(str(token), language="text")

            # Solo si el léxico fue exitoso, pasamos al parser
            try:
                parser = Parser(tokens)
                parser.parse()
                st.success("✅ Análisis sintáctico completado con éxito")
            except Exception as e:
                st.error("❌ Error sintáctico detectado:")
                st.code(str(e), language="text")

        except ValueError as e:
            st.error("❌ Error léxico detectado:")
            st.code(str(e), language="text")

if __name__ == "__main__":
    main()
