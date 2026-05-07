from typing import Optional
from .enums import EngineType
from .exceptions import ValidationError, SubsystemError, CapacityError

class Hull:
    """
    Класс корпуса/борта корабля. 
    Отвечает за физическую целостность и базовую вместимость.
    """
    def __init__(self, capacity: float):
        if capacity <= 0:
            raise ValidationError("capacity", "Вместимость корпуса должна быть строго положительной")
        self._capacity = capacity
        self._current_load = 0.0
        self._is_intact = True
        self._damage_level = 0.0

    @property
    def capacity(self) -> float:
        return self._capacity

    @property
    def is_intact(self) -> bool:
        return self._is_intact
    
    def load_cargo(self, amount: float) -> None:
        """Погрузка груза ."""
        if amount < 0:
            raise ValidationError("amount", "Количество груза не может быть отрицательным")
        if self._current_load + amount > self._capacity:
            raise CapacityError(limit=self._capacity, attempted=self._current_load + amount)
        self._current_load += amount

    def take_damage(self, damage_percent: float) -> None:
        """Регистрация повреждений борта."""
        if damage_percent < 0:
            raise ValidationError("damage_percent", "Урон не может быть отрицательным")
        self._damage_level = min(100.0, self._damage_level + damage_percent)
        if self._damage_level >= 50.0:
            self._is_intact = False

    def repair(self) -> None:
        """Ремонт корпуса в доке."""
        self._damage_level = 0.0
        self._is_intact = True


class Engine:
    """
    Класс судового двигателя.
    Управляет запуском, мощностью и состоянием машин.
    """
    def __init__(self, power: int, engine_type: EngineType = EngineType.DIESEL):
        if power <= 0:
            raise ValidationError("power", "Мощность двигателя должна быть больше нуля")
        self._power = power
        self._engine_type = engine_type
        self._is_functional = True
        self._is_running = False

    @property
    def is_functional(self) -> bool:
        return self._is_functional

    @property
    def is_running(self) -> bool:
        return self._is_running

    def start(self) -> None:
        """Запуск двигателя перед отплытием."""
        if not self._is_functional:
            raise SubsystemError("Невозможно запустить неисправный двигатель")
        self._is_running = True

    def stop(self) -> None:
        """Остановка двигателя."""
        self._is_running = False

    def perform_maintenance(self) -> None:
        """Техническое обслуживание двигателя."""
        self._is_functional = True
        self.stop()


class CommandBridge:
    """
    Класс командного мостика.
    Отвечает за навигационное оборудование и прокладку курса.
    """
    def __init__(self):
        self._is_calibrated = False
        self._current_course: Optional[str] = None

    @property
    def is_calibrated(self) -> bool:
        return self._is_calibrated

    @property
    def current_course(self) -> Optional[str]:
        return self._current_course

    def calibrate_systems(self) -> None:
        """Калибровка навигационных систем (обязательна перед отплытием)."""
        self._is_calibrated = True

    def set_course(self, destination: str) -> None:
        """Прокладка курса к пункту назначения."""
        if not self._is_calibrated:
            raise SubsystemError("Невозможно проложить курс: системы не откалиброваны")
        if not destination.strip():
            raise ValidationError("destination", "Пункт назначения не может быть пустым")
        self._current_course = destination.strip()
    
    def reset_calibration(self) -> None:
        """Сброс калибровки и курса после возвращения в порт."""
        self._is_calibrated = False
        self._current_course = None


class SafetySystem:
    """
    Класс систем безопасности судна.
    Независимо контролирует наличие спасательного оборудования.
    """
    def __init__(self, lifeboats_count: int = 10, extinguishers_count: int = 50):
        self._lifeboats_count = lifeboats_count
        self._extinguishers_count = extinguishers_count

    def check_equipment(self) -> bool:
        """
        Проверка минимально необходимого спасательного оборудования.
        Возвращает True, если оборудование в норме.
        """
        return self._lifeboats_count > 0 and self._extinguishers_count > 0

    def replenish_equipment(self, lifeboats: int, extinguishers: int) -> None:
        """Пополнение запасов спасательного оборудования."""
        if lifeboats < 0 or extinguishers < 0:
            raise ValidationError("equipment", "Количество пополняемого оборудования не может быть отрицательным")
        self._lifeboats_count += lifeboats
        self._extinguishers_count += extinguishers
