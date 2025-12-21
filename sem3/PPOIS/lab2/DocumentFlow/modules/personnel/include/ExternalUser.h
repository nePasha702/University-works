#pragma once
#include "../include/Contractor.h"

class ExternalUser : public Contractor {
private:
    std::string organization;    // Организация
    bool dataAccessLevel;         // Уровень доступа к данным
    int supportPriority;          // Приоритет поддержки

public:
    ExternalUser(std::string id, std::string name, std::string org);
    void grantDataAccess();
    int getPriority() const;
};