#pragma once
#include <string>
#include <fstream>

class AuditLogger {
private:
    std::string logFile;    
    bool isEnabled;         
    int entryCount;         
public:
    AuditLogger(std::string filename);
    void logEntry(std::string message);
    int getEntryCount() const;
};
