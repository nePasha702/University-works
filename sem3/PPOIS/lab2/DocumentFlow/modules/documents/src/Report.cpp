#include "Report.h"

Report::Report(std::string id, std::string authorName)
    : DocumentBase(id), author(authorName), pages(1), topic("Без темы") {}

bool Report::validate() {
    return !author.empty() && pages > 0;
}

std::string Report::generateReport() {
    return "Отчёт #" + id + " от " + author + " по теме: " + topic;
}

void Report::setTopic(std::string newTopic) {
    topic = newTopic;
}