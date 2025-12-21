#pragma once
#include "DocumentBase.h"

// Сертификат
class Certificate : public DocumentBase {
private:
    std::string holder;     // Владелец
    std::string type;       // Тип сертификата
    time_t issueDate;       // Дата выдачи

public:
    Certificate(std::string id, std::string owner, std::string certType);
    bool validate() override;
    std::string generateReport() override;
    bool isExpired();
};