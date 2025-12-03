#include "PostMachineTape.h"

Tape::Tape() : position(0) {
    cells.push_back(' ');
}

void Tape::set(char value) {
    cells[position] = value;
}

char Tape::get() const {
    return cells[position];
}

void Tape::moveLeft() {
    if (position == 0) {
        cells.insert(cells.begin(), ' ');
    } else {
        position--;
    }
}

void Tape::moveRight() {
    if (position == static_cast<int>(cells.size()) - 1) {
        cells.push_back(' ');
        position++;
    } else {
        position++;
    }
}

void Tape::loadFromStream(std::istream& is) {
    std::string line;
    std::getline(is, line);
    cells.clear();
    for (char c : line) {
        cells.push_back(c);
    }
    position = 0;
}

void Tape::reset() {
    cells = std::vector<char>(1, ' ');
    position = 0;
}

std::ostream& operator<<(std::ostream& os, const Tape& tape) {
    for (size_t i = 0; i < tape.cells.size(); ++i) {
        if (i == static_cast<size_t>(tape.position)) os << '[';
        os << tape.cells[i];
        if (i == static_cast<size_t>(tape.position)) os << ']';
    }
    return os;
}
