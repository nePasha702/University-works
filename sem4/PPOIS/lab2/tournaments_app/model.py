class TournamentRecord:
    """Класс, описывающий одну запись о турнире."""
    
    def __init__(self, tournament_name: str, date_held: str, sport_type: str, winner_name: str, prize_pool: float):
        self.tournament_name = tournament_name
        self.date_held = date_held 
        self.winner_name = winner_name
        self.prize_pool = float(prize_pool)
        
        self.winner_earnings = self._calculate_earnings()

    def _calculate_earnings(self) -> float:
        """Внутренний метод для расчета заработка победителя."""
        return round(self.prize_pool * 0.60, 2)

    def to_tuple(self) -> tuple:
        """Удобный метод для передачи данных в таблицу интерфейса."""
        return (
            self.tournament_name,
            self.date_held,
            self.sport_type,
            self.winner_name,
            self.prize_pool,
            self.winner_earnings
        )


class TournamentModel:
    """Класс, управляющий коллекцией записей (базой данных в памяти)."""
    
    def __init__(self):
        self.records = []  
        self.records_per_page = 10 

    def add_record(self, record: TournamentRecord):
        """Добавление новой записи в массив."""
        self.records.append(record)

    def clear_records(self):
        """Очистка всех записей (понадобится при загрузке нового файла)."""
        self.records.clear()

    def get_all_records(self):
        """Получить все записи."""
        return self.records

    def get_unique_sports(self) -> list:
        """ Собирает список всех уникальных видов спорта из имеющихся записей. """
        sports = set()
        for record in self.records:
            sports.add(record.sport_type)
        return sorted(list(sports))


    def get_total_pages(self, data_list=None) -> int:
        """Возвращает общее количество страниц для переданного списка."""
        if data_list is None:
            data_list = self.records
            
        if not data_list:
            return 1
            
        return (len(data_list) + self.records_per_page - 1) // self.records_per_page

    def get_records_for_page(self, page: int, data_list=None) -> list:
        """Возвращает срез массива записей для конкретной страницы."""
        if data_list is None:
            data_list = self.records
            
        start_index = (page - 1) * self.records_per_page
        end_index = start_index + self.records_per_page
        
        return data_list[start_index:end_index]