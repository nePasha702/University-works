from typing import Optional
from .enums import CrewRole
from .exceptions import ValidationError, CrewError

class CrewMember:
    """
    Класс, описывающий члена экипажа корабля.
    Отвечает за персональные данные, роль и статус дежурства.
    """
    def __init__(self, full_name: str, role: CrewRole, license_number: str):
        self._full_name = self._validate_string(full_name, "ФИО")
        self._license_number = self._validate_string(license_number, "Номер лицензии")
        self._role = role
        self._is_on_duty = False 

    @property
    def full_name(self) -> str:
        return self._full_name

    @property
    def role(self) -> CrewRole:
        return self._role

    @property
    def license_number(self) -> str:
        return self._license_number

    @property
    def is_on_duty(self) -> bool:
        return self._is_on_duty

    def start_duty(self) -> None:
        """Начало вахты/дежурства."""
        if self._is_on_duty:
            raise CrewError(f"{self._full_name} уже несет вахту.")
        self._is_on_duty = True

    def end_duty(self) -> None:
        """Конец вахты/дежурства."""
        if not self._is_on_duty:
            raise CrewError(f"{self._full_name} сейчас не на вахте.")
        self._is_on_duty = False

    def perform_duty(self, task: str) -> str:
        """Выполнение рабочих обязанностей."""
        task = self._validate_string(task, "Задача")
        
        if not self._is_on_duty:
            raise CrewError(
                f"{self._full_name} не может выполнить задачу '{task}', "
                f"так как не находится на вахте."
            )
        return f"[{self._role.name}] {self._full_name} выполняет: {task}"

    @staticmethod
    def _validate_string(value: str, field_name: str) -> str:
        """Статический метод для проверки строковых данных."""
        if not value or not value.strip():
            raise ValidationError(field_name, "Строка не может быть пустой")
        return value.strip()