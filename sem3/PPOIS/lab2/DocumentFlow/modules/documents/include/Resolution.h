#pragma once
#include "DocumentBase.h"

// Решение
class Resolution : public DocumentBase {
private:
    std::string decider;    // Принявший решение
    std::string decision;   // Решение
    bool isFinal;           // Окончательное

public:
    Resolution(std::string id, std::string deciderName);
    bool validate() override;
    std::string generateReport() override;
    void finalize();
};