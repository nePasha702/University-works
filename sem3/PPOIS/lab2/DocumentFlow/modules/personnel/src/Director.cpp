#include "Director.h"

Director::Director(std::string id, std::string name, std::string division)
    : Employee(id, name, "Director"), companyDivision(division), strategicApprovalLevel(5), isBoardMember(true) {}

std::string Director::getDivision() const {
    return companyDivision;
}

void Director::approveStrategicPlan() {
    strategicApprovalLevel--;
}