#include "Invoice.h"

Invoice::Invoice(std::string id)
    : DocumentBase(id), total(0.0), isPaid(false) {}

bool Invoice::validate() {
    return !items.empty() && total > 0;
}

std::string Invoice::generateReport() {
    return "Счёт #" + id + ", товаров: " + std::to_string(items.size()) + ", сумма: " + std::to_string(total);
}

void Invoice::addItem(std::string item, double price) {
    items.push_back(item + ": " + std::to_string(price));
    total += price;
}