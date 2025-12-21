#pragma once
#include "DocumentBase.h"

// Спецификация
class Specification : public DocumentBase {
private:
    std::string product;    // Продукт
    double version;         // Версия
    std::string details;    // Детали

public:
    Specification(std::string id, std::string productName);
    bool validate() override;
    std::string generateReport() override;
    void updateVersion(double newVer);
};