#pragma once
#include "DocumentBase.h"

// Заявление
class Application : public DocumentBase {
private:
    std::string applicant;  // Заявитель
    std::string reason;     // Причина
    int attachmentCount;    // Количество вложений

public:
    Application(std::string id, std::string name);
    bool validate() override;
    std::string generateReport() override;
    void addAttachment();
};