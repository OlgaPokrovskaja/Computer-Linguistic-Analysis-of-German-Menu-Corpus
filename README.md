# Computer Linguistic Analysis of German Menu Corpus

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
  
4. methods: POS-Tagging, NER-Tagging, Geokoordinaten, BundesländerSuche der Sprachaspekte, Visualisierungen, Komplexitätsmessung, POS-Analyse, Zusammenfführung der Teilkorpora
   - additions: Hinzufügen der POS-Tags, NER-Tags, Lemmatisierungen, Geokoordinaten, Bundesländer
     - addons.py: Hinzufügen vom Mittelwert jeder Wortlänge und Wortanzahl in den Speisenbeschreibungen
     - bundesland.py: Hinzufügen von deutschen Bundesländern anhand der PLZ
     - coordinates.py: Hinzufügen von Koordinaten nach den Mittelpunkt der PLZ
     - pos_tagging.py: Hinzufügen von POS-Tags zu den Scpeisenbeschreibungen mit Stanza
     - pos_lemmatization.py: Hinzufügen von POS-Tags und Lemmatisierungen zu Speisennamen; Hinzufügen von Lemmatisierungen zu den Speisenbeschreibungen mit Stanza
     - ner_tagging.py: Hinzufügen von NER-Tags zu den Scpeisenbeschreibungen und Speisennamen mit Stanza
     - ner_analysis.py: Erstellung von Frequenzlisten für die NER-Tags Personennamen (PER), Ortsnennungen (LOC), Organisationen (ORG) und Verschiedenes (MISC)
   - pos_analysis: POS-Tag Kombinationen, Wortarten-Frequenzlisten, Scatter-Plot Erstellung der Wortarten
     - pos_combination.py: Suche nach Komposita Kombinationen durch POS-Tags Kombinationen
     - pos_frequency.py: N-Gram Analyse durch POS-Tags von Adjektiven (ADJ), Verben (VERB), Eigennamen (PROPN), Nomen (NOUN), Prepositionen (ADP), Adverbien (ADV)
     - pos_plot.py: Plot der 1-Gram Analyse der Wortarten
   - language_aspects: Suche der Sprachaspekte
     - adjectives.py: Suche nach den Sprachaspekt Adjectives (aufwertende Adjektive in Speisennamen und Speisenbeschreibungen)
     - comp_split.py: Erstellung des Teilkorpus nur mit gefundenen Splits des Compound-Splitters
     - compound_german_adel.py: Suche nach den Sprachaspekt Compound_Bind (aufwertender vorderer Teil der nominalen Komposita-Bindestrich-Zusammensetzungen)
     - compound_german_split.py: Suche nach den Sprachaspekt Compound_Split (aufwertender vorderer Teil der nominalen Komposita)
     - descriptions_analysis.py: Erstellung des Teilkorpus "descriptions_output" zur detaillierten Analyse der Speisenbeschreibungen
     - dialekte.py: Suche nach den Sprachaspekt Dialect (Verwendung von dialektaler Sprache Speisennamen und Speisenbeschreibungen)
     - homemade.py: Suche nach den Sprachaspekt Homemade (Verwendung von "hausgemacht"-Erwähnungen und Synonymen in Speisennamen und Speisenbeschreibungen)
     - international_adel.py: Suche nach den Sprachaspekt International (Verwendung von internationalen Adelstiteln in Speisennamen und Speisenbeschreibungen)
     - none-corpus.py: Erstellung des Teilkorpus 'None' (Restaurants und Speisen mit keinen einzigen Sprachaspekt)
     - personen.py: Suche nach den Sprachaspekt Person (Verwendung von Personennamen in  Speisennamen und Speisenbeschreibungen)
     - prepositions.py: Suche nach den Sprachaspekt Preposition (aufwertende Preposition "an" in Speisennamen und Speisenbeschreibungen)
     - region.py: Suche nach den Sprachaspekt Region (Verwendung Erwähnungen der Stadt oder Bundeslandes des Restaurants Speisennamen und Speisenbeschreibungen)
   - descriptiv_analysis: Erstellung der Daten für die deskreptive Analyse
     - analysis_language_aspects.py: Daten für deskriptive Analyse der Sprachaspekte zu generieren
     - frequency_categorie.py: Erstellung der Frequenzlisten der Restaurantkategorien für jeden Sprachaspekt
   - combine_outputs: Skripte zum Zusammenfügen der Teilkorpora der Sprachaspekte zu einem Korpus (Teil 1 bis 11)
   - visualisation:
     - mapping_dots.py: Visualisierung des gesamten Korpus
     - mapping_hexbin.py: Visualisierung der Sprachaspekte nach der Varianz der Restaurantkategorien in Form von Hexagons (Umkreis ca. 50 km)
     - plotting: Visualisierung der Komplexitätsmessung

5. datasets: Verwendete Datensätze für Geokoordinaten, Bundesländer und manuell erstellte Lexika zur Suche der Sprachaspekte:
   - lang_long.csv: Zuordnung der Postleitzahlen zum geogrpaphischen Mittelpunkt
   - plz_de.csv: Zuordnung der Postleitzahlen, Ortsnamen und Bundeslandes
   - adeltitel_deutsch.txt: manuell erstelltes Lexika deutscher Adelstitel
   - adeltitel_international.txt: manuell erstelltes Lexika internationaler Adelstitel
   - adjektive.txt: manuell erstelltes Lexika aufwertender Adjektive
   - adp_keyword.txt: aufwertende Preposition "an"
   - dialekte.txt: manuell erstelltes Lexika der regionalen Küchenbegriffe
   - homemade.txt: manuell erstelltes Lexika der "hausgemacht"-Begriffe und Synonyme
   - person_ruf.txt: manuell erstelltes Lexika der Rufnamen
   - person_name.txt: manuell erstelltes Lexika der berühmten Personnennamen, sowie Namen von Comic-, Buch-, Filmcharakteren
 

