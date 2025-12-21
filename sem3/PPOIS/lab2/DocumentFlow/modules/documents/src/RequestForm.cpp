#include "RequestForm.h"

RequestForm::RequestForm(std::string id, std::string requesterName)
    : DocumentBase(id), requester(requesterName), isUrgent(false) {}

bool RequestForm::validate() {
    return !requester.empty() && !purpose.empty();
}

std::string RequestForm::generateReport() {
    return "Заявка #" + id + " от " + requester + (isUrgent ? " [СРОЧНО]" : "");
}

void RequestForm::markAsUrgent() {
    isUrgent = true;
}