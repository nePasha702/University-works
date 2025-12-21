#include "Protocol.h"

Protocol::Protocol(std::string id, std::string chair)
    : DocumentBase(id), chairperson(chair), attendeesCount(0) {}

bool Protocol::validate() {
    return !chairperson.empty() && attendeesCount > 0;
}

std::string Protocol::generateReport() {
    return "Протокол #" + id + " от " + chairperson + ", участников: " + std::to_string(attendeesCount);
}

void Protocol::addAttendee() {
    attendeesCount++;
}