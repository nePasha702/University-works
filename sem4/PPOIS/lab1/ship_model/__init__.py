"""
Пакет ship_model.
Содержит ООП-модель корабля, подсистем и экипажа для симуляции жизненного цикла судна.
"""

from .ship import Ship
from .subsystems import Engine, Hull, CommandBridge, SafetySystem
from .crew import CrewMember
from .enums import ShipStatus, CrewRole, EngineType
from .exceptions import (
    ShipError, 
    ValidationError, 
    ConstructionError, 
    CrewError, 
    NavigationError, 
    SubsystemError, 
    CapacityError
)

__version__ = "1.0.0"

# Явно указываем, что именно экспортируется при вызове: from ship_model import *
__all__ = [
    "Ship",
    "Engine",
    "Hull",
    "CommandBridge",
    "SafetySystem",
    "CrewMember",
    "ShipStatus",
    "CrewRole",
    "EngineType",
    "ShipError",
    "ValidationError",
    "ConstructionError",
    "CrewError",
    "NavigationError",
    "SubsystemError",
    "CapacityError",
]
