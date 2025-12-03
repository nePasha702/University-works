#include "include/Multiset.h"
#include "main.h"
#include <iostream>
#include <limits>

void displayMenu() {
    std::cout << "\n=== МЕНЮ ===" << std::endl;
    std::cout << "1. Создать/изменить мультимножество" << std::endl;
    std::cout << "2. Добавить элемент" << std::endl;
    std::cout << "3. Вывести мультимножество" << std::endl;
    std::cout << "4. Удалить элемент" << std::endl;
    std::cout << "5. Мощность множества" << std::endl;
    std::cout << "6. Проверить наличие элемента" << std::endl;
    std::cout << "7. Объединение двух множеств" << std::endl;
    std::cout << "8. Пересечение двух множеств" << std::endl;
    std::cout << "9. Разность двух множеств" << std::endl;
    std::cout << "10. Тест операторов (=, +, +=, *, *=, -, -=)" << std::endl;
    std::cout << "0. Выход" << std::endl;
    std::cout << "Выберите действие: ";
}

void clearInputBuffer() {
    std::cin.clear();
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

void runMenu() {
    Multiset currentSet;
    int choice = 0;
    
    do {
        displayMenu();
        std::cin >> choice;
        clearInputBuffer();
        
        switch(choice) {
            case 1: {
                std::cout << "\nВведите множество в формате {элементы}:" << std::endl;
                std::cout << "Пример: {a, a, b, {c, d}}" << std::endl;
                std::cout << "Ввод: ";
                
                std::string input;
                std::getline(std::cin, input);
                
                try {
                    currentSet = Multiset(input);
                    std::cout << "Создано: " << currentSet << std::endl;
                } catch (const std::exception& e) {
                    std::cout << "Ошибка: " << e.what() << std::endl;
                }
                break;
            }
            
            case 2: {
                if (currentSet.isEmpty()) {
                    std::cout << "Сначала создайте множество" << std::endl;
                    break;
                }
                
                std::cout << "\n1. Добавить символ" << std::endl;
                std::cout << "2. Добавить вложенное множество" << std::endl;
                std::cout << "Выбор: ";
                
                int type;
                std::cin >> type;
                clearInputBuffer();
                
                if (type == 1) {
                    std::cout << "Введите символ: ";
                    char c;
                    std::cin >> c;
                    clearInputBuffer();
                    
                    currentSet.addElement(c);
                    std::cout << "Добавлено. Результат: " << currentSet << std::endl;
                } 
                else if (type == 2) {
                    std::cout << "Введите множество: ";
                    std::string input;
                    std::getline(std::cin, input);
                    
                    try {
                        Multiset nested(input);
                        currentSet.addElement(nested);
                        std::cout << "Добавлено. Результат: " << currentSet << std::endl;
                    } catch (const std::exception& e) {
                        std::cout << "Ошибка: " << e.what() << std::endl;
                    }
                }
                break;
            }
            
            case 3: {
                std::cout << "\nТекущее множество: " << currentSet << std::endl;
                break;
            }
            
            case 4: {
                if (currentSet.isEmpty()) {
                    std::cout << "Множество пустое" << std::endl;
                    break;
                }
                
                std::cout << "Введите символ для удаления: ";
                char c;
                std::cin >> c;
                clearInputBuffer();
                
                if (currentSet.contains(c)) {
                    currentSet.removeElement(c);
                    std::cout << "Удалено. Результат: " << currentSet << std::endl;
                } else {
                    std::cout << "Элемент не найден" << std::endl;
                }
                break;
            }
            
            case 5: {
                std::cout << "\nМощность множества: " << currentSet.cardinality() << std::endl;
                break;
            }
            
            case 6: {
                if (currentSet.isEmpty()) {
                    std::cout << "Множество пустое" << std::endl;
                    break;
                }
                
                std::cout << "Введите символ для проверки: ";
                char c;
                std::cin >> c;
                clearInputBuffer();
                
                if (currentSet.contains(c)) {
                    std::cout << "Найден " << currentSet.count(c) << " раз(а)" << std::endl;
                } else {
                    std::cout << "Не найден" << std::endl;
                }
                break;
            }
            
            case 7: {
                std::cout << "\nВведите второе множество: ";
                std::string input;
                std::getline(std::cin, input);
                
                try {
                    Multiset setB(input);
                    Multiset result = currentSet + setB;
                    std::cout << currentSet << " + " << setB << " = " << result << std::endl;
                } catch (const std::exception& e) {
                    std::cout << "Ошибка: " << e.what() << std::endl;
                }
                break;
            }
            
            case 8: {
                std::cout << "\nВведите второе множество: ";
                std::string input;
                std::getline(std::cin, input);
                
                try {
                    Multiset setB(input);
                    Multiset result = currentSet * setB;
                    std::cout << currentSet << " * " << setB << " = " << result << std::endl;
                } catch (const std::exception& e) {
                    std::cout << "Ошибка: " << e.what() << std::endl;
                }
                break;
            }
            
            case 9: {
                std::cout << "\nВведите второе множество: ";
                std::string input;
                std::getline(std::cin, input);
                
                try {
                    Multiset setB(input);
                    Multiset result = currentSet - setB;
                    std::cout << currentSet << " - " << setB << " = " << result << std::endl;
                } catch (const std::exception& e) {
                    std::cout << "Ошибка: " << e.what() << std::endl;
                }
                break;
            }
            
            case 10: {
                std::cout << "\n=== ТЕСТ ОПЕРАТОРОВ ===" << std::endl;
                
                Multiset A("{a, b, c}");
                Multiset B("{b, c, d}");
                
                std::cout << "A = " << A << std::endl;
                std::cout << "B = " << B << std::endl;
                
                // Оператор =
                Multiset C = A;
                std::cout << "C = A: " << C << std::endl;
                
                // Оператор +
                Multiset D = A + B;
                std::cout << "A + B: " << D << std::endl;
                
                // Оператор +=
                C += B;
                std::cout << "C += B: " << C << std::endl;
                
                // Оператор *
                Multiset E = A * B;
                std::cout << "A * B: " << E << std::endl;
                
                // Оператор *=
                C = A;
                C *= B;
                std::cout << "C *= B: " << C << std::endl;
                
                // Оператор -
                Multiset F = A - B;
                std::cout << "A - B: " << F << std::endl;
                
                // Оператор -=
                C = A;
                C -= B;
                std::cout << "C -= B: " << C << std::endl;
                break;
            }
            
            case 0: {
                std::cout << "Выход" << std::endl;
                break;
            }
            
            default: {
                std::cout << "Неверный выбор" << std::endl;
                break;
            }
        }
        
        if (choice != 0) {
            std::cout << "\nНажмите Enter для продолжения";
            std::cin.get();
        }
        
    } while (choice != 0);
}

int main() {
    runMenu();
    return 0;
}
