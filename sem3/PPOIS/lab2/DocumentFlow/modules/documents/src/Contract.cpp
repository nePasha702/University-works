#include "Contract.h"
#include <ctime>

Contract::Contract(std::string id, std::string name, double sum)
    : DocumentBase(id), contractorName(name), amount(sum) {
    expirationDate = time(nullptr) + 3600 * 24 * 365; // +1 год
}

bool Contract::validate() {
    return !contractorName.empty() && amount > 0;
}

std::string Contract::generateReport() {
    return "Договор #" + id + " с " + contractorName + " на сумму " + std::to_string(amount) + " руб.";
}

void Contract::extendContract(int days) {
    expirationDate += 3600 * 24 * days;
}