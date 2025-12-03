#ifndef MENU_H
#define MENU_H

#include "PostMachine.h"
#include <string>

class Menu {
public:
    static void displayMenu();
    static void handleUserInput(PostMachine& machine);
    static void loadProgramFromFile(PostMachine& machine);             
    static void addRuleManually(PostMachine& machine);
    static void loadTapeState(PostMachine& machine);
    static void viewAllRules(const PostMachine& machine);
    static void modifyTapeValue(PostMachine& machine);
    static void runFullInterpretation(PostMachine& machine, bool log);
    static void executeSingleStep(PostMachine& machine, bool log);
    static void resetState(PostMachine& machine);
    static void showCurrentState(const PostMachine& machine);
};

#endif
