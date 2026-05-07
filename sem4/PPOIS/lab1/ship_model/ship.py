from typing import List, Optional, Dict
from .enums import ShipStatus, CrewRole
from .exceptions import NavigationError, ConstructionError, CrewError, ValidationError
from .subsystems import Hull, Engine, CommandBridge, SafetySystem
from .crew import CrewMember

class Ship:
    """
    Центральный класс системы, управляющий состоянием судна и его подсистемами.
    Реализует логику переходов между этапами: от проектирования до навигации.
    """

    def __init__(self, name: str, model_type: str):
        self._name = self._validate_string(name, "Имя корабля")
        self._model_type = self._validate_string(model_type, "Тип модели")
        
        # Начальный статус — Проектирование 
        self._status = ShipStatus.IN_DESIGN
        
        # Композиция: подсистемы создаются вместе с кораблем 
        self._hull: Optional[Hull] = None
        self._engine: Optional[Engine] = None
        self._bridge: Optional[CommandBridge] = None
        self._safety_system: SafetySystem = SafetySystem()
        
        # Агрегация: экипаж управляется извне 
        self._crew: List[CrewMember] = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def status(self) -> ShipStatus:
        return self._status

    @property
    def crew_count(self) -> int:
        return len(self._crew)

    def build(self, hull_capacity: float, engine_power: int) -> None:
        """Операция строительства: установка корпуса и двигателя."""
        if self._status != ShipStatus.IN_DESIGN:
            raise ConstructionError(f"Строительство невозможно: текущий статус {self._status.name}")
        
        self._hull = Hull(capacity=hull_capacity)
        self._engine = Engine(power=engine_power)
        self._bridge = CommandBridge()
        
        self._change_status(ShipStatus.UNDER_CONSTRUCTION)
        print(f"Корабль '{self._name}' успешно построен. Переход в стадию экипировки.")

    def add_crew_member(self, member: CrewMember) -> None:
        """Операция экипировки: наем экипажа."""
        if self._status not in [ShipStatus.UNDER_CONSTRUCTION, ShipStatus.EQUIPPING]:
            raise CrewError("Нанимать экипаж можно только на стадии строительства или экипировки")
        
        if member.role == CrewRole.CAPTAIN:
            has_captain = any(m.role == CrewRole.CAPTAIN for m in self._crew)
            if has_captain:
                raise CrewError("На борту уже есть капитан! Двух капитанов быть не может.")
        
        if self._status == ShipStatus.UNDER_CONSTRUCTION:
            self._change_status(ShipStatus.EQUIPPING)
            
        self._crew.append(member)
        print(f"На борт принят: {member.full_name} ({member.role.name})")

    def perform_safety_check(self) -> Dict[str, bool]:
        """Проверка систем безопасности перед выходом в море."""
        checks = {
            "hull_integrity": self._hull is not None and self._hull.is_intact,
            "engine_ready": self._engine is not None and self._engine.is_functional,
            "crew_minimum": self._check_minimum_crew(),
            "bridge_calibration": self._bridge is not None and self._bridge.is_calibrated
        }
    
        if all(checks.values()) and self._status in [
            ShipStatus.EQUIPPING, 
            ShipStatus.UNDER_CONSTRUCTION, 
            ShipStatus.MAINTENANCE
        ]:
            self._change_status(ShipStatus.READY_FOR_VOYAGE)
            
        return checks

    def sail(self) -> None:
        """Операция навигации и управления."""
        if self._status == ShipStatus.IN_NAVIGATION:
            raise NavigationError("Корабль уже находится в открытом море!")

        if self._status != ShipStatus.READY_FOR_VOYAGE:
            raise NavigationError("Выход в море запрещен! Корабль не готов. Сначала откалибруйте приборы и пройдите проверку безопасности.")
            
        self._change_status(ShipStatus.IN_NAVIGATION)
        print(f"Корабль '{self._name}' вышел в открытое море. Счастливого пути!")

    def dock(self) -> None:
        """Возврат в порт и переход к техническому обслуживанию."""
        if self._status != ShipStatus.IN_NAVIGATION:
            raise NavigationError("Корабль не может пришвартоваться, так как он не в море")
            
        if self._bridge:
            self._bridge.reset_calibration()
        if self._engine:
            self._engine.perform_maintenance()
            
        self._change_status(ShipStatus.MAINTENANCE)
        print(f"Корабль '{self._name}' зашел в порт на ТО. Навигационные системы сброшены.")

    def _change_status(self, new_status: ShipStatus) -> None:
        """Внутренний метод для логирования смены состояний (FSM)."""
        print(f"[FSM] Статус изменен: {self._status.name} -> {new_status.name}")
        self._status = new_status

    def _check_minimum_crew(self) -> bool:
        """Проверка минимальных требований к экипажу для безопасности."""
        roles = [m.role for m in self._crew]
        return CrewRole.CAPTAIN in roles and CrewRole.ENGINEER in roles

    @staticmethod
    def _validate_string(value: str, field_name: str) -> str:
        if not value or not value.strip():
            raise ValidationError(field_name, "Строка не может быть пустой")
        return value.strip()
