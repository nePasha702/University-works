import pytest
from ship_model.ship import Ship
from ship_model.crew import CrewMember
from ship_model.enums import CrewRole
from ship_model.subsystems import Engine, Hull, CommandBridge

@pytest.fixture
def captain():
    """Фикстура: Капитан корабля."""
    return CrewMember("Джек Воробей", CrewRole.CAPTAIN, "CAP-001")

@pytest.fixture
def engineer():
    """Фикстура: Главный механик."""
    return CrewMember("Уилл Тернер", CrewRole.ENGINEER, "ENG-002")

@pytest.fixture
def empty_ship():
    """Фикстура: Корабль на стадии проектирования."""
    return Ship("Черная Жемчужина", "Галеон")

@pytest.fixture
def built_ship(empty_ship):
    """Фикстура: Построенный корабль (корпус и двигатель установлены)."""
    empty_ship.build(hull_capacity=1000.0, engine_power=5000)
    return empty_ship

@pytest.fixture
def equipped_ship(built_ship, captain, engineer):
    """Фикстура: Экипированный корабль с минимальной командой."""
    built_ship.add_crew_member(captain)
    built_ship.add_crew_member(engineer)
    return built_ship

@pytest.fixture
def ready_ship(equipped_ship):
    """Фикстура: Корабль, прошедший калибровку и готовый к отплытию."""
    equipped_ship._bridge.calibrate_systems()
    equipped_ship._bridge.set_course("Тортуга")
    equipped_ship.perform_safety_check()
    return equipped_ship
