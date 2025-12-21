#include "Employee.h"

Employee::Employee(std::string id, std::string name, std::string pos)
    : employeeId(id), fullName(name), position(pos) {}

std::string Employee::getId() const {
    return employeeId;
}

std::string Employee::getName() const {
    return fullName;
}

void Employee::setPosition(std::string newPos) {
    position = newPos;
}