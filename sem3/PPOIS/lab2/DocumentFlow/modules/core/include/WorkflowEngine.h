#pragma once
#include "DocumentBase.h"
#include "FlowController.h"

// Движок бизнес-процессов
class WorkflowEngine {
private:
    FlowController controller; // Ассоциация: использует FlowController
    int maxSteps;              // Максимальное количество шагов
    bool isActive;             // Активен ли процесс

public:
    WorkflowEngine();
    void startProcess(DocumentBase* doc);
    bool completeProcess();
};