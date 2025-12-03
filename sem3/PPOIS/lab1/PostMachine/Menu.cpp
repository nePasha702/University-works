#include "Menu.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <limits>

void Menu::displayMenu() {
    std::cout << "\n===== Меню =====\n";
    std::cout << "1. Загрузить программу из файла\n";
    std::cout << "2. Загрузить состояние ленты из файла\n";
    std::cout << "3. Добавить команду вручную\n";
    std::cout << "4. Просмотреть все команды программы\n";
    std::cout << "5. Изменить значение на ленте\n";
    std::cout << "6. Запуск полной интерпретации\n";
    std::cout << "7. Выполнить один шаг (+)\n";
    std::cout << "8. Сбросить состояние (-)\n";
    std::cout << "9. Показать текущее состояние\n";
    std::cout << "0. Выход\n";
    std::cout << "Выберите действие: ";
}

void Menu::handleUserInput(PostMachine& machine) {
    int choice;
    bool log = false;
    
    while (true) {
        displayMenu();
        std::cin >> choice;
        
        if (std::cin.fail()) {
            std::cin.clear();
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            std::cout << "Ошибка: введите число от 0 до 9\n";
            continue;
        }

        switch (choice) {
            case 1: loadProgramFromFile(machine); break;
            case 2: loadTapeState(machine); break;
            case 3: addRuleManually(machine); break;
            case 4: viewAllRules(machine); break;
            case 5: modifyTapeValue(machine); break;
            case 6: runFullInterpretation(machine, log); break;
            case 7: executeSingleStep(machine, log); break;
            case 8: resetState(machine); break;
            case 9: showCurrentState(machine); break;
            case 0: return;
            default: std::cout << "Неверный выбор\n";
        }
    }
}

void Menu::loadProgramFromFile(PostMachine& machine) {
    std::string filename;
    std::cout << "Введите имя файла: ";
    std::cin >> filename;
    
    std::ifstream file(filename);
    if (file) {
        machine.loadFromStream(file);
        std::cout << "Программа загружена\n";
    } else {
        std::cout << "Ошибка открытия файла\n";
    }
}

void Menu::loadTapeState(PostMachine& machine) {
    std::string state;
    std::cout << "Введите начальное состояние ленты: ";
    std::cin >> state;
    
    std::istringstream iss(state);
    machine.loadTapeState(iss);
    std::cout << "Состояние ленты загружено\n";
}

void Menu::addRuleManually(PostMachine& machine) {
    int cs, ns;
    char csym, nsym;
    char shiftChar;
    
    std::cout << "Текущее состояние: ";
    std::cin >> cs;
    std::cout << "Текущий символ: ";
    std::cin >> csym;
    std::cout << "Новое состояние: ";
    std::cin >> ns;
    std::cout << "Новый символ: ";
    std::cin >> nsym;
    std::cout << "Сдвиг (L/R): ";
    std::cin >> shiftChar;
    
    int shift = (shiftChar == 'L') ? -1 : (shiftChar == 'R') ? 1 : 0;
    machine.addRule(cs, csym, ns, nsym, shift);
    std::cout << "Правило добавлено\n";
}

void Menu::viewAllRules(const PostMachine& machine) {
    machine.printRules(std::cout);
}

void Menu::modifyTapeValue(PostMachine& machine) {
    char value;
    std::cout << "Введите новый символ: ";
    std::cin >> value;
    machine.setTapeValue(value);
}

void Menu::runFullInterpretation(PostMachine& machine, bool log) {
    machine.run(log);
    std::cout << "Интерпретация завершена\n";
}

void Menu::executeSingleStep(PostMachine& machine, bool log) {
    if (machine.step()) {
        std::cout << "Шаг выполнен\n";
        if (log) std::cout << machine << "\n";
    } else {
        std::cout << "Нет подходящего правила\n";
    }
}

void Menu::resetState(PostMachine& machine) {
    machine.reset();
    std::cout << "Состояние сброшено\n";
}

void Menu::showCurrentState(const PostMachine& machine) {
    std::cout << "Текущее состояние: " << machine << "\n";
}
