class Sudoku:

    def __init__(self):
        self.ROWS = 9
        self.COLS = 9
        self.section_size = 3
        self.board = self.construct_board()

    def construct_board(self):
        return [[
            0
            for row in range(self.ROWS)

        ]for col in range(self.COLS)]

    def valid(self, number, row, col):
        return self._check_row(number, row, col) and self._check_col(number, row, col) and self._check_section(number, row, col)

    def _check_row(self, number, row, col):
        for num in range(self.ROWS):
            if num != col:
                if number == self.board[row][num]:
                    return False
        return True

    def _check_col(self, number, row, col):
        for num in range(self.COLS):
            if num != row:
                if number == self.board[num][col]:
                    return False
        return True

    def _check_section(self, number, row, col):
        row_index, col_index = self._get_section_indexing(row, col)
        for r in range(row_index, row_index + self.section_size):
            for c in range(col_index, col_index + self.section_size):
                if [r, c] != [row, col]:
                    if number == self.board[r][c]:
                        return False
        return True

    def _get_section_indexing(self, row, col):
        if row < self.section_size:
            row_index = 0
        elif row < 2 * self.section_size:
            row_index = 3
        else:
            row_index = 6

        if col < self.section_size:
            col_index = 0
        elif col < 2 * self.section_size:
            col_index = 3
        else:
            col_index = 6

        return row_index, col_index

    def next_tile_exists(self):
        for row in range(self.ROWS):
            for col in range(self.COLS):
                if self.board[row][col] == 0:
                    return row, col
        return False

    def fill(self):
        for row in range(self.ROWS):
            print('Feed in row: {} '.format(row))
            for col in range(self.COLS):
                string = input('Press enter to skip, or 1 - 9 for number at col: {} '.format(col))
                if string != '':
                    self.board[row][col] = int(string)
            self.print_board()

    def solve(self):

        if not self.next_tile_exists():
            return True
        else:
            row, col = self.next_tile_exists()

        for num in range(1, 10):
            if self.valid(num, row, col):
                self.board[row][col] = num

                if self.solve():
                    return True

                self.board[row][col] = 0

        return False

    def print_board(self):
        for row in self.board:
            print(row)


if __name__ == '__main__':
    sd = Sudoku()
    fill = int(input('Want to insert numbers? 1 for yes, 0 for no: '))
    if fill:
        sd.fill()
    solvable = sd.solve()
    print('Was the Sudoku solvable?', solvable)
    if solvable:
        sd.print_board()
