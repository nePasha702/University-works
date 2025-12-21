#pragma once
#include "../include/Employee.h"
#include <vector>

class Manager : public Employee {
private:
    std::vector<std::string> departmentEmployees; // Сотрудники отдела
    int approvalLimit;            // Лимит утверждения
    bool hasSigningAuthority;     // Право подписи

public:
    Manager(std::string id, std::string name, int limit);
    void addSubordinate(std::string empId);
    bool canApprove(double amount) const;
};