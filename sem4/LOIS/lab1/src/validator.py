################################################################################
# Лабораторная работа №1 по дисциплине "ЛОИС"
# Выполнена студентом группы 421702 БГУИР Перервой Павлом Дмитриевичем
# Файл: validator.py — Семантический анализатор (проверка на СКНФ)
# Дата: 01.06.2026
#
# Ссылки на использованные материалы:
# [1] Голенков, В. В. Логические основы интеллектуальных систем. Практикум.
# [2] The Python Tutorial: https://docs.python.org/3/tutorial/index.html
# [3] Python school: https://www.w3schools.com/python/
# ################################################################################

from src.utils import die
from src.parser import ASTNode

def get_all_variables(node: ASTNode) -> set:
    """Рекурсивно собирает множество всех уникальных переменных в формуле."""
    if node.type == 'VAR':
        return {node.value}
    elif node.type == 'UNARY':
        return get_all_variables(node.left)
    elif node.type == 'BINARY':
        return get_all_variables(node.left).union(get_all_variables(node.right))
    return set()

def collect_maxterms(node: ASTNode) -> list:
    """
    Разбивает верхний уровень дерева по операциям конъюнкции (&).
    Возвращает список узлов, которые являются макстермами.
    """
    if node.type == 'BINARY' and node.value == '&':
        return collect_maxterms(node.left) + collect_maxterms(node.right)
    return [node]

def validate_and_extract_literals(node: ASTNode) -> list:
    """
    Проверяет, что макстерм состоит только из дизъюнкций (|) и литералов.
    Возвращает список строковых представлений литералов (например, ['A', '!B']).
    """
    if node.type == 'BINARY' and node.value == '|':
        return validate_and_extract_literals(node.left) + validate_and_extract_literals(node.right)
    
    elif node.type == 'VAR':
        return [node.value]
    
    elif node.type == 'UNARY' and node.value == '!' and node.left.type == 'VAR':
        return ['!' + node.left.value]
    
    else:
        die("Формула не является СКНФ: обнаружены недопустимые операции (или константы) внутри макстерма")

def is_pcnf(root_node: ASTNode) -> bool:
    """
    Главная функция валидации СКНФ.
    Проверяет все математические критерии совершенной формы.
    """
    global_vars = get_all_variables(root_node)
    if not global_vars:
        die("Формула не является СКНФ: отсутствуют пропозициональные переменные")

    maxterm_nodes = collect_maxterms(root_node)
    
    normalized_maxterms = []

    for m_node in maxterm_nodes:
        literals = validate_and_extract_literals(m_node)
        
        local_vars = set()
        for lit in literals:
            var_name = lit[-1] 
            if var_name in local_vars:
                die(f"Формула не является СКНФ: в макстерме дублируется переменная '{var_name}'")
            local_vars.add(var_name)

        if local_vars != global_vars:
            die("Формула не является СКНФ: макстерм не содержит полного набора переменных")

        normalized_maxterms.append(tuple(sorted(literals)))

    if len(set(normalized_maxterms)) != len(normalized_maxterms):
        die("Формула не является СКНФ: в формуле присутствуют одинаковые макстермы")

    return True