import random
import copy

class SudokuBoard:
    def __init__(self, board=None):
        if board is None:
            self.board = []
            for i in range(9):
                linha = []
                for j in range(9):
                    linha.append(0)
                self.board.append(linha)
        else:
            self.board = copy.deepcopy(board)

    def eh_valido(self, row, col, num):
        # Célula já preenchida
        if self.board[row][col] != 0:
            return False

        # Verifica a linha
        for c in range(9):
            if self.board[row][c] == num:
                return False

        # Verifica a coluna
        for r in range(9):
            if self.board[r][col] == num:
                return False

        # Verifica o box 3x3
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if self.board[i][j] == num:
                    return False

        return True

    def encontrar_vazio(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return i, j
        return None

    def resolver(self):
        vazio = self.encontrar_vazio()
        if not vazio:
            return True

        row, col = vazio
        nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        random.shuffle(nums)

        for num in nums:
            if self.eh_valido(row, col, num):
                self.board[row][col] = num
                if self.resolver():
                    return True
                self.board[row][col] = 0

        return False

    def generate_full_board(self):
        # Zera o tabuleiro
        for i in range(9):
            for j in range(9):
                self.board[i][j] = 0
        self.resolver()
        return self.board

    def create_puzzle(self, remocoes=45):
        # Salva a solução antes de remover
        solucao = []
        for i in range(9):
            linha = []
            for j in range(9):
                linha.append(self.board[i][j])
            solucao.append(linha)

        # Cria lista de todas as posições e embaralha
        celulas = []
        for r in range(9):
            for c in range(9):
                celulas.append((r, c))
        random.shuffle(celulas)

        # Remove células para criar o puzzle
        for idx in range(remocoes):
            r, c = celulas[idx]
            self.board[r][c] = 0

        return self.board, solucao