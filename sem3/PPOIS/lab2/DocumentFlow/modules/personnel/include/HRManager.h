#pragma once
#include "../include/Employee.h"
#include <vector>

class HRManager : public Employee {
private:
    std::vector<std::string> vacantPositions; // Вакансии
    int recruitmentBudget;      // Бюджет на найм
    bool trainingCoordinator;   // Координатор обучения

public:
    HRManager(std::string id, std::string name);
    void postVacancy(std::string position);
    int getBudget() const;
};