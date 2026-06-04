################################################################################
# Лабораторная работа №1 по дисциплине "ЛОИС"
# Выполнена студентом группы 421702 БГУИР Перервой Павлом Дмитриевичем
# Файл: test_parser.py — Автоматические тесты для синтаксического анализатора
# Дата: 03.06.2026
#
# Ссылки на использованные материалы:
# [1] Голенков, В. В. Логические основы интеллектуальных систем. Практикум.
# [2] Документация Python: https://docs.pytest.org/en/stable/
################################################################################

import pytest
from src.parser import parse, ASTNode
from src.utils import FormulaError

# ============== Тесты на базовые формулы ==============

def test_parse_valid_structures():
    """Проверка корректного построения AST для правильных формул."""
    tree = parse("A")
    assert tree.type == 'VAR'
    assert tree.value == 'A'
    
    tree = parse("(!B)")
    assert tree.type == 'UNARY'
    assert tree.value == '!'
    assert tree.left.type == 'VAR'
    assert tree.left.value == 'B'
    
    tree = parse("(A|B)")
    assert tree.type == 'BINARY'
    assert tree.value == '|'
    assert tree.left.value == 'A'
    assert tree.right.value == 'B'

def test_parse_single_variables():
    """Тесты парсинга одиночных переменных."""
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        tree = parse(letter)
        assert tree.type == 'VAR'
        assert tree.value == letter

def test_parse_constants():
    """Тесты парсинга логических констант."""
    tree = parse("0")
    assert tree.type == 'CONST'
    assert tree.value == '0'
    
    tree = parse("1")
    assert tree.type == 'CONST'
    assert tree.value == '1'

# ============== Тесты на унарные формулы ==============

def test_parse_negation():
    """Проверка парсинга отрицания различных элементов."""
    tree = parse("(!A)")
    assert tree.type == 'UNARY'
    assert tree.value == '!'
    assert tree.left.value == 'A'
    
    tree = parse("(!B)")
    assert tree.type == 'UNARY'
    assert tree.left.value == 'B'

def test_parse_negation_of_constant():
    """Проверка парсинга отрицания констант."""
    tree = parse("(!0)")
    assert tree.type == 'UNARY'
    assert tree.left.type == 'CONST'
    assert tree.left.value == '0'
    
    tree = parse("(!1)")
    assert tree.type == 'UNARY'
    assert tree.left.type == 'CONST'
    assert tree.left.value == '1'

# ============== Тесты на бинарные формулы ==============

def test_parse_conjunction():
    """Проверка парсинга конъюнкции."""
    tree = parse("(A&B)")
    assert tree.type == 'BINARY'
    assert tree.value == '&'
    assert tree.left.value == 'A'
    assert tree.right.value == 'B'

def test_parse_disjunction():
    """Проверка парсинга дизъюнкции."""
    tree = parse("(A|B)")
    assert tree.type == 'BINARY'
    assert tree.value == '|'
    assert tree.left.value == 'A'
    assert tree.right.value == 'B'

def test_parse_implication():
    """Проверка парсинга импликации."""
    tree = parse("(A>B)")
    assert tree.type == 'BINARY'
    assert tree.value == '>'
    assert tree.left.value == 'A'
    assert tree.right.value == 'B'

def test_parse_biconditional():
    """Проверка парсинга эквивалентности."""
    tree = parse("(A~B)")
    assert tree.type == 'BINARY'
    assert tree.value == '~'
    assert tree.left.value == 'A'
    assert tree.right.value == 'B'

def test_parse_binary_with_constants():
    """Проверка парсинга бинарных операций с константами."""
    tree = parse("(0&1)")
    assert tree.type == 'BINARY'
    assert tree.left.type == 'CONST'
    assert tree.right.type == 'CONST'
    
    tree = parse("(0|1)")
    assert tree.type == 'BINARY'
    assert tree.left.type == 'CONST'
    assert tree.right.type == 'CONST'

# ============== Тесты на вложенные формулы ==============

def test_parse_unary_in_binary():
    """Проверка парсинга унарной операции внутри бинарной."""
    tree = parse("((!A)|B)")
    assert tree.type == 'BINARY'
    assert tree.left.type == 'UNARY'
    assert tree.right.type == 'VAR'

def test_parse_binary_with_negations():
    """Проверка парсинга бинарной операции с отрицаниями."""
    tree = parse("((!A)|(!B))")
    assert tree.type == 'BINARY'
    assert tree.left.type == 'UNARY'
    assert tree.right.type == 'UNARY'

# ============== Тесты на синтаксические ошибки ==============

def test_parse_invalid_syntax():
    """Проверка синтаксических ошибок (скобки, пустые строки)."""
    with pytest.raises(FormulaError) as exc:
        parse("")
    assert "пустая формула" in str(exc.value)

def test_parse_missing_closing_paren():
    """Проверка ошибки: не хватает закрывающей скобки."""
    with pytest.raises(FormulaError) as exc:
        parse("(A|B")
    assert "Неожиданный конец формулы" in str(exc.value) or "Ожидалась закрывающая скобка" in str(exc.value)

def test_parse_extra_symbols():
    """Проверка ошибки: лишние символы после правильной формулы."""
    with pytest.raises(FormulaError) as exc:
        parse("A|B")
    assert "Обнаружены лишние символы" in str(exc.value)

def test_parse_three_operands():
    """Проверка ошибки: попытка использовать три операнда в бинарной операции."""
    with pytest.raises(FormulaError) as exc:
        parse("(A|B|C)")
    assert "Ожидалась закрывающая скобка" in str(exc.value)

def test_parse_missing_operand():
    """Проверка ошибки: пропущен операнд."""
    with pytest.raises(FormulaError) as exc:
        parse("(A|)")
    assert "Неожиданный символ" in str(exc.value) or "ожиданной" in str(exc.value).lower()

def test_parse_missing_opening_paren():
    """Проверка ошибки: не хватает открывающей скобки."""
    with pytest.raises(FormulaError) as exc:
        parse("A|B)")
    assert "Обнаружены лишние символы" in str(exc.value) or "Неожиданный символ" in str(exc.value)

def test_parse_unary_without_operand():
    """Проверка ошибки: унарный оператор без операнда."""
    with pytest.raises(FormulaError) as exc:
        parse("(!)")
    assert "Неожиданный символ" in str(exc.value) or "ожиданной" in str(exc.value).lower()

def test_parse_binary_without_operator():
    """Проверка ошибки: бинарная операция без оператора."""
    with pytest.raises(FormulaError) as exc:
        parse("(AB)")
    assert "Ожидался бинарный оператор" in str(exc.value)

def test_parse_invalid_char_in_formula():
    """Проверка ошибки: недопустимый символ в формуле."""
    with pytest.raises(FormulaError) as exc:
        parse("(A@B)")

# ============== Тесты на граничные случаи ==============

def test_parse_single_char_formulas():
    """Тесты на граничные случаи одиночных символов."""
    for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        tree = parse(ch)
        assert tree.type == 'VAR'
        assert tree.value == ch

def test_parse_long_chain_of_operations():
    """Проверка парсинга длинной цепочки операций."""
    tree = parse("((((A&B)|C)&D)|E)")
    assert tree.type == 'BINARY'
    assert tree.value == '|'