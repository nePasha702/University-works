#include "HRManager.h"

HRManager::HRManager(std::string id, std::string name)
    : Employee(id, name, "HR Manager"), recruitmentBudget(100000), trainingCoordinator(true) {}

void HRManager::postVacancy(std::string position) {
    vacantPositions.push_back(position);
}

int HRManager::getBudget() const {
    return recruitmentBudget;
}