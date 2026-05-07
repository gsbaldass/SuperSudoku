import random
import copy

class SudokuBoard:
    def __init__(self, board=None):
        if board is None:
            self.board = [[0] * 9 for _ in range(9)]
        else:
            self.board = copy.deepcopy(board)

    def is_valid(self, row, col, num):
        if num in self.board[row]:
            return False
        if num in [self.board[i][col] for i in range(9)]:
            return False
        box_row, box_col = (row // 3) * 3, (col // 3) * 3
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if self.board[i][j] == num:
                    return False
        return True

    def solve(self):
        empty = self.find_empty()
        if not empty:
            return True
        row, col = empty
        nums = list(range(1, 10))
        random.shuffle(nums)
        for num in nums:
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.solve():
                    return True
                self.board[row][col] = 0
        return False

    def find_empty(self):
        """Find an empty cell (0)."""
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return (i, j)
        return None

    def generate_full_board(self):
        self.board = [[0] * 9 for _ in range(9)]
        self.solve()
        return self.board

    def create_puzzle(self, removals=45):
        solution = SudokuBoard(self.board)
        cells = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(cells)
        for r, c in cells[:removals]:
            self.board[r][c] = 0
        return self.board, solution.board

    def is_complete(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return False
        return True

    def get_board(self):
        return copy.deepcopy(self.board)

    def set_cell(self, row, col, num):
        if 0 <= row < 9 and 0 <= col < 9:
            self.board[row][col] = num

    def get_cell(self, row, col):
        if 0 <= row < 9 and 0 <= col < 9:
            return self.board[row][col]
        return None