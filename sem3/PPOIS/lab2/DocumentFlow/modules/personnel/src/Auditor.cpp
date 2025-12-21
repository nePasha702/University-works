#include "Auditor.h"

Auditor::Auditor(std::string id, std::string name, std::string area)
    : Employee(id, name, "Auditor"), auditArea(area), violationsFound(0), external(false) {}

void Auditor::reportViolation() {
    violationsFound++;
}

bool Auditor::isExternal() const {
    return external;
}
