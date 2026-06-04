################################################################################
# Лабораторная работа №1 по дисциплине "ЛОИС"
# Выполнена студентом группы 421702 БГУИР Перервой Павлом Дмитриевичем
# Файл: test_validator.py — Автоматические тесты для семантического анализатора
# Дата: 03.06.2026
#
# Ссылки на использованные материалы:
# [1] Голенков, В. В. Логические основы интеллектуальных систем. Практикум.
# [2] Документация Python: https://docs.pytest.org/en/stable/
################################################################################

import pytest
from src.lexer import prepare
from src.parser import parse
from src.validator import is_pcnf, get_all_variables, collect_maxterms
from src.utils import FormulaError

# ============== Тесты на корректные СКНФ формулы ==============

def test_validator_valid_pcnf_single_maxterm():
    """Проверка корректной СКНФ с одним макстермом от одной переменной."""
    tree = parse(prepare("A"))
    assert is_pcnf(tree) is True

def test_validator_valid_pcnf_single_maxterm_with_negation():
    """Проверка корректной СКНФ: просто ¬A."""
    tree = parse(prepare("(!A)"))
    assert is_pcnf(tree) is True

# ============== Тесты на ошибку: дублирующиеся переменные ==============

def test_validator_duplicate_variables():
    """Проверка ошибки: дублирование переменных в одном макстерме."""
    tree = parse(prepare("((A\\/A)/\\((!A)\\/B))"))
    with pytest.raises(FormulaError) as exc:
        is_pcnf(tree)
    assert "дублируется переменная" in str(exc.value)

def test_validator_duplicate_variables_with_negation():
    """Проверка ошибки: переменная и её отрицание в одном макстерме."""
    tree = parse(prepare("((A\\/(! A))/\\(A\\/B))"))
    with pytest.raises(FormulaError) as exc:
        is_pcnf(tree)

# ============== Тесты на ошибку: отсутствие переменных ==============

def test_validator_missing_variables():
    """Проверка ошибки: макстерм не содержит полного набора переменных (несовершенность)."""
    tree = parse(prepare("((A\\/B)/\\A)"))
    with pytest.raises(FormulaError) as exc:
        is_pcnf(tree)
    assert "не содержит полного набора переменных" in str(exc.value)

# ============== Тесты на ошибку: дублирующиеся макстермы ==============

def test_validator_duplicate_maxterms():
    """Проверка ошибки: в формуле присутствуют абсолютно одинаковые макстермы."""
    tree = parse(prepare("((A\\/B)/\\(A\\/B))"))
    with pytest.raises(FormulaError) as exc:
        is_pcnf(tree)
    assert "присутствуют одинаковые макстермы" in str(exc.value)

# ============== Тесты на ошибку: недопустимые операции ==============

def test_validator_invalid_operations():
    """Проверка ошибки: внутри макстерма обнаружены недопустимые операторы (например, импликация)."""
    tree = parse(prepare("((A\\/B)/\\(A->B))"))
    with pytest.raises(FormulaError) as exc:
        is_pcnf(tree)
    assert "обнаружены недопустимые операции" in str(exc.value)

# ============== Тесты на ошибку: неправильная корневая операция ==============

def test_validator_wrong_root_operation():
    """
    Проверка ошибки: главная операция — дизъюнкция, а не конъюнкция.
    В таком случае анализатор воспримет всю строку как один гигантский 
    макстерм и найдет в нем дубликаты переменных.
    """
    tree = parse(prepare("((A\\/B)\\/(A\\/(!B)))"))
    with pytest.raises(FormulaError) as exc:
        is_pcnf(tree)
    assert "дублируется переменная" in str(exc.value)

# ============== Вспомогательные функции - тесты ==============

def test_get_all_variables_simple():
    """Проверка функции сбора переменных на простой формуле."""
    tree = parse(prepare("A"))
    vars_set = get_all_variables(tree)
    assert vars_set == {'A'}

def test_collect_maxterms_single():
    """Проверка функции сбора макстермов для одного макстерма."""
    tree = parse(prepare("(A\\/B)"))
    maxterms = collect_maxterms(tree)
    assert len(maxterms) == 1

def test_validator_single_variable_formula():
    """Проверка СКНФ для формулы с одной переменной."""
    tree = parse(prepare("A"))
    assert is_pcnf(tree) is True

def test_validator_single_negated_variable():
    """Проверка СКНФ для отрицания одной переменной."""
    tree = parse(prepare("(!A)"))
    assert is_pcnf(tree) is True
