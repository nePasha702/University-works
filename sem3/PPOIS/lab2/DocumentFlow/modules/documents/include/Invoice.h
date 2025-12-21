#pragma once
#include "DocumentBase.h"
#include <vector>

// Счёт-фактура
class Invoice : public DocumentBase {
private:
    std::vector<std::string> items; // Список товаров
    double total;                   // Итоговая сумма
    bool isPaid;                    // Оплачено ли

public:
    Invoice(std::string id);
    bool validate() override;
    std::string generateReport() override;
    void addItem(std::string item, double price);
};