#include "Resolution.h"

Resolution::Resolution(std::string id, std::string deciderName)
    : DocumentBase(id), decider(deciderName), isFinal(false) {}

bool Resolution::validate() {
    return !decider.empty() && !decision.empty();
}

std::string Resolution::generateReport() {
    return "Решение #" + id + " от " + decider + (isFinal ? " [ОКОНЧАТЕЛЬНОЕ]" : "");
}

void Resolution::finalize() {
    isFinal = true;
}