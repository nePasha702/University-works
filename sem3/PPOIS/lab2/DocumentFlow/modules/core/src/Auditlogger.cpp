#include "AuditLogger.h"
#include <iostream>

AuditLogger::AuditLogger(std::string filename) 
    : logFile(filename), isEnabled(true), entryCount(0) {
    std::ofstream file(logFile);
}

void AuditLogger::logEntry(std::string message) {
    if (!isEnabled) return;
    std::ofstream file(logFile, std::ios::app);
    file << message << "\n";
    entryCount++;
}

int AuditLogger::getEntryCount() const {
    return entryCount;
}
