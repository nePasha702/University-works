################################################################################
# Лабораторная работа №1 по дисциплине "ЛОИС"
# Выполнена студентом группы 421702 БГУИР Перервой Павлом Дмитриевичем
# Файл: lexer.py — Лексический анализатор (токенизация и проверка алфавита)
# Дата: 01.06.2026
#
# Ссылки на использованные материалы:
# [1] Голенков, В. В. Логические основы интеллектуальных систем. Практикум.
# [2] The Python Tutorial: https://docs.python.org/3/tutorial/index.html
# [3] Python school: https://www.w3schools.com/python/
# ################################################################################

from src.utils import die

def not_extraneous_symbol(c: str) -> bool:
    """
    Проверяет, входит ли одиночный символ в базовый алфавит 
    сокращенного языка логики высказываний.
    """
    valid_chars = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ01()!/\\->~")
    return c in valid_chars

def prepare(src: str) -> str:
    """
    Очищает строку от пробелов, проверяет алфавит и заменяет
    двухсимвольные операторы на внутреннюю односимвольную запись.
    /\ заменяется на &
    \/ заменяется на |
    -> заменяется на >
    """
    dest = []
    i = 0
    length = len(src)

    while i < length:
        c = src[i]

        if c.isspace():
            i += 1
            continue

        if not not_extraneous_symbol(c):
            die(f"Символ '{c}' не входит в алфавит сокращённого языка логики высказываний")

        if c == '/' and i + 1 < length and src[i+1] == '\\':
            dest.append('&')
            i += 2
            continue

        if c == '\\' and i + 1 < length and src[i+1] == '/':
            dest.append('|')
            i += 2
            continue

        if c == '-' and i + 1 < length and src[i+1] == '>':
            dest.append('>')
            i += 2
            continue

        if c in ('/', '\\', '-'):
            die(f"Символ '{c}' не является корректным логическим оператором")

        dest.append(c)
        i += 1

    return "".join(dest)