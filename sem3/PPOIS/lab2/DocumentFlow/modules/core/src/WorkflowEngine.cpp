#include "WorkflowEngine.h"

WorkflowEngine::WorkflowEngine() 
    : maxSteps(5), isActive(false) {}

void WorkflowEngine::startProcess(DocumentBase* doc) {
    controller.setDocument(doc);
    isActive = true;
}

bool WorkflowEngine::completeProcess() {
    if (!isActive) return false;
    for (int i = 0; i < maxSteps; i++) {
        controller.moveToNextStep();
    }
    return true;
}