#include "Specification.h"

Specification::Specification(std::string id, std::string productName)
    : DocumentBase(id), product(productName), version(1.0) {}

bool Specification::validate() {
    return !product.empty() && version > 0;
}

std::string Specification::generateReport() {
    return "Спецификация #" + id + " для " + product + " v" + std::to_string(version);
}

void Specification::updateVersion(double newVer) {
    if (newVer > version) version = newVer;
}