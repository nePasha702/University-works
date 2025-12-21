#pragma once
#include <string>

class Employee {
protected:
    std::string employeeId;   // ID сотрудника
    std::string fullName;     // ФИО
    std::string position;     // Должность

public:
    Employee(std::string id, std::string name, std::string pos);
    std::string getId() const;
    std::string getName() const;
    void setPosition(std::string newPos);
};