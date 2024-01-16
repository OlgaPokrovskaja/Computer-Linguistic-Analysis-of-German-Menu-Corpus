
"""
Suche nach den Sprachaspekt Compound_Bind (aufwertender vorderer Teil der nominalen Komposita-Bindestrich-Zusammensetzungen)

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
output_file_name = 'results/outputs_language_aspects/compounds_adel_deutsch.json'
keywords_file_name = 'datasets/adeltitel_deutsch.txt'

#Setzen der Blacklist Wörter der gängigen Speisennamen
blacklisted_words = ['herzogin-kartoffel', 'herzogin-kartoffeln', 'herzogin - kartoffeln', 'herzogin - kartoffel' 'herzogin-erdäpfel', 'königsberger klopse', 'fürst-pückler', 'fürst pückler', 'fürst - pückler', 'königin-pastetchen', 'königin-pastete']

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


                splits = [] # Liste für nicht leere Speisennamen und Speisenbeschreibungen
                filtered_splits = [] # Liste für die gefundenen Einträge
                skip_entry = False #Überspringen des Eintrags auf Default "False" setzen
                
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

                #Suche nach den Keywords in den Speisennamen und Speisenbeschreibungen, falls eine POS-Tag Struktur von Bindestrich-Zusammensetzungen vorliegt
                for tags in [dish['pos_tags'], dish['pos_tags_s']]:
                    for i in range(len(tags) - 2):
                        tag1 = tags[i][2]
                        tag2 = tags[i + 1][2]
                        tag3 = tags[i + 2][2]
                        bindestrich = tags[i + 1][0]
                        if (
                            (tag1 == 'NOUN' and tag2 == 'PUNCT' and bindestrich == '-' and tag3 == 'NOUN') or
                            (tag1 == 'NOUN' and tag2 == 'PUNCT' and bindestrich == '-' and tag3 == 'PROPN') or
                            (tag1 == 'PROPN' and tag2 == 'PUNCT' and bindestrich == '-' and tag3 == 'NOUN') or
                            (tag1 == 'PROPN' and tag2 == 'PUNCT' and bindestrich == '-' and tag3 == 'PROPN')
                            ):
                            original_words = [tags[i][0], tags[i + 1][0], tags[i + 2][0]]
                            
                            for word in original_words:
                                for keyword in keywords_mapping:
                                    if re.search(r'\b' + re.escape(keyword) + r'\b', word.lower()):
                                        filtered_splits.append(f"{keyword};{keywords_mapping[keyword]}")


                                             
                #Falls ein ein Split.Eintrag erstellt wird, wird der dazugehörige Speisenname, die Speisenbeschreibung und der Speisenpreis mit in die Liste der Speisen übertragen
                if filtered_splits:
                    filtered_dishes.append({
                        'speisenname': speisenname2,
                        'beschreibung': beschreibung2,
                        'splits_compound_adel': filtered_splits, 
                        'preis': preis
                    })
            # Nur wenn gefilterte Gerichte vorhanden sind, werden die gesamten Informationen der Restaurants mit den Speisen in die neue JSON übertragen
            if filtered_dishes:
                data = {
                    'restaurantname': restaurantname,
                    'url': url,
                    'kategorie': kategorie,
                    'straße': straße,
                    'stadt': stadt,
                    'plz': plz,
                    'latitude': latitude,
                    'longitude': longitude,
                    'bundesland': bundesland,
                    'speisen': filtered_dishes
                }
                json.dump(data, output_file, ensure_ascii=False, default=lambda x: str(x) if isinstance(x, Decimal) else x)
                output_file.write(',' + '\n')

        output_file.write(']')

    remove_last_comma(output_file_name)


