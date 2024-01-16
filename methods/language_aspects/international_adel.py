"""
Suche nach den Sprachaspekt International (Verwendung von internationalen Adelstiteln in Speisennamen und Speisenbeschreibungen)

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
input_file_name = 'results/outputs_scraping_cleaning_pos/output_basis.json'
output_file_name = 'results/outputs_language_aspects/international_adel.json'
keywords_file_name = 'datasets/adeltitel_international.txt'

#Einlesen jedes keywords und als Liste speichern in lowercase
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

            if "Bundesland" in obj:
                bundesland = obj["Bundesland"]
            else:
                bundesland = "Undefined"

            restaurantname = obj["restaurantname"]
            url = obj["url"]

            if "latitude" in obj:
                latitude = obj["latitude"]

            if "longitude" in obj:
                longitude = obj["longitude"]

            if 'adresse_stadt' in obj:
                stadt = obj['adresse_stadt'][0]
            elif 'adresse_stadt_p' in obj:
                plz = obj['adresse_stadt_p'].split(' ')[0]
                stadt = obj['adresse_stadt_p'][0]
            else:
                stadt = "Undefined"

            if 'adresse_plz' in obj:
                plz = obj['adresse_plz'][0]
            else:
                plz = "Undefined"

            if 'adresse_straße' in obj:
                straße = obj['adresse_straße'][0]
            elif 'adresse_str_h' in obj:
                straße = obj['adresse_str_h']
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

                #Umwandlung der Speisennamen und Speisenbeschreibungen in Lowercase-Schreibweise
                speisen_doc = speisenname.lower()
                beschreibung_doc = beschreibung.lower()

                splits = [] # Liste für nicht leere Speisennamen und Speisenbeschreibungen
                filtered_splits = [] # Liste für die gefundene Einträge

                if speisen_doc != "":
                    splits.append(speisen_doc)

                if beschreibung_doc != "":
                    splits.append(beschreibung_doc)
                
                #Suche nach den keywords mit RegEx und anschließende Übertragung der gefundenen Einträge in filtered_splits
                for split in splits:
                    if split != "":
                        for keyword in keywords_mapping:
                            if re.search(r'\b' + re.escape(keyword) + r'\b', split):
                                filtered_splits.append(f"{keyword};{keywords_mapping[keyword]}")

                #Falls ein ein Split.Eintrag erstellt wird, wird der dazugehörige Speisenname, die Speisenbeschreibung und der Speisenpreis mit in die Liste der Speisen übertragen
                if filtered_splits:
                    filtered_dishes.append({
                        'speisenname': speisenname2,
                        'beschreibung': beschreibung2,
                        'international_adel_splits': filtered_splits,
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
                    'url': url,
                    'latitude': latitude,
                    'longitude': longitude,
                    'bundesland': bundesland,
                    'speisen': filtered_dishes
                }
                json.dump(data, output_file, ensure_ascii=False, default=lambda x: str(x) if isinstance(x, Decimal) else x)
                output_file.write(',' + '\n')

        output_file.write(']')

    remove_last_comma(output_file_name)
