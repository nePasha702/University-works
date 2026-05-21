from model import TournamentRecord

def generate_test_data() -> list:
    """Генерирует 55 тестовых записей"""
    return [
        # Киберспорт
        TournamentRecord("The International 2024", "15.09.2024", "Dota 2", "Team Spirit", 3000000),
        TournamentRecord("IEM Katowice 2024", "11.02.2024", "CS2", "Team Falcon", 1000000),
        TournamentRecord("Worlds 2024", "02.11.2024", "League of Legends", "T1", 2250000),
        TournamentRecord("Valorant Champions", "25.08.2024", "Valorant", "Evil Geniuses", 2250000),
        TournamentRecord("EWC Riyadh 2024", "14.07.2024", "Dota 2", "Gaimin Gladiators", 5000000),
        TournamentRecord("Blast Premier Final", "17.12.2023", "CS2", "Vitality", 1000000),
        TournamentRecord("Evo 2024", "21.07.2024", "Tekken 8", "Arslan Ash", 100000),
        TournamentRecord("RLCS World Championship", "10.09.2023", "Rocket League", "Team Vitality", 2100000),
        TournamentRecord("Six Invitational 2024", "25.02.2024", "Rainbow Six Siege", "w7m esports", 3000000),
        TournamentRecord("ALGS Championship 2023", "10.09.2023", "Apex Legends", "TSM", 2000000),
        TournamentRecord("PUBG Global Championship", "03.12.2023", "PUBG", "Danawa e-sports", 2000000),
        
        # Теннис
        TournamentRecord("Wimbledon 2024", "14.07.2024", "Теннис", "Карлос Алькарас", 59000000),
        TournamentRecord("US Open 2023", "10.09.2023", "Теннис", "Новак Джокович", 65000000),
        TournamentRecord("Roland Garros 2024", "09.06.2024", "Теннис", "Карлос Алькарас", 53000000),
        TournamentRecord("Australian Open 2024", "28.01.2024", "Теннис", "Янник Синнер", 57000000),
        TournamentRecord("ATP Finals Turin", "19.11.2023", "Теннис", "Новак Джокович", 15000000),
        TournamentRecord("Indian Wells Masters", "17.03.2024", "Теннис", "Карлос Алькарас", 8900000),
        TournamentRecord("Miami Open", "31.03.2024", "Теннис", "Янник Синнер", 8900000),
        TournamentRecord("Monte-Carlo Masters", "14.04.2024", "Теннис", "Стефанос Циципас", 5900000),
        TournamentRecord("Madrid Open", "05.05.2024", "Теннис", "Андрей Рублев", 7800000),
        TournamentRecord("Rome Masters", "19.05.2024", "Теннис", "Александр Зверев", 7800000),
        
        # Футбол
        TournamentRecord("Лига Чемпионов УЕФА", "01.06.2024", "Футбол", "Реал Мадрид", 85000000),
        TournamentRecord("Лига Европы УЕФА", "22.05.2024", "Футбол", "Аталанта", 25000000),
        TournamentRecord("Клубный чемпионат мира", "22.12.2023", "Футбол", "Манчестер Сити", 16000000),
        TournamentRecord("Кубок Либертадорес", "04.11.2023", "Футбол", "Флуминенсе", 21000000),
        TournamentRecord("Кубок Азии", "10.02.2024", "Футбол", "Катар", 14000000),
        TournamentRecord("Кубок Африканских наций", "11.02.2024", "Футбол", "Кот-д Ивуар", 7000000),
        TournamentRecord("Суперкубок УЕФА", "16.08.2023", "Футбол", "Манчестер Сити", 5000000),
        TournamentRecord("Кубок Англии", "25.05.2024", "Футбол", "Манчестер Юнайтед", 4500000),
        TournamentRecord("Кубок Испании", "06.04.2024", "Футбол", "Атлетик Бильбао", 3000000),
        TournamentRecord("Кубок Германии", "25.05.2024", "Футбол", "Байер 04", 4000000),
        
        # Шахматы
        TournamentRecord("FIDE World Cup", "24.08.2023", "Шахматы", "Магнус Карлсен", 1892500),
        TournamentRecord("Candidates Tournament", "21.04.2024", "Шахматы", "Доммараджу Гукеш", 500000),
        TournamentRecord("Tata Steel Chess", "28.01.2024", "Шахматы", "Вэй И", 350000),
        TournamentRecord("Norway Chess", "07.06.2024", "Шахматы", "Магнус Карлсен", 160000),
        TournamentRecord("Sinquefield Cup", "30.11.2023", "Шахматы", "Фабиано Каруана", 350000),
        TournamentRecord("Grand Swiss", "05.11.2023", "Шахматы", "Видит Гуджрати", 460000),
        TournamentRecord("World Rapid Chess", "28.12.2023", "Шахматы", "Магнус Карлсен", 350000),
        TournamentRecord("World Blitz Chess", "30.12.2023", "Шахматы", "Магнус Карлсен", 350000),
        TournamentRecord("Chessable Masters", "07.02.2024", "Шахматы", "Магнус Карлсен", 300000),
        TournamentRecord("Grenke Chess Classic", "01.04.2024", "Шахматы", "Магнус Карлсен", 200000),
        
        # Разное (Гольф, Покер, Снукер)
        TournamentRecord("Masters Tournament", "14.04.2024", "Гольф", "Скотти Шеффлер", 20000000),
        TournamentRecord("PGA Championship", "19.05.2024", "Гольф", "Ксандер Шоффеле", 18500000),
        TournamentRecord("US Open Golf", "16.06.2024", "Гольф", "Брайсон Дешамбо", 21500000),
        TournamentRecord("The Open Championship", "23.07.2023", "Гольф", "Брайан Харман", 16500000),
        TournamentRecord("WSOP Main Event", "17.07.2023", "Покер", "Дэниел Вайнман", 93399900),
        TournamentRecord("EPT Prague Main Event", "17.12.2023", "Покер", "Падрейг О'Нил", 6000000),
        TournamentRecord("WPT World Championship", "21.12.2023", "Покер", "Дэн Сепиол", 40000000),
        TournamentRecord("World Snooker Championship", "06.05.2024", "Снукер", "Кайрен Уилсон", 2900000),
        TournamentRecord("UK Championship", "03.12.2023", "Снукер", "Ронни О'Салливан", 1500000),
        TournamentRecord("The Masters Snooker", "14.01.2024", "Снукер", "Ронни О'Салливан", 900000),
        TournamentRecord("Tour Championship", "07.04.2024", "Снукер", "Марк Уильямс", 600000),
        TournamentRecord("Tour de France", "23.07.2023", "Велоспорт", "Йонас Вингегор", 2500000),
        TournamentRecord("Giro d'Italia", "26.05.2024", "Велоспорт", "Тадей Погачар", 1700000),
        TournamentRecord("Super Bowl LVIII", "11.02.2024", "Американский футбол", "Kansas City Chiefs", 12000000)
    ]