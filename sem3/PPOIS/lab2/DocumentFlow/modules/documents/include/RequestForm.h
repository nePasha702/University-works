#pragma once
#include "DocumentBase.h"

// Заявка
class RequestForm : public DocumentBase {
private:
    std::string requester;  // Заявитель
    std::string purpose;    // Цель заявки
    bool isUrgent;          // Срочность

public:
    RequestForm(std::string id, std::string requesterName);
    bool validate() override;
    std::string generateReport() override;
    void markAsUrgent();
};