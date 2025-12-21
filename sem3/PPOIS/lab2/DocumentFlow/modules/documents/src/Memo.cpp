#include "Memo.h"

Memo::Memo(std::string id, std::string to)
    : DocumentBase(id), recipient(to), isConfidential(false) {}

bool Memo::validate() {
    return !recipient.empty() && !subject.empty();
}

std::string Memo::generateReport() {
    return "Записка #" + id + " для " + recipient + (isConfidential ? " [КОНФИДЕНЦИАЛЬНО]" : "");
}

void Memo::markConfidential() {
    isConfidential = true;
}