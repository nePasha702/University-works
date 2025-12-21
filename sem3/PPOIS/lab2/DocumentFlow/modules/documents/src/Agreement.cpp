#include "Agreement.h"
#include <ctime>

Agreement::Agreement(std::string id, std::string participants)
    : DocumentBase(id), parties(participants), isVerbal(true) {
    signingDate = time(nullptr);
}

bool Agreement::validate() {
    return !parties.empty() && !isVerbal;
}

std::string Agreement::generateReport() {
    return "Соглашение #" + id + " между " + parties;
}

void Agreement::sign() {
    isVerbal = false;
}
