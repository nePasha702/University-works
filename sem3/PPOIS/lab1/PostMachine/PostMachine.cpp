#include "PostMachine.h"

void PostMachine::loadFromStream(std::istream& is) {
    std::string line;
    while (std::getline(is, line)) {
        if (line.empty()) continue;
        
        std::istringstream iss(line);
        int cs, ns;
        char csym, nsym;
        char shiftChar;
        
        if (iss >> cs >> csym >> ns >> nsym >> shiftChar) {
            int shift = 0;
            if (shiftChar == 'L') shift = -1;
            else if (shiftChar == 'R') shift = 1;
            commands.emplace_back(cs, csym, ns, nsym, shift);
        }
    }
}

void PostMachine::loadTapeState(std::istream& is) {
    tape.loadFromStream(is);
}

void PostMachine::addRule(int cs, char csym, int ns, char nsym, int shift) {
    commands.emplace_back(cs, csym, ns, nsym, shift);
}

void PostMachine::setTapeValue(char value) {
    tape.set(value);
}

bool PostMachine::step() {
    char currentSymbol = tape.get();
    for (const auto& rule : commands) {
        if (rule.getCurrentState() == currentState && 
            rule.getCurrentState() == currentSymbol) {
            tape.set(rule.getNewSymbol());
            currentState = rule.getNextState();
            if (rule.getShift() == -1) tape.moveLeft();
            else if (rule.getShift() == 1) tape.moveRight();
            return true;
        }
    }
    return false;
}

void PostMachine::run(bool log) {
    int stepCount = 0;
    while (step()) {
        stepCount++;
        if (log) {
            std::cout << "Step " << stepCount << ": " << *this << "\n";
        }
    }
    if (log) {
        std::cout << "Выполнено " << stepCount << " шагов\n";
    }
}

void PostMachine::reset() {
    currentState = 1;
    tape.reset();
}

std::ostream& operator<<(std::ostream& os, const PostMachine& pm) {
    os << "State=" << pm.currentState << ", Tape=" << pm.tape;
    return os;
}

// Для тестов 
void PostMachine::printRules(std::ostream& os) const {
    if (commands.empty()) {
        os << "No rules defined\n";
        return;
    }
    for (const auto& cmd : commands) {
        os << cmd.getCurrentState() << " " 
           << cmd.getCurrentSymbol() << " " 
           << cmd.getNextState() << " " 
           << cmd.getNewSymbol() << " " 
           << (cmd.getShift() == -1 ? "L" : cmd.getShift() == 1 ? "R" : "-") 
           << "\n";
    }
}

void PostMachine::loadTapeFromString(const std::string& state) {
    tape.reset();
    for (size_t i = 0; i < state.length(); ++i) {
        if (i > 0) tape.moveRight();
        tape.set(state[i]);
    }
    while (tape.get() != ' ') tape.moveLeft();
    tape.moveRight();
}
