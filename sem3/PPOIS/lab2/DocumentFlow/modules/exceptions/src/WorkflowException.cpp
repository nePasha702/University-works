#include "WorkflowException.h"

WorkflowException::WorkflowException(const std::string& process, int step)
    : processName(process) {
    message = "Ошибка в процессе " + process + " на шаге " + std::to_string(step);
}

const char* WorkflowException::what() const noexcept {
    return message.c_str();
}