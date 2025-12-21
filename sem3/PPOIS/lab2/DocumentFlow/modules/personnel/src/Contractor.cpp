#include "Contractor.h"

Contractor::Contractor(std::string id, std::string name, std::string type)
    : Employee(id, name, "Contractor"), contractType(type), contractDuration(90), hasCompanyResources(false) {}

void Contractor::extendContract(int days) {
    contractDuration += days;
}

bool Contractor::needsResources() const {
    return hasCompanyResources;
}