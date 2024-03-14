from random import sample


class Board:
    def __init__(self, amount_of_mines, width, height):
        self.amount_of_mines = amount_of_mines
        self.board_checked = []
        self.height = height
        self.width = width
        self.board = [['' for i in range(width)] for j in range(height)]
        coords = []
        for i in range(height):
            for j in range(width):
                coords.append((i, j))
        self.mine_coordinates = sample(coords, amount_of_mines)
        for coords in self.mine_coordinates:
            y, x = coords
            self.board[y][x] = f"yes no 100 no"
        for i in range(height):
            for j in range(width):
                if not self.board[i][j]:
                    amount_of_mines_near = self.count_near(i, j)
                    self.board[i][j] = f"no no {amount_of_mines_near} no"

    def count_near(self, y, x):
        n = 0
        for y_i in range(y - 1, y + 2):
            for x_i in range(x - 1, x + 2):
                if (0 <= y_i <= self.height - 1 and 0 <= x_i <= self.width - 1 and
                        self.board[y_i][x_i] and self.board[y_i][x_i].split()[0] == 'yes'):
                    n += 1
        return n

    def recurs_zeros(self, y, x):
        count = self.count_near(y, x)
        if count == 0 and 0 <= y <= self.height - 1 and 0 <= x <= self.width - 1 and not self.board_checked[y][x]:
            self.board[y][x] = f"no yes {count} no"
            self.board_checked[y][x] = True
            for y_i in range(y - 1, y + 2):
                for x_i in range(x - 1, x + 2):
                    if y_i != y or x_i != x:
                        self.recurs_zeros(y_i, x_i)
        elif count != 0 and 0 <= y <= self.height - 1 and 0 <= x <= self.width - 1:
            self.board[y][x] = f"no yes {count} no"

    def check(self):
        board_with_every = []
        board_with_opened = []
        for i in self.board:
            board_with_every.extend(i)
            board_with_opened.extend(list(filter(lambda x: x.split()[1] == 'yes', i)))
        return len(board_with_every) - len(board_with_opened) == self.amount_of_mines


def get_width():
    print('Введите ширину поля')
    width = input()
    while True:
        try:
            width_check = float(width)
            width = int(width)
            if width <= 0 or width != width_check:
                raise AssertionError
            return width
        except ValueError:
            print('неправильный тип числа')
            width = input()
        except AssertionError:
            print('Неправильное число, введите повторно')
            width = input()


def get_height():
    print('Введите длину поля')
    height = input()
    while True:
        try:
            height_check = float(height)
            height = int(height)
            if height <= 0 or height_check != height:
                raise AssertionError
            return height
        except ValueError:
            print('неправильный тип числа')
            height = input()
        except AssertionError:
            print('Неправильное число, введите повторно')
            height = input()


def get_amount_of_mines(width, height):
    print('Введите количество мин')
    amount_of_mines = input()
    while True:
        try:
            amount_of_mines_check = float(amount_of_mines)
            amount_of_mines = int(amount_of_mines)
            if width * height <= amount_of_mines:
                print('Количество мин меньше или равно размеру поля')
            if amount_of_mines <= 0 or amount_of_mines != amount_of_mines_check or width * height <= amount_of_mines:
                raise AssertionError
            return amount_of_mines
        except ValueError:
            print('неправильный тип числа')
            amount_of_mines = input()
        except AssertionError:
            print('Неправильное число, введите повторно')
            amount_of_mines = input()


def print_command():
    print('Синтаксис команд для игры:')
    print('Счёт номеров строки и столбцов начинается с крайней левой верхней клетки')
    print('<номер строки(счет начинается с 1)> <номер столбца(счет начинается с 1)> <команда действия>')
    print("Команды действия:")
    print('флажок - устанавливает флаг')
    print('открыть - открывает ячейку')
    print('снять_флажок - снимает флажок')
    print('Синтаксис команд для управления игрой:')
    print('<команда>')
    print('начать_заново - начинает игру заново обновляя размер поля и количество мин')
    print('закончить - заканчивает ход программы')
    print('поменять_количество_мин - меняет количество мин не меняя размер поля, игра начинается заново')
    print('поменять_ширину - меняет ширину не меняя высоту и количество мин, игра начинается заново')
    print('поменять_высоту - меняет высоту не меняя ширину и количество мин, игра начинается заново')
    print('Синтаксис поля:')
    print('[ ] - ячейка еще не открыта')
    print('[F] - стоит флажок')
    print('[<номер>] - открытая ячейка, с номером количества взрывчаток вблизи')
    print('--------------------------------------------------------------------------------------------')


def print_board(board):
    for i in range(len(board)):
        print_line = []
        for j in range(len(board[0])):
            a = board[i][j].split()
            if a[3] == 'yes':
                print_line.append('[F]')
                continue
            active, opened, number, flag = a
            if opened == 'yes':
                if int(number) == 0:
                    print_line.append('[0]')
                elif int(number) == 100:
                    print_line.append(f"[B]")
                else:
                    print_line.append(f"[{number}]")
            else:
                print_line.append('[ ]')
        print(' '.join(print_line))


def open_board(board):
    for y in range(len(board)):
        for x in range(len(board[0])):
            active, opened, number, flag = board[y][x].split()
            board[y][x] = f"{active} yes {number} no"
    return board


print_command()
width, height = get_width(), get_height()
amount_of_mines = get_amount_of_mines(width, height)
board = Board(amount_of_mines, width, height)
print_board(board.board)
is_active = True
while True:
    input_user = input()
    try:
        if len(input_user.split()) == 1:
            type_of_move = input_user
            if type_of_move.lower() == 'начать_заново':
                width, height = get_width(), get_height()
                amount_of_mines = get_amount_of_mines(width, height)
                board = Board(amount_of_mines, width, height)
                print_board(board.board)
                is_active = True
            elif type_of_move.lower() == 'команды':
                print_command()
            elif type_of_move.lower() == 'закончить':
                print('игра закончена')
                break
            elif type_of_move.lower() == 'поменять_количество_мин':
                amount_of_mines = get_amount_of_mines(width, height)
                board = Board(amount_of_mines, width, height)
                print_board(board.board)
            elif type_of_move.lower() == 'поменять_ширину':
                width = get_width()
                while True:
                    if width * height <= amount_of_mines:
                        print('Слишком маленькая ширина')
                        width = get_width()
                    else:
                        break
                board = Board(amount_of_mines, width, height)
                print_board(board.board)
            elif type_of_move.lower() == 'поменять_высоту':
                height = get_height()
                while True:
                    if width * height <= amount_of_mines:
                        print('Слишком маленькая высота')
                        height = get_height()
                    else:
                        break
                board = Board(amount_of_mines, width, height)
                print_board(board.board)
            else:
                raise AssertionError
        elif is_active and len(input_user.split()) == 3:
            line, column, type_of_move = input_user.split()
            line = int(line) - 1
            column = int(column) - 1
            if board.board[line][column].split()[1] == 'yes':
                print('ячейка уже открыта')
                continue
            if type_of_move.lower() == 'флажок':
                state = board.board[line][column].split()
                board.board[line][column] = f'{state[0]} {state[1]} {state[2]} yes'
                print_board(board.board)
            elif type_of_move.lower() == 'снять_флажок':
                state = board.board[line][column].split()
                board.board[line][column] = f'{state[0]} {state[1]} {state[2]} no'
                print_board(board.board)
            elif type_of_move.lower() == 'открыть':
                state = board.board[line][column].split()
                if state[3] == 'yes':
                    print('стоит флажок, чтобы открыть ячейку, нужно его снять')
                elif state[0] == 'yes':
                    print('Вы проиграли, начните игру заново')
                    board.board = open_board(board.board)
                    print_board(board.board)
                    is_active = False
                elif state[2] == '0':
                    board.board[line][column] = f"no yes 0 {state[3]}"
                    board.board_checked = [[False for j in range(board.width)] for i in range(board.height)]
                    board.recurs_zeros(line, column)
                    if board.check():
                        print('Вы выиграли, начните игру заново (команда - начать_заново)')
                        board.board = open_board(board.board)
                        is_active = False
                    print_board(board.board)
                else:
                    board.board[line][column] = f"no yes {state[2]} {state[3]}"
                    if board.check():
                        print('Вы выиграли, начните игру заново (команда - начать_заново)')
                        board.board = open_board(board.board)
                        is_active = False
                    print_board(board.board)
        elif not is_active:
            print('начните игру заново (команда - начать_заново)')
            continue
        elif not input_user:
            raise ValueError
        elif len(input_user) > 3:
            raise AssertionError
    except ValueError:
        if not input_user:
            print('чтобы программа работала, нужно что-то ввести')
        elif ((isinstance(line, tuple) or isinstance(column, tuple) or isinstance(line, str) or isinstance(column, str))
              and isinstance(type_of_move, str)):
            print('число строки/столбца должно быть типа int')
    except AssertionError:
        print('команда не распознана, введите заново')
