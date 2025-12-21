#include "Manager.h"

Manager::Manager(std::string id, std::string name, int limit)
    : Employee(id, name, "Manager"), approvalLimit(limit), hasSigningAuthority(true) {}

void Manager::addSubordinate(std::string empId) {
    departmentEmployees.push_back(empId);
}

bool Manager::canApprove(double amount) const {
    return amount <= approvalLimit;
}