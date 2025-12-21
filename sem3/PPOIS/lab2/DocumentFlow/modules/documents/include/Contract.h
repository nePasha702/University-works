#pragma once
#include "DocumentBase.h"

// Договор
class Contract : public DocumentBase {
private:
    std::string contractorName; // Имя контрагента
    double amount;              // Сумма договора
    time_t expirationDate;      // Дата окончания

public:
    Contract(std::string id, std::string name, double sum);
    bool validate() override;
    std::string generateReport() override;
    void extendContract(int days);
};