#pragma once
#include "../include/Employee.h"

class ITSupport : public Employee {
private:
    std::string ticketSystem;    // Система тикетов
    int unresolvedTickets;       // Нерешённые обращения
    bool hasServerAccess;        // Доступ к серверам

public:
    ITSupport(std::string id, std::string name);
    void resolveTicket();
    bool checkAccess() const;
};