import xml.sax
from xml.dom.minidom import Document
from model import TournamentRecord

class TournamentSAXHandler(xml.sax.ContentHandler):
    """Обработчик SAX для чтения XML-файла."""
    
    def __init__(self, model):
        self.model = model
        self.current_element = ""
        self.current_value = ""
        self.record_data = {}

    def startElement(self, tag, attributes):
        """Вызывается при открытии тега (например, <name>)."""
        self.current_element = tag
        self.current_value = ""

    def characters(self, content):
        """Читает текстовое содержимое внутри тегов."""
        self.current_value += content

    def endElement(self, tag):
        """Вызывается при закрытии тега (например, </name>)."""
        if tag == "tournament":
            try:
                record = TournamentRecord(
                    tournament_name=self.record_data.get("name", ""),
                    date_held=self.record_data.get("date_held", ""),
                    sport_type=self.record_data.get("sport_type", ""),
                    winner_name=self.record_data.get("winner_name", ""),
                    prize_pool=self.record_data.get("prize_pool", 0)
                )
                self.model.add_record(record)
            except ValueError:
                pass 
            self.record_data = {} 
            
        elif tag in ["name", "date_held", "sport_type", "winner_name", "prize_pool"]:
            self.record_data[tag] = self.current_value.strip()
            
        self.current_element = ""


class XMLManager:
    """Менеджер для импорта (SAX) и экспорта (DOM) XML."""
    
    @staticmethod
    def load_from_xml(filepath: str, model):
        """Загрузка данных с использованием SAX-парсера."""
        handler = TournamentSAXHandler(model)
        parser = xml.sax.make_parser()
        parser.setContentHandler(handler)
        
        model.clear_records()
        parser.parse(filepath)

    @staticmethod
    def save_to_xml(filepath: str, model):
        """Сохранение данных с использованием DOM-парсера."""
        doc = Document()
        root = doc.createElement("tournaments")
        doc.appendChild(root)

        for record in model.get_all_records():
            tournament_elem = doc.createElement("tournament")
            root.appendChild(tournament_elem)

            def add_element(name, text):
                elem = doc.createElement(name)
                text_node = doc.createTextNode(str(text))
                elem.appendChild(text_node)
                tournament_elem.appendChild(elem)

            add_element("name", record.tournament_name)
            add_element("date_held", record.date_held)
            add_element("sport_type", record.sport_type)
            add_element("winner_name", record.winner_name)
            add_element("prize_pool", record.prize_pool)
            
        with open(filepath, "w", encoding="utf-8") as f:
            doc.writexml(f, indent="", addindent="    ", newl="\n")