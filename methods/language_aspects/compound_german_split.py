
"""
Suche nach den Sprachaspekt Compound_Split (aufwertender vorderer Teil der nominalen Komposita)

"""


import ijson
import json
from decimal import Decimal
import re

#Methode, um letztes Komma bei der Output_Json zu entfernen
def remove_last_comma(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    if len(lines) >= 2:
        second_last_line = lines[-2].rstrip()
        if second_last_line.endswith(','):
            lines[-2] = second_last_line[:-1]

    with open(json_file, 'w', encoding='utf-8') as file:
        file.writelines(lines)

#Bestimmung der Input und Output-Pfade, sowie keyword File
input_file_name = 'results/outputs_language_aspects/comp_split.json'
output_file_name = 'results/outputs_language_aspects/compounds_adel_deutsch_split.json'
keywords_file_name = 'datasets/adeltitel_deutsch.txt'

#Setzen der Blacklist Wörter der gängigen Speisennamen
blacklisted_words = ['herzoginkartoffel', 'herzoginkartoffeln', 'herzoginerdäpfel', 'königsberger klopse', 'fürstpückler', 'fürst pückler', 'fürst-pückler', 'königin-pastetchen', 'königin-pastete', 'königinpastete', 'königinpastetchen',]

#Einlesen jedes keywords und als Liste speichern
with open(keywords_file_name, 'r', encoding='utf-8') as keywords_file:
    keywords_data = keywords_file.read().splitlines()

#Keywords als Set speichern mit der dazugehörigen Region
keywords_mapping = {}
for line in keywords_data:
    keyword, region = line.split(';')
    keywords_mapping[keyword.lower()] = region

#Einlesen der Input-Datei
with open(input_file_name, 'r', encoding='utf-8') as input_file:
    json_data = ijson.items(input_file, 'item')

    #Direktes Schreiben in die Output-Datei
    with open(output_file_name, 'w', encoding='utf-8') as output_file:
        output_file.write('[')

       #Übertragung der Kategorie, des Bundeslandes, latitude und longitude, URL,  sowie einheitliche Formatierung der Stadt, PLZ und Straße
        for obj in json_data:
            kategorie = obj["kategorie"]


            restaurantname = obj["restaurantname"]


            if "latitude" in obj:
                latitude = obj["latitude"]

            if "longitude" in obj:
                longitude = obj["longitude"]

            if 'stadt' in obj:
                stadt = obj['stadt']
            else:
                stadt = "Undefined"

            if 'plz' in obj:
                plz = obj['plz']
            else:
                plz = "Undefined"

            if 'straße' in obj:
                straße = obj['straße']

            else:
                straße = "Undefined"

            filtered_dishes = []# Liste für die gefilterten Gerichte pro Datenobjekt

            #Originalschreibweise der Speisennamen und Speisenbeschreibungen extrahieren
            for dish in obj["speisen"]:
                speisenname = dish.get('speisenname', '')  # Speisennamen
                beschreibung = dish.get('beschreibung', '')  # Beschreibungen

                #Speichern der Orginalschreibweise der Speisennamen und Speisenbeschreibungen
                speisenname2 = dish['speisenname']
                beschreibung2 = dish['beschreibung']

                #Umwandlung des Preises in eine Gelitkommazahl
                preis = float(dish['preis'])



                filtered_splits = []  # Liste für die gefundenen Einträge
                splits = dish['splits'] #Setzen der splits_liste
                skip_entry = False#Überspringen des Eintrags auf Default "False" setzen

                #Falls ein keyword mit der Blacklist der Wörter übereinstimmt, wird der Eintrag übersprungen
                for blacklisted_word in blacklisted_words:
                    if re.search(r'\b' + re.escape(blacklisted_word) + r'\b', speisenname.lower()):
                         skip_entry = True
                         break
                    
                if skip_entry:
                    continue
                        

                for blacklisted_word in blacklisted_words:
                    if re.search(r'\b' + re.escape(blacklisted_word) + r'\b', beschreibung.lower()):
                        skip_entry = True
                        break
           
                if skip_entry:
                    continue

                for split in splits:
                    words = split.split()  # Teilen der Splits-Einträge in Wörter
                    
                    for word in words:# Extrahieren des vorderen Teil vor dem Zeichen "·" (falls vorhanden)
                        word_parts = word.split('·')
                        front_part = word_parts[0]
                        
                        for keyword in keywords_mapping:
                            if re.search(r'\b' + re.escape(keyword) + r'\b', front_part.lower()):
                                filtered_splits.append(f"{keyword};{keywords_mapping[keyword]}")

                #Falls ein ein Split.Eintrag erstellt wird, wird der dazugehörige Speisenname, die Speisenbeschreibung und der Speisenpreis mit in die Liste der Speisen übertragen
                if filtered_splits:
                    filtered_dishes.append({
                        'speisenname': speisenname2,
                        'beschreibung': beschreibung2,
                        'splits_compound_adel_split': filtered_splits, # Konvertiere das Set in eine Liste
                        'preis': preis
                    })
            # Nur wenn gefilterte Gerichte vorhanden sind, werden die gesamten Informationen der Restaurants mit den Speisen in die neue JSON übertragen
            if filtered_dishes:
                data = {
                    'restaurantname': restaurantname,
                    'kategorie': kategorie,
                    'straße': straße,
                    'stadt': stadt,
                    'plz': plz,
                    'latitude': latitude,
                    'longitude': longitude,
                    'speisen': filtered_dishes
                }
                json.dump(data, output_file, ensure_ascii=False, default=lambda x: str(x) if isinstance(x, Decimal) else x)
                output_file.write(',' + '\n')

        output_file.write(']')

    remove_last_comma(output_file_name)


