#include "include/Menu.h"
#include <iostream>

int main() {
    PostMachine machine;
    std::cout << "Задание: Машина Поста\n";
    Menu::handleUserInput(machine);
    std::cout << "Программа завершена\n";
    return 0;
}
