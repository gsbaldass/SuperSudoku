import random
import copy

class SudokuBoard:
    def __init__(self, board=None):
        if board is None:
            self.board = [[0] * 9 for _ in range(9)]
        else:
            self.board = copy.deepcopy(board)

    def eh_valido(self, row, col, num):
        if self.board[row][col] != 0:
            return False
        if num in self.board[row]:
            return False
        if any(self.board[i][col] == num for i in range(9)):
            return False
        box_row, box_col = (row // 3) * 3, (col // 3) * 3
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if self.board[i][j] == num:
                    return False
        return True

    def resolver(self):
        vazio = self.encontrar_vazio()
        if not vazio:
            return True
        row, col = vazio
        nums = list(range(1, 10))
        random.shuffle(nums)
        for num in nums:
            if self.eh_valido(row, col, num):
                self.board[row][col] = num
                if self.resolver():
                    return True
                self.board[row][col] = 0
        return False

    def encontrar_vazio(self):
        """Find an empty cell (0)."""
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return i, j
        return None

    def gerar_tabuleiro_completo(self):
        self.board = [[0] * 9 for _ in range(9)]
        self.resolver()
        return self.board

    def criar_quebra_cabeca(self, remocoes=45):
        solution = SudokuBoard(self.board)
        cells = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(cells)
        for r, c in cells[:remocoes]:
            self.board[r][c] = 0
        return self.board, solution.board

    def esta_completo(self):
        return all(cell != 0 for row in self.board for cell in row)

    def esta_resolvido(self, tabuleiro_solucao):
        if isinstance(tabuleiro_solucao, SudokuBoard):
            return self.board == tabuleiro_solucao.board
        return self.board == tabuleiro_solucao

    def obter_tabuleiro(self):
        return copy.deepcopy(self.board)

    def definir_celula(self, row, col, num):
        if 0 <= row < 9 and 0 <= col < 9:
            self.board[row][col] = num

    def obter_celula(self, row, col):
        if 0 <= row < 9 and 0 <= col < 9:
            return self.board[row][col]
        return None