#include "../include/ITSupport.h"

ITSupport::ITSupport(std::string id, std::string name)
    : Employee(id, name, "IT Support"), ticketSystem("Jira"), unresolvedTickets(5), hasServerAccess(true) {}

void ITSupport::resolveTicket() {
    if (unresolvedTickets > 0) unresolvedTickets--;
}

bool ITSupport::checkAccess() const {
    return hasServerAccess;
}