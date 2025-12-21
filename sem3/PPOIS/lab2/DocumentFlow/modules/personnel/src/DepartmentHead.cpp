#include "DepartmentHead.h"

DepartmentHead::DepartmentHead(std::string id, std::string name, std::string dept, double budg)
    : Manager(id, name, 500000), departmentName(dept), budget(budg), profitCenter(true) {}

std::string DepartmentHead::getDepartment() const {
    return departmentName;
}

void DepartmentHead::allocateBudget(double amount) {
    if (amount <= budget) budget -= amount;
}