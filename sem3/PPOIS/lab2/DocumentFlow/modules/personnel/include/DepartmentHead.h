#pragma once
#include "../include/Manager.h"

class DepartmentHead : public Manager {
private:
    std::string departmentName;  // Название отдела
    double budget;               // Бюджет отдела
    bool profitCenter;           // Центр прибыли

public:
    DepartmentHead(std::string id, std::string name, std::string dept, double budg);
    std::string getDepartment() const;
    void allocateBudget(double amount);
};