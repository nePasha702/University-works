#pragma once
#include "DocumentBase.h"
#include <vector>

// Чек-лист
class Checklist : public DocumentBase {
private:
    std::vector<bool> items; // Статусы пунктов
    std::string title;       // Название
    int completedCount;      // Количество выполненных

public:
    Checklist(std::string id, std::string name);
    bool validate() override;
    std::string generateReport() override;
    void addItem();
    void markItemCompleted(int index);
};