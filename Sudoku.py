from random import choice, randint
from copy import deepcopy


class sudoku():
    def __init__(self):
        self.sudoku = []
        self.rows = []  # 每行已用的数字，从上到下
        self.columns = []  # 每列已用的数字，从左到右
        self.squares = []  # 每个3*3块已用的数字，按行遍历

        self.solution_set = []

    def init_sudoku(self):
        self.sudoku = []
        self.rows = []
        self.columns = []
        self.squares = []

        row = []
        for j in range(0, 9):
            '''
            [0] : 数字
            [1] : 1 表示题目提供， 0 表示题目未提供
            [2] : [0(row), 0(column), 0(square)] 表示不违反数独规则， [-1, -1, -1] 表示违反
            [3] : 当前单元与那些单元冲突，以坐标元组形式存储在列表中
            '''
            row.append([0, 1, [0, 0, 0], []])
            self.columns.append([])
        for i in range(0, 9):
            self.sudoku.append(deepcopy(row))
            self.rows.append([])
        for i in range(0, 3):
            squares_row = []
            for j in range(0, 3):
                squares_row.append([])
            self.squares.append(deepcopy(squares_row))

    def is_valid(self, i, j, number):
        if number in self.rows[i] or number in self.columns[j] or number in self.squares[i // 3][j // 3]:
            return False
        return True

    def unchoose_number(self, sudoku_copy, i, j, number):
        sudoku_copy[i][j][0] = 0
        self.rows[i].remove(number)
        self.columns[j].remove(number)
        self.squares[i // 3][j // 3].remove(number)

    def choose_number(self, sudoku_copy, i, j, number):
        sudoku_copy[i][j][0] = number
        self.rows[i].append(number)
        self.columns[j].append(number)
        self.squares[i // 3][j // 3].append(number)

    def generate_sudoku(self, given):

        def dfs(i, j):  # 回溯生成终盘
            if i > 8:
                return 1

            next_i = i
            next_j = j + 1
            if next_j > 8:
                next_i += 1
                next_j = 0

            numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]

            while len(numbers) != 0:
                number = choice(numbers)
                numbers.remove(number)

                if self.is_valid(i, j, number):
                    self.choose_number(self.sudoku, i, j, number)
                    if dfs(next_i, next_j):
                        return 1
                    self.unchoose_number(self.sudoku, i, j, number)

        while True:
            self.init_sudoku()
            dfs(0, 0)

            space = 81 - given  # 根据玩家选择挖空
            while space != 0:
                r = randint(0, 8)
                c = randint(0, 8)
                if self.sudoku[r][c][1] == 0:
                    continue
                self.unchoose_number(self.sudoku, r, c, self.sudoku[r][c][0])
                self.sudoku[r][c][1] = 0  # 表示空格
                space -= 1

            for a in self.sudoku:
                print(a)
            self.solve_sudoku()
            print(len(self.solution_set))
            if len(self.solution_set) == 1:
                break
        return self.sudoku

    def solve_sudoku(self):
        solution = deepcopy(self.sudoku)

        def dfs(i, j):  # 回溯解出数独
            if i > 8:
                self.solution_set.append(deepcopy(solution))
                return

            next_i = i
            next_j = j + 1
            if next_j > 8:
                next_i += 1
                next_j = 0

            if solution[i][j][0] == 0:
                for number in range(1, 10):
                    if self.is_valid(i, j, number):
                        self.choose_number(solution, i, j, number)
                        dfs(next_i, next_j)
                        self.unchoose_number(solution, i, j, number)
            else:
                dfs(next_i, next_j)

        self.solution_set.clear()
        dfs(0, 0)

    def check_sudoku(self, i, j, number):
        cell = [[], [], [], [], [], [], [], [], []]
        rows = []
        columns = []
        squares = [[], [], []]

        for row in range(0, 9):
            rows.append(deepcopy(cell))

        for column in range(0, 9):
            columns.append(deepcopy(cell))

        for square_row in range(0, 3):
            for square in range(0, 3):
                squares[square_row].append(deepcopy(cell))

        for row in range(0, 9):
            for column in range(0, 9):
                num = self.sudoku[row][column][0]
                if num == 0:
                    continue
                rows[row][num - 1].append((row, column))
                columns[column][num - 1].append((row, column))
                squares[row // 3][column // 3][num - 1].append((row, column))

        for row in rows:
            for num in row:
                length = len(num)
                for position in num:
                    if length <= 1:
                        self.sudoku[position[0]][position[1]][2][0] = 0
                    else:
                        self.sudoku[position[0]][position[1]][2][0] = -1

        for column in columns:
            for num in column:
                length = len(num)
                for position in num:
                    if length <= 1:
                        self.sudoku[position[0]][position[1]][2][1] = 0
                    else:
                        self.sudoku[position[0]][position[1]][2][1] = -1

        for square_rows in squares:
            for square in square_rows:
                for num in square:
                    length = len(num)
                    for position in num:
                        if length <= 1:
                            self.sudoku[position[0]][position[1]][2][2] = 0
                        else:
                            self.sudoku[position[0]][position[1]][2][2] = -1

    def correct(self):

        def is_the_same_with(solution):
            for i in range(0, 9):
                for j in range(0, 9):
                    if solution[i][j][0] != self.sudoku[i][j][0]:
                        return False
            return True

        for solution in self.solution_set:
            if is_the_same_with(solution):
                return True
