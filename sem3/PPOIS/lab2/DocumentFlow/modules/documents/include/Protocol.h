#pragma once
#include "DocumentBase.h"

// Протокол
class Protocol : public DocumentBase {
private:
    std::string chairperson; // Председатель
    int attendeesCount;      // Количество участников
    std::string meetingDate;// Дата встречи

public:
    Protocol(std::string id, std::string chair);
    bool validate() override;
    std::string generateReport() override;
    void addAttendee();
};