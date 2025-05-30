# gui/interface.py
import tkinter as tk
from lexer import Lexer

class CompilerGUI:
    def __init__(self):
        self.lexer = Lexer()
        self.root = tk.Tk()
        self.root.title("Compilador Musical")
        self._build_ui()

    def _build_ui(self):
        self.text = tk.Text(self.root, height=15, width=50)
        self.text.pack()

        self.result = tk.Text(self.root, height=10, width=50, bg="#f0f0f0")
        self.result.pack()

        btn = tk.Button(self.root, text="Analizar", command=self.analizar)
        btn.pack()

    def analizar(self):
        entrada = self.text.get("1.0", tk.END)
        tokens = self.lexer.analizar(entrada)
        self.result.delete("1.0", tk.END)
        for token in tokens:
            self.result.insert(tk.END, f"{token}\n")

    def ejecutar(self):
        self.root.mainloop()
