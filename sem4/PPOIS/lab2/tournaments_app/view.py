import tkinter as tk
import tkinter.font
from tkinter import ttk, messagebox, filedialog

class DatePicker(ttk.Frame):
    """Собственный безопасный виджет для ввода даты."""
    def __init__(self, parent):
        super().__init__(parent)
        days = [str(i).zfill(2) for i in range(1, 32)]
        months = [str(i).zfill(2) for i in range(1, 13)]
        years = [str(i) for i in range(2000, 2030)]
        
        self.day_cb = ttk.Combobox(self, values=days, width=3, state="readonly")
        self.day_cb.set("01")
        self.day_cb.pack(side=tk.LEFT)
        ttk.Label(self, text=".").pack(side=tk.LEFT)
        self.month_cb = ttk.Combobox(self, values=months, width=3, state="readonly")
        self.month_cb.set("01")
        self.month_cb.pack(side=tk.LEFT)
        ttk.Label(self, text=".").pack(side=tk.LEFT)
        self.year_cb = ttk.Combobox(self, values=years, width=5, state="readonly")
        self.year_cb.set("2026")
        self.year_cb.pack(side=tk.LEFT)

    def get_date(self) -> str:
        return f"{self.day_cb.get()}.{self.month_cb.get()}.{self.year_cb.get()}"

class MainWindow(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Управление спортивными турнирами")
        self.geometry("1100x650")
        self.minsize(800, 500)
        self.search_dialog = None

        self._init_menu()
        self._init_toolbar()
        self._init_table()
        self._init_pagination()

    def _init_menu(self):
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Загрузить из XML", command=self._on_load)
        file_menu.add_command(label="Сохранить в XML", command=self._on_save)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.destroy)
        menubar.add_cascade(label="Файл", menu=file_menu)

        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Добавить запись", command=self._open_add_dialog)
        edit_menu.add_command(label="Поиск записей", command=self._open_search_dialog)
        edit_menu.add_command(label="Удалить записи", command=self._open_delete_dialog)
        menubar.add_cascade(label="Управление", menu=edit_menu)

        data_menu = tk.Menu(menubar, tearoff=0)
        data_menu.add_command(label="Сгенерировать тестовые данные", command=self._on_generate_data)
        menubar.add_cascade(label="Данные", menu=data_menu)

        self.config(menu=menubar)

    def _init_toolbar(self):
        toolbar = tk.Frame(self, bd=1, relief=tk.RAISED)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        ttk.Button(toolbar, text="➕ Добавить", command=self._open_add_dialog).pack(side=tk.LEFT, padx=2, pady=2)
        ttk.Button(toolbar, text="🔍 Поиск", command=self._open_search_dialog).pack(side=tk.LEFT, padx=2, pady=2)
        ttk.Button(toolbar, text="🗑 Удалить", command=self._open_delete_dialog).pack(side=tk.LEFT, padx=2, pady=2)
        ttk.Button(toolbar, text="📊 Тестовые данные", command=self._on_generate_data).pack(side=tk.LEFT, padx=15, pady=2)
        
        ttk.Button(toolbar, text="💾 Сохранить", command=self._on_save).pack(side=tk.RIGHT, padx=2, pady=2)
        ttk.Button(toolbar, text="📂 Загрузить", command=self._on_load).pack(side=tk.RIGHT, padx=2, pady=2)

    def _init_table(self):
        table_frame = tk.Frame(self)
        table_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.columns = ("name", "date", "sport", "winner", "prize", "earnings")
        self.tree = ttk.Treeview(table_frame, columns=self.columns, show="headings")
        self.tree.heading("name", text="Название турнира")
        self.tree.heading("date", text="Дата проведения")
        self.tree.heading("sport", text="Вид спорта")
        self.tree.heading("winner", text="ФИО победителя")
        self.tree.heading("prize", text="Призовые")
        self.tree.heading("earnings", text="Заработок (60%)")

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _init_pagination(self):
        page_frame = tk.Frame(self)
        page_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        ttk.Label(page_frame, text="Записей на странице:").pack(side=tk.LEFT)
        self.per_page_var = tk.StringVar(value="10")
        per_page_cb = ttk.Combobox(page_frame, textvariable=self.per_page_var, values=["5", "10", "20", "50"], width=5, state="readonly")
        per_page_cb.pack(side=tk.LEFT, padx=5)
        per_page_cb.bind("<<ComboboxSelected>>", lambda e: self.controller.change_per_page(int(self.per_page_var.get())))

        self.page_info_label = ttk.Label(page_frame, text="Страница 1 из 1")
        self.page_info_label.pack(side=tk.LEFT, padx=20)
        self.total_records_label = ttk.Label(page_frame, text="Всего записей: 0")
        self.total_records_label.pack(side=tk.LEFT, padx=20)

        ttk.Button(page_frame, text=">>", width=3, command=self.controller.last_page).pack(side=tk.RIGHT, padx=2)
        ttk.Button(page_frame, text=">", width=3, command=self.controller.next_page).pack(side=tk.RIGHT, padx=2)
        ttk.Button(page_frame, text="<", width=3, command=self.controller.prev_page).pack(side=tk.RIGHT, padx=2)
        ttk.Button(page_frame, text="<<", width=3, command=self.controller.first_page).pack(side=tk.RIGHT, padx=2)

    def update_table(self, records):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for record in records:
            self.tree.insert("", tk.END, values=record.to_tuple())
        self._auto_resize_columns(self.tree, self.columns)

    def _auto_resize_columns(self, tree, columns):
        """Динамический расчет ширины колонок"""
        dfont = tkinter.font.nametofont("TkDefaultFont")
        for col in columns:
            max_width = dfont.measure(tree.heading(col)["text"]) + 20
            for item in tree.get_children():
                cell_value = str(tree.set(item, col))
                max_width = max(max_width, dfont.measure(cell_value) + 20)
            tree.column(col, width=max_width, minwidth=max_width)

    def update_pagination_info(self, current_page, total_pages, total_records):
        self.page_info_label.config(text=f"Страница {current_page} из {total_pages}")
        self.total_records_label.config(text=f"Всего записей: {total_records}")

    def _on_load(self):
        filepath = filedialog.askopenfilename(filetypes=[("XML", "*.xml")])
        if filepath:
            success, msg = self.controller.load_file(filepath)
            messagebox.showinfo("Информация", msg) if success else messagebox.showerror("Ошибка", msg)

    def _on_save(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML", "*.xml")])
        if filepath:
            success, msg = self.controller.save_file(filepath)
            messagebox.showinfo("Информация", msg) if success else messagebox.showerror("Ошибка", msg)

    def _on_generate_data(self):
        count = self.controller.generate_test_data()
        messagebox.showinfo("Готово", f"Успешно сгенерировано и добавлено {count} записей.")

    def _open_add_dialog(self):
        AddDialog(self, self.controller)

    def _open_search_dialog(self):
        self.search_dialog = SearchDialog(self, self.controller)

    def _open_delete_dialog(self):
        DeleteDialog(self, self.controller)


class AddDialog(tk.Toplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title("Добавить турнир")
        self.geometry("350x250")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        ttk.Label(self, text="Название турнира:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.name_entry = ttk.Entry(self, width=25)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(self, text="Дата проведения:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.date_picker = DatePicker(self)
        self.date_picker.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)

        ttk.Label(self, text="Вид спорта:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        self.sport_entry = ttk.Entry(self, width=25)
        self.sport_entry.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(self, text="ФИО победителя:").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        self.winner_entry = ttk.Entry(self, width=25)
        self.winner_entry.grid(row=3, column=1, padx=10, pady=5)

        ttk.Label(self, text="Размер призовых:").grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
        self.prize_entry = ttk.Entry(self, width=25)
        self.prize_entry.grid(row=4, column=1, padx=10, pady=5)

        ttk.Button(self, text="Сохранить", command=self._on_save).grid(row=5, column=0, columnspan=2, pady=15)

    def _on_save(self):
        data = {
            "name": self.name_entry.get(), "date": self.date_picker.get_date(),
            "sport": self.sport_entry.get(), "winner": self.winner_entry.get(),
            "prize": self.prize_entry.get()
        }
        success, msg = self.controller.add_record(data)
        if success:
            self.destroy()
        else:
            messagebox.showerror("Ошибка валидации", msg)


class SearchDialog(tk.Toplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title("Поиск турниров")
        self.geometry("900x550")
        self.transient(parent)

        unique_sports = self.controller.get_unique_sports()

        filter_frame = ttk.LabelFrame(self, text="Критерии поиска")
        filter_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        ttk.Label(filter_frame, text="Название:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = ttk.Entry(filter_frame, width=15)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(filter_frame, text="ИЛИ Дата:").grid(row=0, column=2, padx=5, pady=5)
        self.date_entry = ttk.Entry(filter_frame, width=10)
        self.date_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(filter_frame, text="Вид спорта:").grid(row=1, column=0, padx=5, pady=5)
        self.sport_cb = ttk.Combobox(filter_frame, values=[""] + unique_sports, state="readonly", width=13)
        self.sport_cb.grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(filter_frame, text="ИЛИ Победитель:").grid(row=1, column=2, padx=5, pady=5)
        self.winner_entry = ttk.Entry(filter_frame, width=15)
        self.winner_entry.grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(filter_frame, text="Призовые (от-до):").grid(row=2, column=0, padx=5, pady=5)
        self.prize_min = ttk.Entry(filter_frame, width=6)
        self.prize_min.grid(row=2, column=1, sticky=tk.W, padx=5)
        self.prize_max = ttk.Entry(filter_frame, width=6)
        self.prize_max.grid(row=2, column=1, sticky=tk.E, padx=5)

        ttk.Label(filter_frame, text="ИЛИ Заработок (от-до):").grid(row=2, column=2, padx=5, pady=5)
        self.earn_min = ttk.Entry(filter_frame, width=6)
        self.earn_min.grid(row=2, column=3, sticky=tk.W, padx=5)
        self.earn_max = ttk.Entry(filter_frame, width=6)
        self.earn_max.grid(row=2, column=3, sticky=tk.E, padx=5)

        ttk.Button(filter_frame, text="Найти", command=self._on_search).grid(row=0, column=4, rowspan=3, padx=20, pady=5)

        self.tree_frame = tk.Frame(self)
        self.tree_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.columns = ("name", "date", "sport", "winner", "prize", "earnings")
        self.tree = ttk.Treeview(self.tree_frame, columns=self.columns, show="headings", height=8)
        for col in self.columns:
            self.tree.heading(col, text=col.capitalize())
        
        scrollbar = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        page_frame = tk.Frame(self)
        page_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)
        self.page_info_label = ttk.Label(page_frame, text="Страница 1 из 1 (Найдено: 0)")
        self.page_info_label.pack(side=tk.LEFT)
        
        ttk.Button(page_frame, text=">>", width=3, command=self.controller.search_last_page).pack(side=tk.RIGHT)
        ttk.Button(page_frame, text=">", width=3, command=self.controller.search_next_page).pack(side=tk.RIGHT)
        ttk.Button(page_frame, text="<", width=3, command=self.controller.search_prev_page).pack(side=tk.RIGHT)
        ttk.Button(page_frame, text="<<", width=3, command=self.controller.search_first_page).pack(side=tk.RIGHT)

    def _on_search(self):
        criteria = {
            "name": self.name_entry.get().strip(), "date": self.date_entry.get().strip(),
            "sport": self.sport_cb.get(), "winner": self.winner_entry.get().strip(),
            "prize_min": self.prize_min.get().strip(), "prize_max": self.prize_max.get().strip(),
            "earn_min": self.earn_min.get().strip(), "earn_max": self.earn_max.get().strip()
        }
        self.controller.execute_search(criteria)

    def update_results(self, records, current_page, total_pages, total_records):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for record in records:
            self.tree.insert("", tk.END, values=record.to_tuple())
        self.page_info_label.config(text=f"Страница {current_page} из {total_pages} (Найдено: {total_records})")
        dfont = tkinter.font.nametofont("TkDefaultFont")
        for col in self.columns:
            max_width = dfont.measure(self.tree.heading(col)["text"]) + 20
            for item in self.tree.get_children():
                cell_value = str(self.tree.set(item, col))
                max_width = max(max_width, dfont.measure(cell_value) + 20)
            self.tree.column(col, width=max_width, minwidth=max_width)


class DeleteDialog(tk.Toplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title("Удалить турниры")
        self.geometry("450x250")
        self.transient(parent)
        self.grab_set()

        unique_sports = self.controller.get_unique_sports()

        ttk.Label(self, text="Название ИЛИ дата:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.name_entry = ttk.Entry(self, width=15)
        self.name_entry.grid(row=0, column=1, padx=2)
        self.date_entry = ttk.Entry(self, width=15)
        self.date_entry.grid(row=0, column=2, padx=2)

        ttk.Label(self, text="Вид спорта ИЛИ победитель:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.sport_cb = ttk.Combobox(self, values=[""] + unique_sports, state="readonly", width=13)
        self.sport_cb.grid(row=1, column=1, padx=2)
        self.winner_entry = ttk.Entry(self, width=15)
        self.winner_entry.grid(row=1, column=2, padx=2)

        ttk.Label(self, text="Призовые (мин-макс):").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.prize_min = ttk.Entry(self, width=6)
        self.prize_min.grid(row=2, column=1, sticky=tk.W)
        self.prize_max = ttk.Entry(self, width=6)
        self.prize_max.grid(row=2, column=1, sticky=tk.E)

        ttk.Button(self, text="Удалить записи", command=self._on_delete).grid(row=4, column=0, columnspan=3, pady=20)

    def _on_delete(self):
        criteria = {
            "name": self.name_entry.get().strip(), "date": self.date_entry.get().strip(),
            "sport": self.sport_cb.get(), "winner": self.winner_entry.get().strip(),
            "prize_min": self.prize_min.get().strip(), "prize_max": self.prize_max.get().strip()
        }
        
        is_empty = all(not str(v) for v in criteria.values())
        if is_empty:
            messagebox.showwarning("Внимание", "Укажите хотя бы один критерий для удаления.")
            return

        deleted_count = self.controller.execute_delete(criteria)
        if deleted_count > 0:
            messagebox.showinfo("Готово", f"Удалено записей: {deleted_count}")
            self.destroy()
        else:
            messagebox.showinfo("Информация", "По заданным критериям ничего не найдено.")