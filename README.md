# lingustic_analysis_of_german_menu_corpus

Diese Repository enthält den Programmcode zur Bachelorarbeit mit den Titel "Anwendung computergestützter Verfahren zur linguistischen Analyse eines deutschen Speisekarten-Korpus", vorgelegt von Olga Pokrovskaja im Januar 2024 an der Universität Leipzig (Institut für Informatik, Studiengang B.Sc. Digital Humaniies). Das Ziel dieser Arbeit war die Erstellung eines großen, deutschsprachigen Speisekarten-Korpus, sowie Entwicklung automatisierter Verfahren zur Suche nach sprachlichen Aufwertungsstrategien der Restaurants. Anschließend sollte gezeigt werden wie oft diese Aufwertungsstrategien im gesamten Korpus, in jedem Bundesland und in jeder Restaurantkategorie vorfinden lassen. Zu den sprachlichen Aufwertungsstrategien gehören:

1.	Language-ID: 
Verwendung unterschiedlicher Sprachen in Speisennamen und Beschreibungen, insbe-sondere deutsche oder englische Übersetzungen 
2.	Complexity: 
Länge und der Komplexität der Speisennamen und Beschreibungen
3.	Compound: 
Komposita, insbesondere die Verwendung vom aufwertenden vorderen Teil in Speisen-namen und Beschreibungen
4.	Person: 
Verwendung von Personennamen in Speisennamen und Beschreibungen
5.	Homemade: 
Verwendung von Signalwörtern, wie „hausgemacht“ und Synonymen in Spesennamen und Beschreibungen
6.	Dialects: 
Nutzung von dialektalen oder regionalen Sprachelementen in Speisennamen und Be-schreibungen
7.	Region: 
Ortsnennungen in den Speisennamen und Beschreibungen
8.	Adjectives: 
Verwendung von aufwertenden Adjektiven in Speisennamen und Beschreibungen
9.	Preposition: 
Verwendungen von besonders aufwertender Präposition „an“ in Speisennamen und Be-schreibungen

Als Erweiterung wurden folgende Aufwertungsstrategien betrachtet:

10. Compounds_Bind:
Verwendung von deutschen Adelstiteln im vorderen Teil des Kompositums in Bindestrich-Zusammensetzungen
11. Compounds_Split:
Verwendung von deutschen Adelstiteln im vorderen Teil des Kompositums ohne Bindestrich-Zusammensetzungen
12. Person_Ruf:
Verwendung von Rufnamen in Speisennamen und Beschreibungen
13. Person-Name:
Verwendung von berühmten Personennamen, sowie Namen von Film-, Buch- und Comic-Charakteren
14. International:
Verwendung von internationalen Adelstiteln in Speisennamen und Speisenbeschreibungen

Gliederung der Repository:

1. speisekarte: Python-Programmcode vom Scraping-Verfahren mit den Tool Scrapy zur Erstellung des Korpus im JSON-Format von speisekarte.de:
   - speisekarte/items.py: Definition der Scrapy Items und Aufbau des resultierenden Korpus
   - speisekarte/middlewares.py: Voreinstellungen der Scrapy Middlewares
   - speisekarte/pipelines.py: Voreinstellungen der Scrapy Pipelines
   - speisekarte/settings.py: Zusätzliche Einstellungen für Scrapy
   - speisekarte/spiders:
   -    - speisekarte/spiders/speisen.py: Scraping von URLs von speisekarte.de#
        - speisekarte/spiders/only_url_parse.py: Scraping jedes Restaurants mit Restaurantname, Restaurantkategorie, Restaurantadressse, URL, letzten Aktualisierungsdatum der Speisekarte, sowie aller Speisen mit Speisennamen, Speisenbeschreibung und Speisenpreis

2. cleaning: Bereinigung des entstandenen Korpus
   - cleaning/cleaning.py:
   -    - Bereinigung des entstandenen Korpus.
        - Falls keine Speisekarte im Restaurant vorhanden ist, wird das Restaurant entfernt.
        - Behebung des Scraping-Fehlers bei den Speisenbeschreibungen.
        - Zusammenführung von Zusatzbeschreibungen zur einer Speisenbeschreibungen.
        - Entfernung von Sonderzeichen in Speisennamen und Speisenbeschreibungen.
        - Extrahierung des Speisenpreis aus den Speisenbeschhreibungen, falls nicht im extra HTML-Container
   - cleaning/cleaning2.py: Entfernen jeder Speise mit keinen eindeutigen Preis

