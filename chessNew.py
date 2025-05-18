# -*- coding: utf-8 -*-
"""
    Считываем файл с данными в формате: N L K V, где N - размерность поля, L - количество фигур, которые нужно поставить на доску(так как у нас две фигуры, то это число отражает выборку фигур с повторениями)
    K - уже существующие кони, V - уже существующие визири.
    Записываем в новый файл все возможнные позиции фигур не под боем
"""
from itertools import combinations_with_replacement 
def add_piece(x,y,piece_type,table,n):
    table[y][x] = piece_type
    mark_position(x,y,piece_type,table,n)
def remove_piece(x,y,piece_type,table,n):
    table[y][x] = '0'
    unmark_position(x,y,piece_type,table,n)
    
def mark_position(x,y, piece_type,table,n):
    """
    Функция создания на матрице позиций под боем

    """   
    piece_moves = {
        # конь
        "k":[(-2, -1), (-2, 1), (2, -1), (2, 1),
        (-1, -2), (-1, 2), (1, -2), (1, 2)],
        # виверь
        "v":[(-1, 0), (1, 0),
        (0, -1), (0, 1)]
    }
    for dx,dy in piece_moves[piece_type]:
        nx,ny = x + dx, y + dy
        if 0 <= x + dx < n and 0 <= y + dy < n: 
            if table[ny][nx] == '0':  # Помечаем только свободные клетки
                table[ny][nx] = '*'

def unmark_position(x,y, piece_type,table,n):
    """
    Функция удаления на матрице позиций под боем

    """   
    piece_moves = {
        # конь
        "k":[(-2, -1), (-2, 1), (2, -1), (2, 1),
        (-1, -2), (-1, 2), (1, -2), (1, 2)],
        # виверь
        "v":[(-2, 0), (-1, 0), (2, 0), (1, 0),
        (0, -2), (0, 2), (0, -1), (0, 1)]
    }
    for dx,dy in piece_moves[piece_type]:
        nx,ny = x + dx, y + dy
        if 0 <= x + dx < n and 0 <= y + dy < n: table[ny][nx] = '0'
def read_input(file_path:str) -> list:
    """
    Функция чтения и обработки данных из файла input.txt 
    
    :param 
    file_path(str): Входное значение с адрессом входного файла

    :return 
    (list): Возвращает такие переменные, как:
        n(int): Размерность поля
        l(int): Количество размещаемых фигур
        k(int): Количество уже размещенных фигур
        existing_piece(list): Список координат всех существующих фигур с названием фигуры
        permut_piece(list): Список всех сочетаний из L фигур, таких как конь и визирь
    """   
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
        n, l, k, v = map(int, lines[0].strip().split())
        table = [["0"]*n for _ in range(n)]
        existing_piece = [list(map(int,line.strip().split())) for line in lines[1:] if line.strip().split()]
        permut_piece = list(combinations_with_replacement('kv', l))
        for i in range(k+v):
            if i < k: existing_piece[i].append("k")
            else: existing_piece[i].append("v")

        for x,y,f in existing_piece:
            add_piece(x,y,f,table,n)

        existing_piece = tuple(tuple(item) for item in existing_piece)
        
    return n, l, k, v, existing_piece, permut_piece, table

def write_output(file_path:str, solutions:tuple) -> None:
    """
        Запись результатов в output.txt.

        :param 
        file_path(str): Входное значение с адрессом входного файла
        solutions(str): Список всех уникальных значений координат расстановок фигур

        :return 
        None
    """
    with open(file_path, 'w') as file:
        if solutions:
            for solution in solutions:
                solution_str = " ".join("({}, {}, {})".format(x, y, f) for x, y, f in solution)

                file.write(solution_str + "\n")
        else:
            file.write("no solutions\n")
def get_solution(n,table) -> tuple:
    solution = []
    for y in range(n):
        for x in range(n):
            if table[y][x] == 'k':
                solution.append((x,y,'k'))
            if table[y][x] == 'v':
                solution.append((x,y,'v'))
    return solution
def is_safe(x:int, y:int, piece_type:str, table: tuple) -> bool:
    """
    Проверка, безопасно ли поставить фигуру в клетку (x, y).

    :param 
    x(int) & y(int): Входные значения с координатами фигуры на поле
    piece_type(str): Строкое значение, обозначающее тип фигуры: "v" - визирь и "k" - конь
    table(tuple): Текущая матрица позиций фигур
    
    :return 
    (bool): Если фигура не находится под боем в этих координатах, то возвращаем True, иначе False
    """

    if table[y][x] != '0':
        return False  # Клетка уже занята или под боем
    
    piece_moves = {
        # конь
        "k":[(-2, -1), (-2, 1), (2, -1), (2, 1),
        (-1, -2), (-1, 2), (1, -2), (1, 2)],
        # виверь
        "v":[(-2, 0), (-1, 0), (2, 0), (1, 0),
        (0, -2), (0, 2), (0, -1), (0, 1)]
    }
    
    # Проверка: не атакует ли новая фигура кого-то
    for dx, dy in piece_moves[piece_type]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n:
                if table[ny][nx] in ('k', 'v'):  # Фигура бьёт существующую
                    return False

    # Проверка: не атакует ли кто-то новую фигуру
    for fx in range(n):
        for fy in range(n):
            if table[fy][fx] in ('k', 'v'):
                for dx, dy in piece_moves[table[fy][fx]]:
                    if (fx + dx == x) and (fy + dy == y):
                        return False
    # for dx, dy in piece_moves['k']:
    #     if 0 <= x + dx < n and 0 <= y + dy < n:
    #         if table[y + dy][x + dx] == "k": return False
    # for dx, dy in piece_moves['v']:
    #     if 0 <= x + dx < n and 0 <= y + dy < n:
    #         if table[y + dy][x + dx] == "v": return False

    return 0 <= x < n and 0 <= y < n

def place_pieces_with_combinations(table,combinations:list) -> list:
    """
    Поиск всех возможных расстановок дополнительных фигур.
    
    :param 
    n(int): Размерность поля
    existing_piece(list): Список координат всех существующих фигур с названием фигуры
    combinations(list): Список всех сочетаний из L фигур, таких как конь и визирь

    
    :return 
    solutions(list): Список всех возможных расположений фигур не под боем
    """
    solutions = []

    def backtrack(remaining_combination:list, table:list) -> None:
        """
        Рекурсивная функция для расположения всех фигур в безопастные позиции
        
        :param 
        remaining_combination(list): Оставшиеся фигуры для расположения на поле
        pieces(list): Список координат всех существующих фигур с названием фигуры

        :return 
        (None)
        """
        if not remaining_combination:
            solutions.append(get_solution(n,table))
            return

        piece_type = remaining_combination[0]  # Берем первый тип фигуры из комбинации
        for x in range(n):
            for y in range(n):
                if is_safe(x, y, piece_type, table):
                    add_piece(x, y, piece_type,table,n)
                    backtrack(remaining_combination[1:], table)
                    remove_piece(x, y, piece_type,table,n)

    # Перебор всех комбинаций
    for combination in combinations:
        backtrack(combination, table)
    return solutions


if __name__ == "__main__":
    # Чтение входных данных
    n, l, k, v, existing_pieces, permut_piece, table = read_input("input.txt")
    print(n, l, k, v, existing_pieces, permut_piece)
    for row in table:
        print(row)
    # Проверка корректности входных данных
    assert all(0 <= x < n and 0 <= y < n for x, y, f in existing_pieces), "Некорректные координаты входных данных."
    # Поиск решений
    solutions = place_pieces_with_combinations(table,permut_piece)
    

    # # Избавляемся от повторяющихся позиций
    solutions = set(tuple(solution) for solution in solutions)
    # Запись решений в файл
    write_output("output.txt", solutions)
    print(len(solutions))

