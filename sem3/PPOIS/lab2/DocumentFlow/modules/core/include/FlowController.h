#pragma once
#include "DocumentBase.h"

// Управление потоком документов
class FlowController {
private:
    DocumentBase* currentDoc; // Ассоциация: содержит документ
    int step;                 // Текущий шаг workflow
    bool isApproved;          // Статус утверждения

public:
    FlowController();
    void setDocument(DocumentBase* doc);
    bool moveToNextStep();
    bool approveDocument();
};