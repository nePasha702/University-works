#include <iostream>
#include <vector>
#include <memory>
#include <fstream>
#include <ctime>
#include <unordered_map>
#include <algorithm>
#include <cctype>
#include <sys/stat.h>
#include "../modules/core/include/DocumentBase.h"
#include "../modules/core/include/FlowController.h"
#include "../modules/core/include/SecurityManager.h"
#include "../modules/core/include/AuditLogger.h"
#include "../modules/core/include/StorageManager.h"
#include "../modules/core/include/ConfigLoader.h"
#include "../modules/core/include/WorkflowEngine.h"
#include "../modules/core/include/Validator.h"
#include "../modules/core/include/Serializer.h"
#include "../modules/core/include/Deserializer.h"
#include "../modules/documents/include/Contract.h"
#include "../modules/documents/include/Invoice.h"
#include "../modules/documents/include/Report.h"
#include "../modules/documents/include/RequestForm.h"
#include "../modules/documents/include/Agreement.h"
#include "../modules/documents/include/Order.h"
#include "../modules/documents/include/Memo.h"
#include "../modules/documents/include/Letter.h"
#include "../modules/documents/include/Certificate.h"
#include "../modules/documents/include/Policy.h"
#include "../modules/documents/include/Application.h"
#include "../modules/documents/include/Resolution.h"
#include "../modules/documents/include/Protocol.h"
#include "../modules/documents/include/Specification.h"
#include "../modules/documents/include/Checklist.h"
#include "../modules/personnel/include/Employee.h"
#include "../modules/personnel/include/Manager.h"
#include "../modules/personnel/include/Director.h"
#include "../modules/personnel/include/Secretary.h"
#include "../modules/personnel/include/Auditor.h"
#include "../modules/personnel/include/HRManager.h"
#include "../modules/personnel/include/ITSupport.h"
#include "../modules/personnel/include/DepartmentHead.h"
#include "../modules/personnel/include/Contractor.h"
#include "../modules/personnel/include/ExternalUser.h"
#include "../modules/exceptions/include/DocumentException.h"
#include "../modules/exceptions/include/SecurityException.h"
#include "../modules/exceptions/include/ValidationException.h"
#include "../modules/exceptions/include/WorkflowException.h"
#include "../modules/exceptions/include/StorageException.h"
#include "../modules/exceptions/include/ConfigException.h"
#include "../modules/exceptions/include/AuditException.h"
#include "../modules/exceptions/include/SerializerException.h"
#include "../modules/exceptions/include/DeserializerException.h"
#include "../modules/exceptions/include/UserException.h"
#include "../modules/exceptions/include/NetworkException.h"
#include "../modules/exceptions/include/FileException.h"
#include "../modules/utils/include/DateUtils.h"
#include "../modules/utils/include/StringUtils.h"
#include "../modules/utils/include/FileHelper.h"

void showMainMenu();
void documentMenu(AuditLogger& logger, StorageManager& storage);
void personnelMenu();
void exceptionMenu(AuditLogger& logger, SecurityManager& security);
void utilsMenu();
void coreMenu();

int main() {
    AuditLogger globalLogger("audit.log");
    SecurityManager globalSecurity;
    StorageManager globalStorage;
    globalStorage.setStoragePath("main_storage");

    int choice;
    do {
        showMainMenu();
        std::cin >> choice;
        std::cin.ignore();

        switch (choice) {
            case 1: documentMenu(globalLogger, globalStorage); break;
            case 2: personnelMenu(); break;
            case 3: exceptionMenu(globalLogger, globalSecurity); break;
            case 4: utilsMenu(); break;
            case 5: coreMenu(); break;
            case 6: std::cout << "Выход из системы...\n"; break;
            default: std::cout << "Неверный выбор!\n";
        }
    } while (choice != 6);

    std::cout << "Система завершена. Все операции записаны в audit.log\n";
    return 0;
}

void showMainMenu() {
    std::cout << "\n=== СИСТЕМА ДОКУМЕНТООБОРОТА ===\n";
    std::cout << "1. Работа с документами\n";
    std::cout << "2. Управление персоналом\n";
    std::cout << "3. Обработка исключений\n";
    std::cout << "4. Утилиты\n";
    std::cout << "5. Системные компоненты\n";
    std::cout << "6. Выход\n";
    std::cout << "Выберите раздел: ";
}

void documentMenu(AuditLogger& logger, StorageManager& storage) {
    int choice;
    do {
        std::cout << "\n--- ДОКУМЕНТЫ ---\n";
        std::cout << "1. Создать договор\n";
        std::cout << "2. Создать счёт-фактуру\n";
        std::cout << "3. Создать отчёт\n";
        std::cout << "4. Заявка с пометкой 'срочно'\n";
        std::cout << "5. Подписать соглашение\n";
        std::cout << "6. Создать приказ с приоритетом\n";
        std::cout << "7. Конфиденциальная записка\n";
        std::cout << "8. Проверить сертификат\n";
        std::cout << "9. Назад\n";
        std::cout << "Выберите действие: ";
        std::cin >> choice;
        std::cin.ignore();

        switch (choice) {
            case 1: {
                Contract contract("CON-" + DateUtils::getCurrentDate(), "ООО 'Ромашка'", 150000.50);
                contract.extendContract(30);
                std::cout << "Договор создан: " << contract.generateReport() << "\n";
                if (storage.saveDocument(&contract)) {
                    std::cout << "Документ сохранен в хранилище\n";
                    logger.logEntry("Document saved: " + contract.getId());
                } else {
                    std::cout << "Ошибка сохранения документа\n";
                }
                break;
            }
            case 2: {
                Invoice invoice("INV-" + std::to_string(time(nullptr)));
                invoice.addItem("Ноутбук", 85000.0);
                invoice.addItem("Монитор", 25000.0);
                std::cout << invoice.generateReport() << "\n";
                logger.logEntry("Invoice created: " + invoice.getId());
                break;
            }
            case 3: {
                Report report("REP-" + DateUtils::getCurrentDate(), "Иванов И.И.");
                report.setTopic("Квартальный отчет");
                std::cout << "Отчет: " << report.generateReport() << "\n";
                logger.logEntry("Report created: " + report.getId());
                break;
            }
            case 4: {
                RequestForm request("REQ-" + std::to_string(time(nullptr)), "Петров А.С.");
                request.markAsUrgent();
                std::cout << "Заявка: " << request.generateReport() << "\n";
                logger.logEntry("Urgent request created: " + request.getId());
                break;
            }
            case 5: {
                Agreement agreement("AGR-001", "Сторона А, Сторона Б");
                agreement.sign();
                std::cout << "Соглашение подписано. Валидация: " << agreement.validate() << "\n";
                logger.logEntry("Agreement signed: " + agreement.getId());
                break;
            }
            case 6: {
                Order order("ORD-" + DateUtils::getCurrentDate(), "Директор");
                order.setPriority(8);
                std::cout << order.generateReport() << "\n";
                logger.logEntry("Order created with priority: " + order.getId());
                break;
            }
            case 7: {
                Memo memo("MEM-001", "Отдел кадров");
                memo.markConfidential();
                std::cout << memo.generateReport() << "\n";
                logger.logEntry("Confidential memo created: " + memo.getId());
                break;
            }
            case 8: {
                Certificate cert("CERT-" + DateUtils::getCurrentDate(), "Сидоров К.В.", "Пожарная безопасность");
                std::cout << cert.generateReport() << "\n";
                std::cout << "Срок действия истек: " << (cert.isExpired() ? "Да" : "Нет") << "\n";
                logger.logEntry("Certificate checked: " + cert.getId());
                break;
            }
        }
    } while (choice != 9);
}

void personnelMenu() {
    int choice;
    do {
        std::cout << "\n--- ПЕРСОНАЛ ---\n";
        std::cout << "1. Создать сотрудника\n";
        std::cout << "2. Назначить менеджера\n";
        std::cout << "3. Создать директора\n";
        std::cout << "4. Назначить секретаря\n";
        std::cout << "5. Проверить аудитора\n";
        std::cout << "6. Создать HR-менеджера\n";
        std::cout << "7. Назначить IT-поддержку\n";
        std::cout << "8. Создать руководителя отдела\n";
        std::cout << "9. Добавить подрядчика\n";
        std::cout << "10. Назад\n";
        std::cout << "Выберите действие: ";
        std::cin >> choice;
        std::cin.ignore();

        switch (choice) {
            case 1: {
                Employee emp("EMP-" + std::to_string(time(nullptr)), "Козлов С.П.", "Инженер");
                emp.setPosition("Ведущий инженер");
                std::cout << "Создан сотрудник: " << emp.getName() << " (" << emp.getId() << ")\n";
                break;
            }
            case 2: {
                Manager mgr("MGR-" + DateUtils::getCurrentDate(), "Смирнова А.Д.", 750000);
                mgr.addSubordinate("EMP-100");
                std::cout << "Менеджер может утвердить до 750 тыс.: " << mgr.canApprove(750000) << "\n";
                break;
            }
            case 3: {
                Director director("DIR-" + DateUtils::getCurrentDate(), "Петров В.В.", "IT");
                director.approveStrategicPlan();
                std::cout << "Директор утвердил стратегический план для отдела: " << director.getDivision() << "\n";
                break;
            }
            case 4: {
                Secretary sec("SEC-001", "Козлова М.И.", "MGR-200");
                sec.scheduleMeeting("Совещание по бюджету");
                std::cout << "Секретарь запланировал встречу. Обработано документов: " << sec.getProcessedCount() << "\n";
                break;
            }
            case 5: {
                Auditor auditor("AUD-" + DateUtils::getCurrentDate(), "Федоров Р.Т.", "Финансы");
                auditor.reportViolation();
                std::cout << "Найдено нарушений: 1. Внешний аудитор: " << (auditor.isExternal() ? "Да" : "Нет") << "\n";
                break;
            }
            case 6: {
                HRManager hr("HR-" + DateUtils::getCurrentDate(), "Волкова Е.С.");
                hr.postVacancy("Программист");
                std::cout << "Вакансия создана. Бюджет на найм: " << hr.getBudget() << " руб.\n";
                break;
            }
            case 7: {
                ITSupport it("IT-" + DateUtils::getCurrentDate(), "Гусев Д.А.");
                it.resolveTicket();
                std::cout << "Обращение решено. Доступ к серверам: " << (it.checkAccess() ? "Да" : "Нет") << "\n";
                break;
            }
            case 8: {
                DepartmentHead head("DH-" + DateUtils::getCurrentDate(), "Николаев А.К.", "Исследования", 2000000.0);
                head.allocateBudget(500000.0);
                std::cout << "Бюджет выделен для отдела: " << head.getDepartment() << "\n";
                break;
            }
            case 9: {
                Contractor contractor("CONTR-" + DateUtils::getCurrentDate(), "Иванов П.С.", "Проект X");
                contractor.extendContract(45);
                std::cout << "Контракт продлен на 45 дней. Нужны ресурсы компании: " << (contractor.needsResources() ? "Да" : "Нет") << "\n";
                break;
            }
        }
    } while (choice != 10);
}

void exceptionMenu(AuditLogger& logger, SecurityManager& security) {
    int choice;
    do {
        std::cout << "\n--- ИСКЛЮЧЕНИЯ ---\n";
        std::cout << "1. DocumentException\n";
        std::cout << "2. SecurityException\n";
        std::cout << "3. ValidationException\n";
        std::cout << "4. WorkflowException\n";
        std::cout << "5. StorageException\n";
        std::cout << "6. Назад\n";
        std::cout << "Выберите исключение для демонстрации: ";
        std::cin >> choice;
        std::cin.ignore();

        try {
            switch (choice) {
                case 1:
                    throw DocumentException("Документ не найден", 404, "DOC-999");
                case 2:
                    throw SecurityException("user_blocked", "DELETE_DOCUMENT");
                case 3:
                    throw ValidationException("email", "invalid_format");
                case 4:
                    throw WorkflowException("Утверждение договора", 3);
                case 5:
                    throw StorageException("/storage", 512);
            }
        } catch (const DocumentException& e) {
            std::cerr << "[DocumentException] " << e.what() 
                      << " (Документ: " << e.getDocumentId() << ")\n";
            logger.logEntry("DocumentException: " + std::string(e.what()));
        } catch (const SecurityException& e) {
            std::cerr << "[SecurityException] " << e.what() << "\n";
            logger.logEntry("SecurityException: " + std::string(e.what()));
            security.lockSystem();
        } catch (const ValidationException& e) {
            std::cerr << "[ValidationException] " << e.what() << "\n";
            logger.logEntry("ValidationException: " + std::string(e.what()));
        } catch (const WorkflowException& e) {
            std::cerr << "[WorkflowException] " << e.what() << "\n";
            logger.logEntry("WorkflowException: " + std::string(e.what()));
        } catch (const StorageException& e) {
            std::cerr << "[StorageException] " << e.what() << "\n";
            logger.logEntry("StorageException: " + std::string(e.what()));
        } catch (...) {
            std::cerr << "Неизвестное исключение\n";
            logger.logEntry("Unknown exception caught");
        }
    } while (choice != 6);
}

void utilsMenu() {
    int choice;
    do {
        std::cout << "\n--- УТИЛИТЫ ---\n";
        std::cout << "1. Получить текущую дату\n";
        std::cout << "2. Преобразовать строку в верхний регистр\n";
        std::cout << "3. Проверить существование файла\n";
        std::cout << "4. Назад\n";
        std::cout << "Выберите утилиту: ";
        std::cin >> choice;
        std::cin.ignore();

        switch (choice) {
            case 1: {
                std::cout << "Текущая дата: " << DateUtils::getCurrentDate() << "\n";
                break;
            }
            case 2: {
                std::string input;
                std::cout << "Введите текст: ";
                std::getline(std::cin, input);
                std::cout << "Результат: " << StringUtils::toUpperCase(input) << "\n";
                std::cout << "Без пробелов: '" << StringUtils::trim(input) << "'\n";
                break;
            }
            case 3: {
                std::string path;
                std::cout << "Введите путь к файлу: ";
                std::getline(std::cin, path);
                if (FileHelper::fileExists(path)) {
                    std::cout << "Файл существует!\n";
                    auto lines = FileHelper::readFileLines(path);
                    std::cout << "Количество строк: " << lines.size() << "\n";
                } else {
                    std::cout << "Файл не найден\n";
                }
                break;
            }
        }
    } while (choice != 4);
}

void coreMenu() {
    int choice;
    do {
        std::cout << "\n--- СИСТЕМНЫЕ КОМПОНЕНТЫ ---\n";
        std::cout << "1. Загрузить конфигурацию\n";
        std::cout << "2. Проверить валидацию\n";
        std::cout << "3. Сериализация/Десериализация\n";
        std::cout << "4. Назад\n";
        std::cout << "Выберите действие: ";
        std::cin >> choice;
        std::cin.ignore();

        switch (choice) {
            case 1: {
                ConfigLoader config("config.txt");
                if (config.load()) {
                    std::cout << "Значение max_documents: " << config.getValue("max_documents") << "\n";
                } else {
                    std::cout << "Ошибка загрузки конфигурации\n";
                }
                break;
            }
            case 2: {
                Validator validator;
                std::cout << "Валидация 'ok': " << validator.validateString("ok") << "\n";
                std::cout << "Валидация '': " << validator.validateString("") 
                          << " (Ошибка: " << validator.getLastError() << ")\n";
                break;
            }
            case 3: {
                Serializer serializer;
                Deserializer deserializer;
                std::string data = "тестовые данные";
                std::string serialized = serializer.serialize(data);
                std::cout << "Сериализовано: " << serialized << "\n";
                std::cout << "Десериализовано: " << deserializer.deserialize(serialized) << "\n";
                break;
            }
        }
    } while (choice != 4);
}
