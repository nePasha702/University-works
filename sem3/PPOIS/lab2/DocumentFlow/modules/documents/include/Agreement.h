#pragma once
#include "DocumentBase.h"

// Соглашение
class Agreement : public DocumentBase {
private:
    std::string parties;    // Стороны соглашения
    time_t signingDate;     // Дата подписания
    bool isVerbal;          // Устное соглашение

public:
    Agreement(std::string id, std::string participants);
    bool validate() override;
    std::string generateReport() override;
    void sign();
};
