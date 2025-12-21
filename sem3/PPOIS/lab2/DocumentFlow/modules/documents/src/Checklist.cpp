#include "Checklist.h"

Checklist::Checklist(std::string id, std::string name)
    : DocumentBase(id), title(name), completedCount(0) {}

bool Checklist::validate() {
    return !title.empty() && !items.empty();
}

std::string Checklist::generateReport() {
    return "Чек-лист #" + id + " \"" + title + "\" выполнено: " + std::to_string(completedCount) + "/" + std::to_string(items.size());
}

void Checklist::addItem() {
    items.push_back(false);
}

void Checklist::markItemCompleted(int index) {
    if (index >= 0 && index < items.size() && !items[index]) {
        items[index] = true;
        completedCount++;
    }
}