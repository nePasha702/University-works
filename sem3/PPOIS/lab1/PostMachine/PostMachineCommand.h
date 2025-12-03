#ifndef POSTMACHINE_COMMAND_H
#define POSTMACHINE_COMMAND_H

class PostMachineCommand {
private:
    int currentState;
    char currentSymbol;
    int nextState;
    char newSymbol;
    int shift;

public:
    PostMachineCommand(int cs, char csym, int ns, char nsym, int sh);
    
    int getCurrentState() const;
    char getCurrentSymbol() const;
    int getNextState() const;
    char getNewSymbol() const;
    int getShift() const;
    
    bool matches(int state, char symbol) const;
};

#endif
