import tkinter as tk
from tkinter import messagebox
import random
import copy

def gerar_tabuleiro():
    board = [[0]*9 for _ in range(9)]
    _preencher(board)
    return board

def _preencher(board):
    nums = list(range(1, 10))
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                random.shuffle(nums)
                for n in nums:
                    if _valido(board, i, j, n):
                        board[i][j] = n
                        if _preencher(board):
                            return True
                        board[i][j] = 0
                return False
    return True

def _valido(board, r, c, n):
    if n in board[r]:
        return False
    if n in [board[i][c] for i in range(9)]:
        return False
    br, bc = (r // 3) * 3, (c // 3) * 3
    for i in range(br, br + 3):
        for j in range(bc, bc + 3):
            if board[i][j] == n:
                return False
    return True

def criar_puzzle():
    solucao = gerar_tabuleiro()
    puzzle = copy.deepcopy(solucao)
    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)
    for r, c in cells[:45]:
        puzzle[r][c] = 0
    return puzzle, solucao


class Sudoku:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku")
        self.root.configure(bg="white")
        self.root.resizable(False, False)

        self.puzzle  = []
        self.solucao = []
        self.usuario = []
        self.fixas   = []
        self.sel     = None

        self._build_ui()
        self.novo_jogo()

    
    
if __name__ == "__main__":
    root = tk.Tk()
    Sudoku(root)
    root.mainloop()