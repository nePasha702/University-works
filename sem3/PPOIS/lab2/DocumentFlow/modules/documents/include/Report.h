#pragma once
#include "DocumentBase.h"

// Отчёт
class Report : public DocumentBase {
private:
    std::string author;     // Автор отчёта
    int pages;              // Количество страниц
    std::string topic;      // Тема отчёта

public:
    Report(std::string id, std::string authorName);
    bool validate() override;
    std::string generateReport() override;
    void setTopic(std::string newTopic);
};