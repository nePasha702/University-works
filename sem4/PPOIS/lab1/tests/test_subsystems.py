import pytest
from ship_model.subsystems import Hull, Engine, CommandBridge, SafetySystem
from ship_model.exceptions import ValidationError, CapacityError, SubsystemError

class TestHull:
    def test_hull_initialization(self):
        hull = Hull(500.0)
        assert hull.capacity == 500.0
        assert hull.is_intact is True

    def test_hull_invalid_capacity(self):
        with pytest.raises(ValidationError, match="строго положительной"):
            Hull(-50.0)

    def test_hull_load_cargo_success(self):
        hull = Hull(100.0)
        hull.load_cargo(60.0)
        assert hull._current_load == 60.0

    def test_hull_load_cargo_negative(self):
        hull = Hull(100.0)
        with pytest.raises(ValidationError, match="Количество груза не может быть отрицательным"):
            hull.load_cargo(-10.0)

    def test_hull_load_cargo_exceed_capacity(self):
        hull = Hull(100.0)
        with pytest.raises(CapacityError, match="Превышен лимит вместимости"):
            hull.load_cargo(150.0)

    def test_hull_damage_and_repair(self):
        hull = Hull(100.0)
        hull.take_damage(40.0)
        assert hull.is_intact
        hull.take_damage(20.0)
        assert not hull.is_intact
        hull.repair()
        assert hull.is_intact

    def test_hull_take_negative_damage(self):
        hull = Hull(100.0)
        with pytest.raises(ValidationError, match="Урон не может быть отрицательным"):
            hull.take_damage(-5.0)

class TestEngine:
    def test_engine_invalid_power(self):
        with pytest.raises(ValidationError, match="больше нуля"):
            Engine(0)

    def test_engine_start_stop(self):
        engine = Engine(1000)
        engine.start()
        assert engine.is_running
        engine.stop()
        assert not engine.is_running

    def test_broken_engine_cannot_start(self):
        engine = Engine(1000)
        engine._is_functional = False 
        with pytest.raises(SubsystemError, match="Невозможно запустить неисправный двигатель"):
            engine.start()

    def test_engine_maintenance(self):
        engine = Engine(1000)
        engine._is_functional = False
        engine._is_running = True
        engine.perform_maintenance()
        assert engine.is_functional is True
        assert engine.is_running is False

class TestCommandBridge:
    def test_bridge_set_course_without_calibration(self):
        bridge = CommandBridge()
        with pytest.raises(SubsystemError, match="системы не откалиброваны"):
            bridge.set_course("Порт Роял")

    def test_bridge_set_empty_course(self):
        bridge = CommandBridge()
        bridge.calibrate_systems()
        with pytest.raises(ValidationError, match="Пункт назначения не может быть пустым"):
            bridge.set_course("   ")

class TestSafetySystem:
    def test_safety_equipment_check(self):
        sys = SafetySystem(lifeboats_count=0, extinguishers_count=0)
        assert not sys.check_equipment()
        sys.replenish_equipment(5, 10)
        assert sys.check_equipment()

    def test_invalid_replenish(self):
        sys = SafetySystem()
        with pytest.raises(ValidationError, match="не может быть отрицательным"):
            sys.replenish_equipment(-5, 10)