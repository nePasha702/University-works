#include "Application.h"

Application::Application(std::string id, std::string name)
    : DocumentBase(id), applicant(name), attachmentCount(0) {}

bool Application::validate() {
    return !applicant.empty() && attachmentCount > 0;
}

std::string Application::generateReport() {
    return "Заявление #" + id + " от " + applicant + ", вложений: " + std::to_string(attachmentCount);
}

void Application::addAttachment() {
    attachmentCount++;
}