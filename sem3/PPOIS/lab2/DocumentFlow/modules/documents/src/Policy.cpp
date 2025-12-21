#include "Policy.h"

Policy::Policy(std::string id, std::string dept)
    : DocumentBase(id), department(dept), isActive(false) {}

bool Policy::validate() {
    return !department.empty() && !rules.empty();
}

std::string Policy::generateReport() {
    return "Политика #" + id + " для отдела " + department + (isActive ? "" : " [НЕАКТИВНА]");
}

void Policy::activate() {
    isActive = true;
}