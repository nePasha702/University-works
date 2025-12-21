#include "FlowController.h"

FlowController::FlowController() 
    : currentDoc(nullptr), step(0), isApproved(false) {}

void FlowController::setDocument(DocumentBase* doc) {
    currentDoc = doc;
}

bool FlowController::moveToNextStep() {
    if (currentDoc == nullptr) return false;
    step++;
    return true;
}

bool FlowController::approveDocument() {
    if (currentDoc == nullptr) return false;
    currentDoc->setStatus(2);
    isApproved = true;
    return true;
}