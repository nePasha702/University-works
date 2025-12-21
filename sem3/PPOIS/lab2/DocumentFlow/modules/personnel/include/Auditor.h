#pragma once
#include "../include/Employee.h"

class Auditor : public Employee {
private:
    std::string auditArea;       // Зона аудита
    int violationsFound;         // Найдено нарушений
    bool external;               // Внешний аудитор

public:
    Auditor(std::string id, std::string name, std::string area);
    void reportViolation();
    bool isExternal() const;
};
