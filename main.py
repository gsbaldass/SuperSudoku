#o jogo ta funcionando mas quando voce seleciona uma coluna e coloca um numero vc tem que ir pra outra coluna pra conseguir ver ele, boa sorte arrumando

import tkinter as tk
from tkinter import messagebox #mostra as mensagens de erro e vitória
import random #embaralha os numeros pra sempre ter um jogo diferente
import copy
from sudoku import SudokuBoard 

class Sudoku:
    def __init__(self, root):
        self.root = root 
        self.root.title("Super Sudoku do Jao e Gui")
        self.root.configure(bg="white")
        self.root.resizable(False, False)
        self.puzzle  = []
        self.solucao = []
        self.usuario = []
        self.fixas   = []
        self.sel     = None
        self.erros = 0
        self._build_ui()
        self.novo_jogo()
    def __init__(self, root):
        self.root = root 
        self.root.title("Super Sudoku do Jao e Gui")
        self.root.configure(bg="white")
        self.root.resizable(False, False)
        self.puzzle  = []
        self.solucao = []
        self.usuario = []
        self.fixas   = []
        self.sel     = None
        self.erros = 0
        self._build_ui()
        self.novo_jogo()

    def _build_ui(self):
        tk.Label(self.root, text="Super Sudoku do Jao e Gui", font=("Arial", 16),
                 bg="white", fg="black").pack(pady=(12, 6))
        self.label_erros = tk.Label(self.root, text=f"Erros: {self.erros}", font=("Arial", 10),
                 bg="white", fg="red").pack(pady=(0, 12))

        self.canvas = tk.Canvas(self.root, width=9*54, height=9*54,
                                bg="white", highlightthickness=1,
                                highlightbackground="black")
        self.canvas.pack(padx=16, pady=4)
        self.canvas.bind("<Button-1>", self._click)
        self.root.bind("<Key>", self._tecla)

        btn_frame = tk.Frame(self.root, bg="white")
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Novo Jogo", font=("Arial", 10),
                  bg="#dddddd", fg="black", relief="flat", padx=10, pady=4,
                  command=self.novo_jogo).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Apagar", font=("Arial", 10),
                  bg="#dddddd", fg="black", relief="flat", padx=10, pady=4,
                  command=self._apagar).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Resolver", font=("Arial", 10),
                  bg="#dddddd", fg="black", relief="flat", padx=10, pady=4,
                  command=self._resolver).pack(side="left", padx=6)

    def novo_jogo(self):
        board = SudokuBoard()
        board.generate_full_board()
        self.puzzle, self.solucao = board.create_puzzle()
        self.usuario = copy.deepcopy(self.puzzle)
        self.fixas   = [[self.puzzle[r][c] != 0 for c in range(9)] for r in range(9)]
        self.sel     = None
        self.erros = 0
        self._desenhar()

    def _click(self, event): #comando que permite usar o mouse pra clicar na tela btw o copiloto me ajudou a cozinhar
        c = event.x // 54
        r = event.y // 54
        if 0 <= r < 9 and 0 <= c < 9:
            self.sel = (r, c)
            self._desenhar()

    def _tecla(self, event): #comando que permite usar o teclado pra interagir com o jogo
        if event.keysym in ("Delete", "BackSpace"):
            self._apagar()
            return
        if event.char.isdigit() and event.char != "0":
            self._inserir(int(event.char))
            return
        if self.sel is None:
            self.sel = (0, 0)
        r, c = self.sel
        moves = {"Up": (-1, 0), "Down": (1, 0), "Left": (0, -1), "Right": (0, 1)}
        if event.keysym in moves:
            dr, dc = moves[event.keysym]
            self.sel = (max(0, min(8, r+dr)), max(0, min(8, c+dc)))
            self._desenhar()     

    def _inserir(self, valor):
        if self.sel is None:
            return
        r, c = self.sel
        if self.fixas[r][c]:
            return
        self.usuario[r][c] = valor
        if valor != self.solucao[r][c]:
            self.erros += 1
            self._desenhar()
            self.root.update()  # Force update to show the number
            if self.erros >= 5:
                messagebox.showerror("Fim de jogo", "Você errou mais de 5 vezes! Comece um novo jogo.")
                self.novo_jogo()
            else:
                self.label_erros.config(text=f"Erros: {self.erros}")
            return
        self._desenhar()
        self.root.update()  # Force update
        if self._vitoria():
            messagebox.showinfo("Parabéns!", "Você completou o Sudoku!")

    def _apagar(self):
        if self.sel is None:
            return
        r, c = self.sel
        if not self.fixas[r][c]:
            self.usuario[r][c] = 0
            self._desenhar()
            self.root.update()
    
    def _resolver(self): # resolve todo o sudoku
        self.usuario = self.solucao
        self._desenhar()

    def _vitoria(self):
        for r in range(9):
            for c in range(9):
                if self.usuario[r][c] != self.solucao[r][c]:
                    return False
        return True

    def _desenhar(self):
        self.canvas.delete("all")
        CELL = 54
        sr, sc = self.sel if self.sel else (-1, -1)

        for r in range(9):
            for c in range(9):
                x1, y1 = c * CELL, r * CELL
                x2, y2 = x1 + CELL, y1 + CELL

                bg = "#c8c8c8" if (r == sr and c == sc) else "white"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=bg, outline="")

                val = self.usuario[r][c]
                if val != 0:
                    errado = (not self.fixas[r][c] and val != self.solucao[r][c])
                    cor    = "#ff0000" if errado else "black"
                    peso   = "bold" if self.fixas[r][c] else "normal"
                    self.canvas.create_text(x1 + CELL//2, y1 + CELL//2,
                                            text=str(val),
                                            font=("Arial", 16, peso),
                                            fill=cor)

        for i in range(10):
            espessura = 2 if i % 3 == 0 else 1
            self.canvas.create_line(i*CELL, 0, i*CELL, 9*CELL,
                                    fill="black", width=espessura)
            self.canvas.create_line(0, i*CELL, 9*CELL, i*CELL,
                                    fill="black", width=espessura)


if __name__ == "__main__":
    root = tk.Tk()
    Sudoku(root)
    root.mainloop()