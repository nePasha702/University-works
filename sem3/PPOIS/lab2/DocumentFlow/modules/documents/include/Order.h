#pragma once
#include "DocumentBase.h"

// Приказ
class Order : public DocumentBase {
private:
    std::string issuer;     // Издатель приказа
    std::string content;    // Содержание приказа
    int priority;           // Приоритет (1-10)

public:
    Order(std::string id, std::string issuerName);
    bool validate() override;
    std::string generateReport() override;
    void setPriority(int level);
};