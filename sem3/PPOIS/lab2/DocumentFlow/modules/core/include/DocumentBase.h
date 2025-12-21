#pragma once
#include <string>
#include <ctime>

class DocumentBase {
protected:
    std::string id;         
    time_t creationTime;    
    int status;             

public:
    DocumentBase(std::string docId);
    virtual ~DocumentBase() = default;

    virtual bool validate() = 0;
    virtual std::string generateReport() = 0;

    std::string getId() const;
    void setStatus(int newStatus);
};
