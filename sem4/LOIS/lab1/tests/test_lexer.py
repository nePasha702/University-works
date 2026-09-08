################################################################################
# Лабораторная работа №1 по дисциплине "ЛОИС"
# Выполнена студентом группы 421702 БГУИР Перервой Павлом Дмитриевичем
# Файл: test_lexer.py — Автоматические тесты для лексического анализатора
# Дата: 01.06.2026
#
# Ссылки на использованные материалы:
# [1] Голенков, В. В. Логические основы интеллектуальных систем. Практикум.
# [2] Документация Python: https://docs.pytest.org/en/stable/
################################################################################

import pytest
from src.lexer import prepare
from src.utils import FormulaError

# ============== Тесты на основные символы и переменные ==============

def test_prepare_valid_symbols():
    """Проверка правильной токенизации и очистки от пробелов."""
    assert prepare("A") == "A"
    assert prepare("1") == "1"
    
    assert prepare("(!A)") == "(!A)"
    assert prepare("(A\\/B)") == "(A|B)"
    assert prepare("(A/\\B)") == "(A&B)"
    assert prepare("(A->B)") == "(A>B)"
    assert prepare("(A~B)") == "(A~B)"
    
    assert prepare("  ( A \\/ B )  ") == "(A|B)"

def test_prepare_single_variables():
    """Тесты для одиночных переменных."""
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        assert prepare(letter) == letter

def test_prepare_single_constants():
    """Тесты для логических констант."""
    assert prepare("0") == "0"
    assert prepare("1") == "1"

def test_prepare_disjunction_replacement():
    """Проверка замены оператора дизъюнкции."""
    assert prepare("\\/") == "|"
    assert prepare("(A\\/B)") == "(A|B)"
    assert prepare("(A\\/B\\/C)") == "(A|B|C)"
    assert prepare("(X\\/Y)") == "(X|Y)"

def test_prepare_conjunction_replacement():
    """Проверка замены оператора конъюнкции."""
    assert prepare("/\\") == "&"
    assert prepare("(A/\\B)") == "(A&B)"
    assert prepare("(A/\\B/\\C)") == "(A&B&C)"
    assert prepare("(X/\\Y)") == "(X&Y)"

def test_prepare_implication_replacement():
    """Проверка замены оператора импликации."""
    assert prepare("->") == ">"
    assert prepare("(A->B)") == "(A>B)"
    assert prepare("(A->B->C)") == "(A>B>C)"
    assert prepare("(X->Y)") == "(X>Y)"

def test_prepare_complex_formula_replacement():
    """Проверка замены всех операторов в сложной формуле."""
    assert prepare("((A/\\B)\\/(C->D))") == "((A&B)|(C>D))"
    assert prepare("((!A)/\\(B\\/C))") == "((!A)&(B|C))"
    assert prepare("((A~B)\\/(C->D))") == "((A~B)|(C>D))"

def test_prepare_negation_operator():
    """Проверка оператора отрицания."""
    assert prepare("!A") == "!A"
    assert prepare("(!A)") == "(!A)"
    assert prepare("(!!A)") == "(!!A)"
    assert prepare("(!B)") == "(!B)"

def test_prepare_biconditional_operator():
    """Проверка оператора эквивалентности."""
    assert prepare("(A~B)") == "(A~B)"
    assert prepare("(X~Y)") == "(X~Y)"

def test_prepare_parentheses():
    """Проверка сохранения скобок."""
    assert prepare("(A)") == "(A)"
    assert prepare("((A))") == "((A))"
    assert prepare("(((A)))") == "(((A)))"

# ============== Тесты на ошибочные символы ==============

def test_prepare_invalid_symbols():
    """Проверка того, что лексер выбрасывает ошибку на мусорные символы."""
    with pytest.raises(FormulaError) as exc:
        prepare("(A\\/С)")
    assert "не входит в алфавит" in str(exc.value)

    with pytest.raises(FormulaError) as exc:
        prepare("(A\\/2)")
    assert "не входит в алфавит" in str(exc.value)

def test_prepare_special_symbols_rejected():
    """Проверка отклонения специальных символов."""
    invalid_chars = ["@", "#", "$", "%", "^", "*", "+", "=", "[", "]", "{", "}", ";", ":", ",", ".", "?", "&"]
    for char in invalid_chars:
        with pytest.raises(FormulaError) as exc:
            prepare(f"(A{char}B)")
        assert "не входит в алфавит" in str(exc.value) or "не является корректным" in str(exc.value)

def test_prepare_lowercase_letters_rejected():
    """Проверка отклонения прописных букв."""
    for letter in "abcdefghijklmnopqrstuvwxyz":
        with pytest.raises(FormulaError) as exc:
            prepare(letter)
        assert "не входит в алфавит" in str(exc.value)

def test_prepare_digits_rejected():
    """Проверка отклонения недопустимых цифр (кроме 0 и 1)."""
    for digit in "23456789":
        with pytest.raises(FormulaError) as exc:
            prepare(digit)
        assert "не входит в алфавит" in str(exc.value)

# ============== Тесты на поврежденные операторы ==============

def test_prepare_dangling_operators():
    """Проверка защиты от 'оборванных' операторов (например, одиночный слеш)."""
    with pytest.raises(FormulaError) as exc:
        prepare("(A \\ B)")
    assert "не является корректным" in str(exc.value)

def test_prepare_incomplete_operators():
    """Проверка отклонения неполных операторов."""
    with pytest.raises(FormulaError) as exc:
        prepare("A/B")
    assert "не является корректным" in str(exc.value)
    
    with pytest.raises(FormulaError) as exc:
        prepare("A\\B")
    assert "не является корректным" in str(exc.value)
    
    with pytest.raises(FormulaError) as exc:
        prepare("A-B")
    assert "не является корректным" in str(exc.value)