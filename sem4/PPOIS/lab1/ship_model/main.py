import sys
from typing import Optional

from .ship import Ship
from .crew import CrewMember
from .enums import ShipStatus, CrewRole
from .exceptions import ShipError, ValidationError

class CLIApplication:
    def __init__(self):
        self.ship: Optional[Ship] = None

    def display_menu(self):
        print("\n" + "="*50)
        print("   КОНСТРУИРОВАНИЕ И ЭКСПЛУАТАЦИЯ СУДОВ - МЕНЮ   ")
        print("="*50)
        print("1. Спроектировать новый корабль")
        print("2. Построить (установить корпус и двигатель)")
        print("3. Нанять члена экипажа")
        print("4. Откалибровать приборы и проложить курс") 
        print("5. Проверить системы безопасности")         
        print("6. Выйти в море (Навигация)")               
        print("7. Пришвартоваться в порту (ТО)")           
        print("8. Показать текущее состояние")             
        print("9. Загрузить демо-данные")                  
        print("0. Выход")
        print("="*50)

    def create_ship(self):
        if self.ship:
            print(f"Ошибка: У вас уже есть активный проект '{self.ship.name}'. Одновременная работа с несколькими судами не поддерживается.")
            return

        name = input("Введите имя корабля: ")
        model = input("Введите тип модели (например, Фрегат): ")
        try:
            self.ship = Ship(name, model)
            print(f"Проект '{name}' создан. Текущий статус: {self.ship.status.name}")
        except ValidationError as e:
            print(f"Ошибка: {e.message}")

    def build_ship(self):
        if not self.ship:
            print("Сначала нужно спроектировать корабль (пункт 1).")
            return
        try:
            cap = float(input("Задайте вместимость корпуса (тонн): "))
            pwr = int(input("Задайте мощность двигателя (л.с.): "))
            self.ship.build(hull_capacity=cap, engine_power=pwr)
        except (ValueError, ShipError) as e:
            msg = e.message if hasattr(e, 'message') else "Некорректный ввод"
            print(f"Ошибка строительства: {msg}")

    def add_crew(self):
        if not self.ship:
            print("Корабль еще не спроектирован.")
            return
        
        print("\nДоступные роли: 1. Капитан, 2. Механик, 3. Матрос, 4. Штурман, 5. Судовой повар")
        choice = input("Выберите роль: ")
        roles = {"1": CrewRole.CAPTAIN, "2": CrewRole.ENGINEER, "3": CrewRole.SAILOR, "4": CrewRole.NAVIGATOR, "5": CrewRole.COOK}
        
        role = roles.get(choice)
        if not role:
            print("Неверный выбор роли.")
            return

        name = input("ФИО члена экипажа: ")
        lic = input("Номер лицензии: ")
        
        try:
            member = CrewMember(name, role, lic)
            self.ship.add_crew_member(member)
        except ShipError as e:
            print(f"Ошибка найма: {e.message}")

    def calibrate_bridge(self):
        """Калибровка мостика."""
        if not self.ship:
            print("Корабль еще не спроектирован.")
            return
        if not self.ship._bridge:
            print("Командный мостик еще не построен (выполните пункт 2).")
            return
        try:
            self.ship._bridge.calibrate_systems()
            dest = input("Введите пункт назначения: ")
            self.ship._bridge.set_course(dest)
            print("Системы успешно откалиброваны. Курс проложен!")
        except (ShipError, ValidationError) as e:
            print(f"Ошибка калибровки: {e.message}")

    def run_navigation(self):
        if not self.ship: return
        try:
            self.ship.sail()
        except ShipError as e:
            print(f"Остановка! {e.message}")

    def show_status(self):
        if not self.ship:
            print("Система пуста.")
            return
        print(f"\n--- СТАТУС СУДНА: {self.ship.name} ---")
        print(f"Модель: {self.ship._model_type}")
        print(f"Статус: {self.ship.status.name}")
        print(f"Экипаж: {self.ship.crew_count} чел.")
        if self.ship.status == ShipStatus.IN_NAVIGATION and self.ship._bridge:
            print(f"Курс на: {self.ship._bridge.current_course}")

    def load_demo(self):
        if self.ship:
            print(f"Ошибка: У вас уже есть активный проект '{self.ship.name}'. Одновременная работа с несколькими судами не поддерживается.")
            return

        self.ship = Ship("Черная Жемчужина", "Галеон")
        self.ship.build(500, 1200)
        self.ship.add_crew_member(CrewMember("Джек Воробей", CrewRole.CAPTAIN, "PIRATE-001"))
        self.ship.add_crew_member(CrewMember("Гиббс", CrewRole.ENGINEER, "ENG-777"))
        print("Демо-данные загружены. Не забудьте откалибровать приборы и проверить безопасность.")

    def run(self):
        while True:
            self.display_menu()
            choice = input("Выберите действие: ")
            
            if choice == "1": self.create_ship()
            elif choice == "2": self.build_ship()
            elif choice == "3": self.add_crew()
            elif choice == "4": self.calibrate_bridge()
            elif choice == "5":
                if self.ship:
                    results = self.ship.perform_safety_check()
                    for k, v in results.items():
                        print(f" - {k}: {'OK' if v else 'FAIL'}")
                    if self.ship.status == ShipStatus.READY_FOR_VOYAGE:
                        print("\n>>> ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ. КОРАБЛЬ ГОТОВ К ОТПЛЫТИЮ! <<<")
            elif choice == "6": self.run_navigation()
            elif choice == "7":
                try: self.ship.dock()
                except ShipError as e: print(e.message)
            elif choice == "8": self.show_status()
            elif choice == "9": self.load_demo()
            elif choice == "0":
                print("Завершение работы...")
                break
            else:
                print("Неверный ввод.")

def main():
    app = CLIApplication()
    try:
        app.run()
    except KeyboardInterrupt:
        print("\nПрограмма принудительно остановлена.")
        sys.exit(0)

if __name__ == "__main__":
    main()