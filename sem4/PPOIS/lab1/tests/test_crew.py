import pytest
from ship_model.crew import CrewMember
from ship_model.enums import CrewRole
from ship_model.exceptions import ValidationError, CrewError

class TestCrewMember:
    def test_crew_member_initialization(self):
        """Проверка успешного создания члена экипажа."""
        member = CrewMember("Иван Иванов", CrewRole.SAILOR, "LIC-123")
        assert member.full_name == "Иван Иванов"
        assert member.role == CrewRole.SAILOR
        assert member.license_number == "LIC-123"
        assert not member.is_on_duty

    def test_invalid_name_validation(self):
        """ПРАВИЛЬНЫЙ ТЕСТ: Проверка ошибки при пустом имени."""
        with pytest.raises(ValidationError, match="Ошибка валидации поля 'ФИО'"):
            CrewMember("   ", CrewRole.SAILOR, "LIC-123")

    def test_invalid_license_validation(self):
        """Проверка ошибки при пустой лицензии."""
        with pytest.raises(ValidationError, match="Ошибка валидации поля 'Номер лицензии'"):
            CrewMember("Иван Иванов", CrewRole.SAILOR, "")

    def test_start_duty_success(self):
        member = CrewMember("Петр", CrewRole.NAVIGATOR, "NAV-001")
        member.start_duty()
        assert member.is_on_duty is True

    def test_start_duty_already_on_duty(self):
        member = CrewMember("Петр", CrewRole.NAVIGATOR, "NAV-001")
        member.start_duty()
        with pytest.raises(CrewError, match="уже несет вахту"):
            member.start_duty()

    def test_end_duty_success(self):
        member = CrewMember("Петр", CrewRole.NAVIGATOR, "NAV-001")
        member.start_duty()
        member.end_duty()
        assert member.is_on_duty is False

    def test_end_duty_already_off_duty(self):
        member = CrewMember("Петр", CrewRole.NAVIGATOR, "NAV-001")
        with pytest.raises(CrewError, match="сейчас не на вахте"):
            member.end_duty()

    def test_perform_duty_success(self):
        member = CrewMember("Сидор", CrewRole.COOK, "COOK-99")
        member.start_duty()
        result = member.perform_duty("Приготовить обед")
        assert "Приготовить обед" in result
        assert member.role.name in result

    def test_perform_duty_not_on_duty(self):
        member = CrewMember("Сидор", CrewRole.COOK, "COOK-99")
        with pytest.raises(CrewError, match="не находится на вахте"):
            member.perform_duty("Приготовить обед")

    def test_perform_duty_empty_task(self):
        """Попытка выполнить 'ничего'."""
        member = CrewMember("Сидор", CrewRole.COOK, "COOK-99")
        member.start_duty()
        with pytest.raises(ValidationError, match="Ошибка валидации поля 'Задача'"):
            member.perform_duty("   ")