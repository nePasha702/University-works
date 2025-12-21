#include "DocumentBase.h"

DocumentBase::DocumentBase(std::string docId) 
    : id(docId), creationTime(time(nullptr)), status(0) {}

std::string DocumentBase::getId() const {
    return id;
}

void DocumentBase::setStatus(int newStatus) {
    status = newStatus;
}