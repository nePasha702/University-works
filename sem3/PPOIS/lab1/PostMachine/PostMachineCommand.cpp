#include "PostMachineCommand.h"

PostMachineCommand::PostMachineCommand(int cs, char csym, int ns, char nsym, int sh)
    : currentState(cs), currentSymbol(csym), 
      nextState(ns), newSymbol(nsym), shift(sh) {}

int PostMachineCommand::getCurrentState() const {
    return currentState;
}

char PostMachineCommand::getCurrentSymbol() const {
    return currentSymbol;
}

int PostMachineCommand::getNextState() const {
    return nextState;
}

char PostMachineCommand::getNewSymbol() const {
    return newSymbol;
}

int PostMachineCommand::getShift() const {
    return shift;
}

bool PostMachineCommand::matches(int state, char symbol) const {
    return (currentState == state) && (currentSymbol == symbol);
}
