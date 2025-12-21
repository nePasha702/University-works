#include "ExternalUser.h"

ExternalUser::ExternalUser(std::string id, std::string name, std::string org)
    : Contractor(id, name, "External"), organization(org), dataAccessLevel(false), supportPriority(3) {}

void ExternalUser::grantDataAccess() {
    dataAccessLevel = true;
}

int ExternalUser::getPriority() const {
    return supportPriority;
}