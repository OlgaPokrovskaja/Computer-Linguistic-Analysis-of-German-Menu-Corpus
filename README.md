# lingustic_analysis_of_german_menu_corpus

Diese Repository enthält den Programmcode zur Bachelorarbeit mit den Titel "Anwendung computergestützter Verfahren zur linguistischen Analyse eines deutschen Speisekarten-Korpus", vorgelegt von Olga Pokrovskaja im Januar 2024 an der Universität Leipzig (Institut für Informatik, Studiengang B.Sc. Digital Humaniies). Das Ziel dieser Arbeit war die Erstellung eines großen, deutschsprachigen Speisekarten-Korpus, sowie Entwicklung automatisierter Verfahren zur Suche nach sprachlichen Aufwertungsstrategien der Restaurants. Anschließend sollte gezeigt werden wie oft diese Aufwertungsstrategien im gesamten Korpus, in jedem Bundesland und in jeder Restaurantkategorie vorfinden lassen.

Gliederung der Repository:

1. speisekarte: Python-Programmcode vom Scraping-Verfahren mit den Tool Scrapy zur Erstellung des Korpus im JSON-Format von speisekarte.de:
   - speisekarte/items.py: Definition der Scrapy Items und Aufbau des resultierenden Korpus
   - speisekarte/middlewares.py: Voreinstellungen der Scrapy Middlewares
   - speisekarte/pipelines.py: Voreinstellungen der Scrapy Pipelines
   - speisekarte/settings.py: Zusätzliche Einstellungen für Scrapy
   - speisekarte/spiders:
     - speisekarte/spiders/speisen.py: Scraping von URLs von speisekarte.de
     - speisekarte/spiders/only_url_parse.py: Scraping jedes Restaurants mit Restaurantname, Restaurantkategorie, Restaurantadressse, URL, letzten Aktualisierungsdatum der Speisekarte, sowie aller Speisen mit Speisennamen, Speisenbeschreibung und Speisenpreis


2. cleaning: Bereinigung des entstandenen Korpus
   - cleaning/cleaning.py:
        - Bereinigung des entstandenen Korpus.
        - Falls keine Speisekarte im Restaurant vorhanden ist, wird das Restaurant entfernt.
        - Behebung des Scraping-Fehlers bei den Speisenbeschreibungen.
        - Zusammenführung von Zusatzbeschreibungen zur einer Speisenbeschreibungen.
        - Entfernung von Sonderzeichen in Speisennamen und Speisenbeschreibungen.
        - Extrahierung des Speisenpreis aus den Speisenbeschhreibungen, falls nicht im extra HTML-Container
   - cleaning/cleaning2.py: Entfernen jeder Speise mit keinen eindeutigen Preis
  
3. ngrams: N-Gram-Analyse der Speisennamen und Speisenbeschreibungen
   - ngrams.py: Erstellung von 1-,2-,3- Grams der Beschreibungen und Speisennamen mit Stopwörtern und Ohne
   - ngram_plot.py: Visualisierung der N-Gram Analyse in Lowercase und in Normalschreibweise der Speisennamen und Speisenbeschreibungen
 

