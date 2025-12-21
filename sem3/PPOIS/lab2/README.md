# Лабораторная работа №2 по дисциплине "Проектирование программного обеспечения интеллектуальных систем"

## Тема: Документооборот

DocumentBase 3 2  
FlowController 3 2 → DocumentBase, SecurityManager, AuditLogger  
SecurityManager 3 3 → String, Vector, Boolean  
AuditLogger 3 2  
StorageManager 3 2 → DocumentBase  
ConfigLoader 3 2  
WorkflowEngine 3 2 → FlowController, DocumentBase  
Validator 3 2  
Serializer 3 2  
Deserializer 3 2  

Contract 3 3 → DocumentBase  
Invoice 3 3 → DocumentBase  
Report 3 3 → DocumentBase  
RequestForm 3 3 → DocumentBase  
Agreement 3 3 → DocumentBase  
Order 3 3 → DocumentBase  
Memo 3 3 → DocumentBase  
Letter 3 3 → DocumentBase  
Certificate 3 3 → DocumentBase  
Policy 3 3 → DocumentBase  
Application 3 3 → DocumentBase  
Resolution 3 3 → DocumentBase  
Protocol 3 3 → DocumentBase  
Specification 3 3 → DocumentBase  
Checklist 3 3 → DocumentBase  

DocumentException 3 2 →
SecurityException 3 2 →
ValidationException 3 2 →
WorkflowException 3 2 →
StorageException 3 2 →
ConfigException 3 2 →
AuditException 3 2 →
SerializerException 3 2 →
DeserializerException 3 2 →
UserException 3 2 →
NetworkException 3 2 →
FileException 3 2 →

Employee 3 3  
Manager 3 3 → Employee  
Director 3 3 → Employee  
Secretary 3 3 → Employee  
Auditor 3 3 → Employee  
HRManager 3 3 → Employee  
ITSupport 3 3 → Employee  
DepartmentHead 3 3 → Manager  
Contractor 3 3 → Employee  
ExternalUser 3 3 → Contractor, Employee  

DateUtils 2 2  
StringUtils 2 2  
FileHelper 2 2

Поля: 189
Поведения: 171
Ассоциации: 63
Исключения: 12
