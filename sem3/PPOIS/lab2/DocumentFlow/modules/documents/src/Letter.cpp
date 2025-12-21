#include "Letter.h"

Letter::Letter(std::string id, std::string from, std::string to)
    : DocumentBase(id), sender(from), receiver(to) {}

bool Letter::validate() {
    return !sender.empty() && !receiver.empty() && !body.empty();
}

std::string Letter::generateReport() {
    return "Письмо #" + id + " от " + sender + " для " + receiver;
}

void Letter::setBody(std::string text) {
    body = text;
}