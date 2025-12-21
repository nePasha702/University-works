#pragma once
#include "../include/Employee.h"

class Contractor : public Employee {
private:
    std::string contractType;    // Тип контракта
    int contractDuration;        // Срок контракта (дни)
    bool hasCompanyResources;    // Доступ к ресурсам

public:
    Contractor(std::string id, std::string name, std::string type);
    void extendContract(int days);
    bool needsResources() const;
};