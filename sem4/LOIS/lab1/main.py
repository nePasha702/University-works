################################################################################
# Лабораторная работа №1 по дисциплине "ЛОИС"
# Выполнена студентом группы 421702 БГУИР Перервой Павлом Дмитриевичем
# Файл: main.py — Главный модуль, консольный интерфейс и режим тестирования
# Дата: 01.06.2026
#
# Ссылки на использованные материалы:
# [1] Голенков, В. В. Логические основы интеллектуальных систем. Практикум.
# [2] The Python Tutorial: https://docs.python.org/3/tutorial/index.html
# [3] Python school: https://www.w3schools.com/python/
# ################################################################################

import sys
from src.lexer import prepare
from src.parser import parse
from src.validator import is_pcnf
from src.utils import FormulaError

def check_custom_formula() -> None:
    """Режим 1: Ручной ввод формулы пользователем и её полная валидация."""
    print("\n--- РЕЖИМ ПРОВЕРКИ ПОЛЬЗОВАТЕЛЬСКОЙ ФОРМУЛЫ ---")
    print("Допустимый алфавит: Заглавные латинские буквы, {0,1}, !, /\\, \\/, ->, ~, (, )")
    
    try:
        src_formula = input("Введите формулу сокращенного языка логики высказываний: ")
        
        cleaned_str = prepare(src_formula)
        ast_root = parse(cleaned_str)
        if is_pcnf(ast_root):
            print("Результат: Введенная формула является СКНФ.")
            
    except FormulaError as e:
        print(f"Ошибка: {e}")
    except KeyboardInterrupt:
        print("\nВвод прерван пользователем.")
        sys.exit(0)


def run_knowledge_testing() -> None:
    """Режим 2: Интерактивное тестирование знаний пользователя."""
    print("\n--- РЕЖИМ ТЕСТИРОВАНИЯ ЗНАНИЙ ПОЛЬЗОВАТЕЛЯ ---")
    print("Система будет предлагать формулы. Необходимо определить, являются ли они СКНФ.")
    print("Введите '1', если формула является СКНФ, или '0', если не является.\n")

    test_cases = [
        {
            "formula": "((A\\/B)/\\((!A)\\/B))",
            "description": "Классическая правильная СКНФ от двух переменных"
        },
        {
            "formula": "((A\\/B)/\\A)",
            "description": "Не СКНФ (во втором макстерме отсутствует переменная B, он несовершенен)"
        },
        {
            "formula": "(((A\\/B)\\/C)/\\(((!A)\\/B)\\/C))",
            "description": "Правильная СКНФ от трех переменных"
        },
        {
            "formula": "((A\\/B)/\\(A\\/B))",
            "description": "Не СКНФ (присутствуют абсолютно одинаковые макстермы)"
        },
        {
            "formula": "((A\\/B)\\/((!A)\\/B))",
            "description": "Не СКНФ (главная операция — дизъюнкция, а должна быть конъюнкция макстермов)"
        },
        {
            "formula": "((((!A)\\/(!B))/\\((!A)\\/B))/\\(A\\/B))",
            "description": "Правильная полная СКНФ из трех макстермов (переменные A и B)"
        }
        
    ]

    score = 0
    total = len(test_cases)

    for idx, case in enumerate(test_cases, 1):
        print(f"Вопрос {idx}/{total}. Анализируемая формула: {case['formula']}")
        
        try:
            cleaned = prepare(case["formula"])
            tree = parse(cleaned)
            correct_answer = 1 if is_pcnf(tree) else 0
        except FormulaError:
            correct_answer = 0

        while True:
            user_input = input("Ваш ответ (1 - Да, 0 - Нет): ").strip()
            if user_input in ('1', '0'):
                user_answer = int(user_input)
                break
            print("Некорректный ввод. Пожалуйста, введите только цифру 1 или 0.")

        if user_answer == correct_answer:
            print("Правильно!\n")
            score += 1
        else:
            print(f"Неправильно. Пояснение: {case['description']}\n")

    print(f"Тестирование завершено. Ваш результат: {score} из {total} правильных ответов.")


def main() -> None:
    """Главная управляющая функция приложения."""
    while True:
        print("\n=============================================")
        print("ЛАБОРАТОРНАЯ РАБОТА №1. ВАРИАНТ 12 (СКНФ)")
        print("=============================================")
        print("1. Проверить формулу (ручной ввод)")
        print("2. Режим тестирования знаний пользователя")
        print("3. Выход из программы")
        print("=============================================")
        
        choice = input("Выберите режим работы (1-3): ").strip()
        
        if choice == '1':
            check_custom_formula()
        elif choice == '2':
            run_knowledge_testing()
        elif choice == '3':
            print("Работа программы завершена.")
            sys.exit(0)
        else:
            print("Ошибка: выбран несуществующий пункт меню. Повторите попытку.")

if __name__ == "__main__":
    main()