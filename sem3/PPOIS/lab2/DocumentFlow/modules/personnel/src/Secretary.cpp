#include "Secretary.h"

Secretary::Secretary(std::string id, std::string name, std::string chiefId)
    : Employee(id, name, "Secretary"), bossId(chiefId), documentsProcessed(0) {}

void Secretary::scheduleMeeting(std::string meeting) {
    scheduledMeetings.push_back(meeting);
}

int Secretary::getProcessedCount() const {
    return documentsProcessed;
}