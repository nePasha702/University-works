#pragma once
#include "DocumentBase.h"

// Политика
class Policy : public DocumentBase {
private:
    std::string department; // Отдел
    std::string rules;      // Правила
    bool isActive;          // Активна ли

public:
    Policy(std::string id, std::string dept);
    bool validate() override;
    std::string generateReport() override;
    void activate();
};