from model import TournamentModel, TournamentRecord
from xml_handler import XMLManager
from test_data import generate_test_data

class TournamentController:
    """Управляет логикой приложения."""
    
    def __init__(self, view=None):
        self.model = TournamentModel()
        self.view = view # Ссылка устанавливается извне (в main.py)
        
        self.current_page = 1
        self.search_results = []
        self.search_current_page = 1

    def set_view(self, view):
        self.view = view

    def run(self):
        self.refresh_main_view()
        self.view.mainloop()

    def generate_test_data(self):
        """Загружает 50+ готовых записей."""
        test_records = generate_test_data()
        for rec in test_records:
            self.model.add_record(rec)
        self.current_page = 1
        self.refresh_main_view()
        return len(test_records)

    # --- УПРАВЛЕНИЕ ГЛАВНЫМ ОКНОМ ---
    def refresh_main_view(self):
        total_records = len(self.model.get_all_records())
        total_pages = self.model.get_total_pages()

        if self.current_page > total_pages and total_pages > 0:
            self.current_page = total_pages
        elif total_pages == 0:
            self.current_page = 1

        records_to_show = self.model.get_records_for_page(self.current_page)
        self.view.update_table(records_to_show)
        self.view.update_pagination_info(self.current_page, max(1, total_pages), total_records)

    def change_per_page(self, new_val: int):
        self.model.records_per_page = new_val
        self.current_page = 1
        self.refresh_main_view()

    def next_page(self):
        if self.current_page < self.model.get_total_pages():
            self.current_page += 1
            self.refresh_main_view()

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.refresh_main_view()

    def first_page(self):
        self.current_page = 1
        self.refresh_main_view()

    def last_page(self):
        total_pages = self.model.get_total_pages()
        if total_pages > 0:
            self.current_page = total_pages
            self.refresh_main_view()

    # --- РАБОТА С ФАЙЛАМИ ---
    def load_file(self, filepath: str) -> tuple[bool, str]:
        try:
            XMLManager.load_from_xml(filepath, self.model)
            self.current_page = 1
            self.refresh_main_view()
            return True, "Файл успешно загружен."
        except Exception as e:
            return False, str(e)

    def save_file(self, filepath: str) -> tuple[bool, str]:
        try:
            XMLManager.save_to_xml(filepath, self.model)
            return True, "Файл успешно сохранен."
        except Exception as e:
            return False, str(e)

    # --- ДОБАВЛЕНИЕ ЗАПИСИ ---
    def add_record(self, data: dict) -> tuple[bool, str]:
        """Возвращает (Успех, Сообщение). View само решает, закрывать ли окно."""
        try:
            if not data["name"].strip() or not data["sport"].strip() or not data["winner"].strip():
                return False, "Текстовые поля не могут быть пустыми."
            
            prize = float(data["prize"])
            if prize < 0:
                return False, "Призовые не могут быть отрицательными."
                
            record = TournamentRecord(
                tournament_name=data["name"].strip(),
                date_held=data["date"],
                sport_type=data["sport"].strip(),
                winner_name=data["winner"].strip(),
                prize_pool=prize
            )
            self.model.add_record(record)
            self.current_page = 1
            self.refresh_main_view()
            return True, "Запись добавлена"
        except ValueError:
            return False, "Размер призовых должен быть числом."

    # --- ПОИСК И УДАЛЕНИЕ ---
    def _check_match(self, record: TournamentRecord, criteria: dict) -> bool:
        """
        Реализация AND/OR логики.
        Группы связаны через AND, условия внутри группы через OR.
        """
        # Группа 1: Название турнира ИЛИ Дата (Если введено хотя бы одно)
        match_g1 = True
        if criteria.get("name") or criteria.get("date"):
            n_match = criteria.get("name", "").lower() in record.tournament_name.lower() if criteria.get("name") else False
            d_match = criteria.get("date") == record.date_held if criteria.get("date") else False
            match_g1 = n_match or d_match

        # Группа 2: Вид спорта ИЛИ Победитель
        match_g2 = True
        if criteria.get("sport") or criteria.get("winner"):
            s_match = criteria.get("sport") == record.sport_type if criteria.get("sport") else False
            w_match = criteria.get("winner", "").lower() in record.winner_name.lower() if criteria.get("winner") else False
            match_g2 = s_match or w_match

        # Группа 3: Призовые ИЛИ Заработок (с обработкой диапазонов)
        match_g3 = True
        has_prize = bool(criteria.get("prize_min") or criteria.get("prize_max"))
        has_earn = bool(criteria.get("earn_min") or criteria.get("earn_max"))
        
        if has_prize or has_earn:
            p_match, e_match = False, False
            
            if has_prize:
                try:
                    p_min = float(criteria.get("prize_min")) if criteria.get("prize_min") else 0.0
                    p_max = float(criteria.get("prize_max")) if criteria.get("prize_max") else float('inf')
                    p_match = p_min <= record.prize_pool <= p_max
                except ValueError: pass
                
            if has_earn:
                try:
                    e_min = float(criteria.get("earn_min")) if criteria.get("earn_min") else 0.0
                    e_max = float(criteria.get("earn_max")) if criteria.get("earn_max") else float('inf')
                    e_match = e_min <= record.winner_earnings <= e_max
                except ValueError: pass
                
            match_g3 = (has_prize and p_match) or (has_earn and e_match)

        # Запись подходит, только если она проходит проверку по ВСЕМ заполненным группам
        return match_g1 and match_g2 and match_g3

    def execute_search(self, criteria: dict):
        self.search_results = [r for r in self.model.get_all_records() if self._check_match(r, criteria)]
        self.search_current_page = 1
        self.refresh_search_view()

    def refresh_search_view(self):
        if not hasattr(self, 'view') or not hasattr(self.view, 'search_dialog') or self.view.search_dialog is None:
            return
            
        total_records = len(self.search_results)
        total_pages = self.model.get_total_pages(self.search_results)
        
        records_to_show = self.model.get_records_for_page(self.search_current_page, self.search_results)
        self.view.search_dialog.update_results(records_to_show, self.search_current_page, max(1, total_pages), total_records)

    # ... Методы пагинации поиска остаются прежними ...
    def search_next_page(self):
        if self.search_current_page < self.model.get_total_pages(self.search_results):
            self.search_current_page += 1
            self.refresh_search_view()
    def search_prev_page(self):
        if self.search_current_page > 1:
            self.search_current_page -= 1
            self.refresh_search_view()
    def search_first_page(self):
        self.search_current_page = 1
        self.refresh_search_view()
    def search_last_page(self):
        total_pages = self.model.get_total_pages(self.search_results)
        if total_pages > 0:
            self.search_current_page = total_pages
            self.refresh_search_view()

    def get_unique_sports(self):
        return self.model.get_unique_sports()

    def execute_delete(self, criteria: dict) -> int:
        records_to_keep = []
        deleted_count = 0
        
        for record in self.model.get_all_records():
            if self._check_match(record, criteria):
                deleted_count += 1
            else:
                records_to_keep.append(record)
                
        if deleted_count > 0:
            self.model.records = records_to_keep
            self.refresh_main_view()
            
        return deleted_count