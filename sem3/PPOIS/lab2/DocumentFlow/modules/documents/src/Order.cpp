#include "Order.h"

Order::Order(std::string id, std::string issuerName)
    : DocumentBase(id), issuer(issuerName), priority(1) {}

bool Order::validate() {
    return !issuer.empty() && priority >= 1 && priority <= 10;
}

std::string Order::generateReport() {
    return "Приказ #" + id + " от " + issuer + ", приоритет: " + std::to_string(priority);
}

void Order::setPriority(int level) {
    if (level >= 1 && level <= 10) priority = level;
}