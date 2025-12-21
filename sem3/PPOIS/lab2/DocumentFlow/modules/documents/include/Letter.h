#pragma once
#include "DocumentBase.h"

// Письмо
class Letter : public DocumentBase {
private:
    std::string sender;     // Отправитель
    std::string receiver;   // Получатель
    std::string body;       // Текст письма

public:
    Letter(std::string id, std::string from, std::string to);
    bool validate() override;
    std::string generateReport() override;
    void setBody(std::string text);
};