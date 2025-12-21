#pragma once
#include "DocumentBase.h"

// Служебная записка
class Memo : public DocumentBase {
private:
    std::string recipient;  // Получатель
    std::string subject;    // Тема
    bool isConfidential;    // Конфиденциально

public:
    Memo(std::string id, std::string to);
    bool validate() override;
    std::string generateReport() override;
    void markConfidential();
};