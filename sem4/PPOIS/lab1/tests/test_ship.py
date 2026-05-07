import pytest
from ship_model.ship import Ship
from ship_model.enums import ShipStatus, CrewRole
from ship_model.crew import CrewMember
from ship_model.exceptions import ValidationError, ConstructionError, CrewError, NavigationError

class TestShip:
    def test_ship_initialization(self):
        ship = Ship("Летучий Голландец", "Фрегат")
        assert ship.name == "Летучий Голландец"
        assert ship.status == ShipStatus.IN_DESIGN
        assert ship.crew_count == 0

    def test_ship_init_invalid_name(self):
        with pytest.raises(ValidationError, match="Ошибка валидации поля 'Имя корабля'"):
            Ship("   ", "Фрегат")

    def test_ship_init_invalid_model(self):
        with pytest.raises(ValidationError, match="Ошибка валидации поля 'Тип модели'"):
            Ship("Летучий Голландец", "")

    def test_ship_build_success(self, empty_ship):
        empty_ship.build(100.0, 500)
        assert empty_ship.status == ShipStatus.UNDER_CONSTRUCTION
        assert empty_ship._hull is not None

    def test_ship_build_already_built(self, built_ship):
        with pytest.raises(ConstructionError, match="Строительство невозможно"):
            built_ship.build(100.0, 500)

    def test_add_crew_member_success(self, built_ship, captain):
        built_ship.add_crew_member(captain)
        assert built_ship.crew_count == 1
        assert built_ship.status == ShipStatus.EQUIPPING

    def test_add_crew_wrong_status(self, empty_ship, captain):
        """Попытка нанять экипаж до постройки корабля."""
        with pytest.raises(CrewError, match="Нанимать экипаж можно только на стадии"):
            empty_ship.add_crew_member(captain)

    def test_add_second_captain_fails(self, built_ship, captain):
        built_ship.add_crew_member(captain)
        second_captain = CrewMember("Барбосса", CrewRole.CAPTAIN, "CAP-002")
        with pytest.raises(CrewError, match="Двух капитанов быть не может"):
            built_ship.add_crew_member(second_captain)

    def test_perform_safety_check_not_built(self, empty_ship):
        """Проверка безопасности только что спроектированного корабля (все подсистемы None)."""
        checks = empty_ship.perform_safety_check()
        assert not checks["hull_integrity"]
        assert not checks["engine_ready"]
        assert not checks["bridge_calibration"]

    def test_perform_safety_check_broken_engine(self, equipped_ship):
        """Проверка безопасности при сломанном двигателе."""
        equipped_ship._engine._is_functional = False
        checks = equipped_ship.perform_safety_check()
        assert not checks["engine_ready"]

    def test_sail_success(self, ready_ship):
        ready_ship.sail()
        assert ready_ship.status == ShipStatus.IN_NAVIGATION

    def test_sail_fails_not_ready(self, equipped_ship):
        with pytest.raises(NavigationError, match="Корабль не готов"):
            equipped_ship.sail()

    def test_sail_already_in_navigation(self, ready_ship):
        """Попытка выйти в море дважды."""
        ready_ship.sail()
        with pytest.raises(NavigationError, match="Корабль уже находится в открытом море"):
            ready_ship.sail()

    def test_dock_not_in_navigation(self, ready_ship):
        """Попытка пришвартоваться, будучи в порту."""
        with pytest.raises(NavigationError, match="не может пришвартоваться, так как он не в море"):
            ready_ship.dock()

    def test_dock_success(self, ready_ship):
        ready_ship.sail() 
        ready_ship.dock() 
        assert ready_ship.status == ShipStatus.MAINTENANCE