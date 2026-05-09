import tkinter as tk
from tkinter import messagebox
from sudoku import SudokuBoard

CELL = 54
GRID = CELL * 9

# mudar as cores na aula de sexta
C_CELL_NORMAL = "white"
C_CELL_SEL    = "#c8c8c8"
C_CELL_PEER   = "#e8e8e8"
C_CELL_SAME   = "#d0d0ff"
C_NUM_FIXED   = "black"
C_NUM_USER    = "#1a1aaa"
C_NUM_ERROR   = "#ff0000"


class Sudoku:
    def __init__(self, root):
        self.root = root
        self.root.title("Super Sudoku do Jao e Gui")
        self.root.configure(bg="white")
        self.root.resizable(False, False)

        # matrizes
        self.puzzle   = []
        self.solucao  = []
        self.usuario  = []
        self.fixas    = []

# matriz de notas (candidatos) coloquei isso hoje
        self.notas = []
        for i in range(9):
            linha = []
            for j in range(9):
                linha.append([])
            self.notas.append(linha)

        self.sel       = None
        self.erros     = 0
        self.modo_nota = False
        self.segundos  = 0
        self._timer_id = None

        self._build_ui()
        self.novo_jogo()

    def _build_ui(self):
        tk.Label(self.root, text="Super Sudoku do Jao e Gui",
                 font=("Arial", 16), bg="white", fg="black").pack(pady=(12, 2))

        info_frame = tk.Frame(self.root, bg="white")
        info_frame.pack(pady=(2, 4))

        self.lbl_erros = tk.Label(info_frame, text="Erros: 0",
                                  font=("Arial", 10), bg="white", fg="red")
        self.lbl_erros.pack(side="left", padx=16)

        self.lbl_timer = tk.Label(info_frame, text="00:00",
                                  font=("Arial", 10), bg="white", fg="black")
        self.lbl_timer.pack(side="left", padx=16)

        self.canvas = tk.Canvas(self.root, width=GRID, height=GRID,
                                bg="white", highlightthickness=1,
                                highlightbackground="black")
        self.canvas.pack(padx=16, pady=4)
        self.canvas.bind("<Button-1>", self._click)
        self.root.bind("<Key>", self._tecla)

        btn_frame = tk.Frame(self.root, bg="white")
        btn_frame.pack(pady=6)

        tk.Button(btn_frame, text="Novo Jogo", font=("Arial", 10),
                  bg="#dddddd", fg="black", relief="flat",
                  padx=10, pady=4, command=self.novo_jogo).pack(side="left", padx=6)

        tk.Button(btn_frame, text="Apagar", font=("Arial", 10),
                  bg="#dddddd", fg="black", relief="flat",
                  padx=10, pady=4, command=self._apagar).pack(side="left", padx=6)

        tk.Button(btn_frame, text="Resolver", font=("Arial", 10),
                  bg="#dddddd", fg="black", relief="flat",
                  padx=10, pady=4, command=self._resolver).pack(side="left", padx=6)

    def _iniciar_timer(self):
        if self._timer_id:
            self.root.after_cancel(self._timer_id)
        self.segundos = 0
        self._tick()

    def _tick(self):
        minutos = self.segundos // 60
        segs    = self.segundos % 60
        self.lbl_timer.config(text=f"{minutos:02d}:{segs:02d}")
        self.segundos += 1
        self._timer_id = self.root.after(1000, self._tick)

    def _parar_timer(self):
        if self._timer_id:
            self.root.after_cancel(self._timer_id)
            self._timer_id = None

    def novo_jogo(self):
        board = SudokuBoard()
        board.generate_full_board()
        self.puzzle, self.solucao = board.create_puzzle()

        self.usuario = []
        for r in range(9):
            linha = []
            for c in range(9):
                linha.append(self.puzzle[r][c])
            self.usuario.append(linha)

        self.fixas = []
        for r in range(9):
            linha = []
            for c in range(9):
                if self.puzzle[r][c] != 0:
                    linha.append(True)
                else:
                    linha.append(False)
            self.fixas.append(linha)

        self.sel       = None
        self.erros     = 0
        self.lbl_erros.config(text="Erros: 0")
        self._iniciar_timer()
        self._desenhar()

    def _click(self, event):
        c = event.x // CELL
        r = event.y // CELL
        if r >= 0 and r < 9 and c >= 0 and c < 9:
            self.sel = (r, c)
            self._desenhar()

    def _tecla(self, event):
        if event.keysym == "Delete" or event.keysym == "BackSpace":
            self._apagar()
            return

        if event.char.isdigit() and event.char != "0":
            self._inserir(int(event.char))
            return

        if self.sel is None:
            self.sel = (0, 0)

        r, c = self.sel

        if event.keysym == "Up":
            r = r - 1
        elif event.keysym == "Down":
            r = r + 1
        elif event.keysym == "Left":
            c = c - 1
        elif event.keysym == "Right":
            c = c + 1

        if r < 0:
            r = 0
        if r > 8:
            r = 8
        if c < 0:
            c = 0
        if c > 8:
            c = 8

        self.sel = (r, c)
        self._desenhar()

    def _inserir(self, valor):
        if self.sel is None:
            return

        r, c = self.sel

        if self.fixas[r][c]:
            return

        self.usuario[r][c] = valor
        self.notas[r][c] = []
        self._limpar_notas_pares(r, c, valor)

        if valor != self.solucao[r][c]:
            self.erros += 1
            self.lbl_erros.config(text=f"Erros: {self.erros}")
            self._desenhar()
            if self.erros >= 5:
                self._parar_timer()
                messagebox.showerror("Fim de jogo",
                    "Você errou mais de 5 vezes! Comece um novo jogo.")
                self.novo_jogo()
            return

        self._desenhar()
        if self._vitoria():
            self._parar_timer()
            minutos = (self.segundos - 1) // 60
            segs    = (self.segundos - 1) % 60
            messagebox.showinfo("Parabéns!",
                f"Você completou o Sudoku!\nTempo: {minutos:02d}:{segs:02d}")

    def _limpar_notas_pares(self, row, col, val):
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3

        for i in range(9):
            # Linha
            if val in self.notas[row][i]:
                self.notas[row][i].remove(val)
            # Coluna
            if val in self.notas[i][col]:
                self.notas[i][col].remove(val)

        # Box 3x3
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if val in self.notas[i][j]:
                    self.notas[i][j].remove(val)

    def _apagar(self):
        if self.sel is None:
            return
        r, c = self.sel
        if not self.fixas[r][c]:
            self.usuario[r][c] = 0
            self.notas[r][c] = []
            self._desenhar()

    def _resolver(self):
        self._parar_timer()
        for r in range(9):
            for c in range(9):
                self.usuario[r][c] = self.solucao[r][c]
                self.notas[r][c] = []
        self._desenhar()

    def _vitoria(self):
        for r in range(9):
            for c in range(9):
                if self.usuario[r][c] != self.solucao[r][c]:
                    return False
        return True

    def _pares(self, sr, sc): 
        pares = []
        box_row = (sr // 3) * 3
        box_col = (sc // 3) * 3

        for i in range(9):
            if (sr, i) not in pares and (sr, i) != (sr, sc):
                pares.append((sr, i))
            if (i, sc) not in pares and (i, sc) != (sr, sc):
                pares.append((i, sc))

        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if (i, j) not in pares and (i, j) != (sr, sc):
                    pares.append((i, j))

        return pares

    def _desenhar(self):
        self.canvas.delete("all")

        if self.sel:
            sr, sc = self.sel
        else:
            sr, sc = -1, -1

        num_sel = 0
        if self.sel:
            num_sel = self.usuario[sr][sc]

        if self.sel:
            pares = self._pares(sr, sc)
        else:
            pares = []

        for r in range(9):
            for c in range(9):
                x1 = c * CELL
                y1 = r * CELL
                x2 = x1 + CELL
                y2 = y1 + CELL

                val = self.usuario[r][c]

                if r == sr and c == sc:
                    bg = C_CELL_SEL
                elif num_sel != 0 and val == num_sel:
                    bg = C_CELL_SAME
                elif (r, c) in pares:
                    bg = C_CELL_PEER
                else:
                    bg = C_CELL_NORMAL

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=bg, outline="")

                if val != 0:
                    errado = False
                    if not self.fixas[r][c] and val != self.solucao[r][c]:
                        errado = True
                    if errado:
                        cor = C_NUM_ERROR
                    elif self.fixas[r][c]:
                        cor = C_NUM_FIXED
                    else:
                        cor = C_NUM_USER
                    if self.fixas[r][c]:
                        peso = "bold"
                    else:
                        peso = "normal"

                    self.canvas.create_text(x1 + CELL // 2, y1 + CELL // 2,
                                            text=str(val),
                                            font=("Arial", 16, peso),
                                            fill=cor)
                elif len(self.notas[r][c]) > 0:
                    self._desenhar_notas(x1, y1, self.notas[r][c])

        for i in range(10):
            if i % 3 == 0:
                espessura = 2
            else:
                espessura = 1

            self.canvas.create_line(i * CELL, 0, i * CELL, GRID,
                                    fill="black", width=espessura)
            self.canvas.create_line(0, i * CELL, GRID, i * CELL,
                                    fill="black", width=espessura)

    def _desenhar_notas(self, x1, y1, notas):
        sz = CELL // 3
        for n in notas:
            nr = (n - 1) // 3
            nc = (n - 1) % 3
            cx = x1 + nc * sz + sz // 2
            cy = y1 + nr * sz + sz // 2
            self.canvas.create_text(cx, cy, text=str(n),
                                    font=("Arial", 7), fill=C_NOTE)


if __name__ == "__main__":
    root = tk.Tk()
    Sudoku(root)
    root.mainloop()