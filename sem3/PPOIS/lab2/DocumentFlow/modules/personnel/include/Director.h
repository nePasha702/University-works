#pragma once
#include "../include/Employee.h"

class Director : public Employee {
private:
    std::string companyDivision;  // Подразделение компании
    int strategicApprovalLevel;   // Уровень стратегических решений
    bool isBoardMember;           // Член совета директоров

public:
    Director(std::string id, std::string name, std::string division);
    std::string getDivision() const;
    void approveStrategicPlan();
};