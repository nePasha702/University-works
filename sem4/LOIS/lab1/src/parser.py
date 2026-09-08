################################################################################
# Лабораторная работа №1 по дисциплине "ЛОИС"
# Выполнена студентом группы 421702 БГУИР Перервой Павлом Дмитриевичем
# Файл: parser.py — Синтаксический анализатор (построение дерева разбора)
# Дата: 01.06.2026
#
# Ссылки на использованные материалы:
# [1] Голенков, В. В. Логические основы интеллектуальных систем. Практикум.
# [2] The Python Tutorial.: https://docs.python.org/3/tutorial/index.html
# [3] Python school: https://www.w3schools.com/python/
################################################################################

from src.utils import die

class ASTNode:
    """
    Класс для представления узла абстрактного синтаксического дерева (AST).
    """
    def __init__(self, node_type: str, value: str, left=None, right=None):
        self.type = node_type 
        self.value = value  
        self.left = left    
        self.right = right     

    def __repr__(self):
        if self.type in ('VAR', 'CONST'):
            return self.value
        elif self.type == 'UNARY':
            return f"(!{self.left})"
        else:
            return f"({self.left}{self.value}{self.right})"


def parse_formula(src: str, pos: int):
    """
    Рекурсивная функция разбора формулы. 
    Принимает строку и текущую позицию чтения.
    Возвращает кортеж: (созданный узел дерева, новая позиция чтения).
    """
    if pos >= len(src):
        die("Неожиданный конец формулы")

    c = src[pos]

    if c == '0' or c == '1':
        return ASTNode('CONST', c), pos + 1

    if c.isupper() and c.isalpha():
        return ASTNode('VAR', c), pos + 1

    if c == '(':
        pos += 1
        if pos >= len(src):
            die("Ожидалось тело формулы после открывающей скобки '('")

        if src[pos] == '!':
            pos += 1
            child_node, pos = parse_formula(src, pos)
            
            if pos >= len(src) or src[pos] != ')':
                die("Ожидалась закрывающая скобка ')' для унарной операции")
            
            return ASTNode('UNARY', '!', left=child_node), pos + 1

        left_child, pos = parse_formula(src, pos)

        if pos >= len(src) or src[pos] not in ('&', '|', '>', '~'):
            die("Ожидался бинарный оператор после первого аргумента в скобках")
        
        op = src[pos]
        pos += 1

        right_child, pos = parse_formula(src, pos)

        if pos >= len(src) or src[pos] != ')':
            die("Ожидалась закрывающая скобка ')' для бинарной операции")

        return ASTNode('BINARY', op, left=left_child, right=right_child), pos + 1


    die(f"Неожиданный символ '{c}' при синтаксическом разборе")


def parse(src: str) -> ASTNode:
    """
    Точка входа для синтаксического анализатора.
    Запускает рекурсивный разбор и проверяет, что строка разобрана полностью.
    """
    if not src:
        die("На вход подана пустая формула")

    root_node, pos = parse_formula(src, 0)

    if pos < len(src):
        die("Обнаружены лишние символы после формулы.")

    return root_node