# -*- coding: utf-8 -*-
"""
    Считываем файл с данными в формате: N L K, где N - размерность поля, L - количество фигур, которые нужно поставить на доску(так как у нас две фигуры, то это число отражает выборку фигур с повторениями)
    K - уже существующие фигуры, где первые K//2+1 - визири, а остальные - кони.
    Записываем в новый файл все возможнные позиции фигур не под боем
"""
from itertools import combinations_with_replacement
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
        n, l, k = map(int, lines[0].strip().split())
        existing_piece = [list(map(int,line.strip().split())) for line in lines[1:] if line.strip().split()]
        permut_piece = list(combinations_with_replacement('vk', l))
        for i in range(k):
            if i <= k//2: existing_piece[i].append("v")
            else: existing_piece[i].append("k")
        existing_piece = set(tuple(item) for item in existing_piece)
    return n, l, k, existing_piece, permut_piece

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

def is_safe(x:int, y:int, piece_type:str, placed_pieces:list, n:int) -> bool:
    """
    Проверка, безопасно ли поставить фигуру в клетку (x, y).

    :param 
    x(int) & y(int): Входные значения с координатами фигуры на поле
    piece_type(str): Строкое значение, обозначающее тип фигуры: "v" - визирь и "k" - конь
    placed_pieces(list): Список всех поставленных фигур
    n(int): Размерность поля
    
    :return 
    (bool): Если фигура не находится под боем в этих координатах, то возвращаем True, иначе False
    """
    piece_moves = {
        # конь
        "k":[(-2, -1), (-2, 1), (2, -1), (2, 1),
        (-1, -2), (-1, 2), (1, -2), (1, 2)],
        # виверь
        "v":[(-2, 0), (-1, 0), (2, 0), (1, 0),
        (0, -2), (0, 2), (0, -1), (0, 1)]
    }
    for dx,dy in piece_moves.get(piece_type):
        nx, ny = x + dx, y + dy
        if (nx, ny, "v") in placed_pieces and piece_type == "k":
            return False
        if (nx, ny, piece_type) in placed_pieces:
            return False
    return 0 <= x < n and 0 <= y < n

def place_pieces_with_combinations(n:int, existing_pieces:list,combinations:list):
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
    initial_pieces = set(existing_pieces)

    def backtrack(remaining_combination:list, pieces:list) -> None:
        """
        Рекурсивная функция для расположения всех фигур в безопастные позиции
        
        :param 
        remaining_combination(list): Оставшиеся фигуры для расположения на поле
        pieces(list): Список координат всех существующих фигур с названием фигуры

        :return 
        (None)
        """
        if not remaining_combination:
            solutions.append(sorted(pieces))
            return

        piece_type = remaining_combination[0]  # Берем первый тип фигуры из комбинации
        for x in range(n):
            for y in range(n):
                if ((x, y, piece_type) not in pieces and is_safe(x, y, piece_type, pieces, n)):
                    pieces.add((x, y, piece_type))
                    backtrack(remaining_combination[1:], pieces)
                    pieces.remove((x, y, piece_type))

    # Перебор всех комбинаций
    for combination in combinations:
        backtrack(combination, initial_pieces)
    return solutions

if __name__ == "__main__":
    # Чтение входных данных
    n, l, k, existing_pieces, permut_piece = read_input("input.txt")
    print(n, l, k, existing_pieces, permut_piece)
    # Проверка корректности входных данных
    assert all(0 <= x < n and 0 <= y < n for x, y, f in existing_pieces), "Некорректные координаты входных данных."

    # Поиск решений
    solutions = place_pieces_with_combinations(n,existing_pieces,permut_piece)


    # Избавляемся от повторяющихся позиций
    solutions = set(tuple(solution) for solution in solutions)
    # Запись решений в файл
    write_output("output.txt", solutions)

