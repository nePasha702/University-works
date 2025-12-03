#ifndef POSTMACHINE_TAPE_H
#define POSTMACHINE_TAPE_H

#include <vector>
#include <iostream>

class Tape {
private:
    std::vector<char> cells;
    int position;

public:
    Tape();
    void set(char value);
    char get() const;
    void moveLeft();
    void moveRight();
    void loadFromStream(std::istream& is);
    void reset();
    friend std::ostream& operator<<(std::ostream& os, const Tape& tape);
};

#endif
