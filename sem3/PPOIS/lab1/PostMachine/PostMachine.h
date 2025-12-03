#ifndef POSTMACHINE_H
#define POSTMACHINE_H

#include "PostMachineTape.h"
#include "PostMachineCommand.h"
#include <vector>
#include <sstream>
#include <string>

class PostMachine {
private:
    int currentState;
    Tape tape;
    std::vector<PostMachineCommand> commands;

public:
    PostMachine() : currentState(1) {}
    
    // Методы для тестов
    int getCurrentState() const { return currentState; }
    char getTapeSymbol() const { return tape.get(); }
    void moveTapeLeft() { tape.moveLeft(); }
    void moveTapeRight() { tape.moveRight(); }
    void loadTapeFromString(const std::string& state);
    void printRules(std::ostream& os) const;
    
    // Основные методы
    void loadFromStream(std::istream& is);
    void loadTapeState(std::istream& is);
    void addRule(int cs, char csym, int ns, char nsym, int shift);
    void setTapeValue(char value);
    bool step();
    void run(bool log = false);
    void reset();
    
    friend std::ostream& operator<<(std::ostream& os, const PostMachine& pm);
};

#endif
