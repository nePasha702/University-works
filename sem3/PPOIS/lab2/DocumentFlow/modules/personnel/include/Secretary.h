#pragma once
#include "../include/Employee.h"
#include <vector>

class Secretary : public Employee {
private:
    std::vector<std::string> scheduledMeetings; // Запланированные встречи
    int documentsProcessed;      // Обработанные документы
    std::string bossId;          // ID руководителя

public:
    Secretary(std::string id, std::string name, std::string chiefId);
    void scheduleMeeting(std::string meeting);
    int getProcessedCount() const;
};