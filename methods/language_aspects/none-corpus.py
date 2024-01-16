"""
Erstellung des Teilkorpus 'None' (Restaurants und Speisen mit keinen einzigen Sprachaspekt)

"""


import ijson
import json
from decimal import Decimal


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

#Bestimmung der Input und Output-Pfade
input_file_name = 'results/output_full.json'
output_file_name = 'results/outputs_language_aspects/none-corpus.json'


#Einlesen der Input-Datei
with open(input_file_name, 'r', encoding='utf-8') as input_file:
    json_data = ijson.items(input_file, 'item')

    #Direktes Schreiben in die Output-Datei
    with open(output_file_name, 'w', encoding='utf-8') as output_file:
        output_file.write('[')

         #Übertragung der Kategorie, des Bundeslandes, latitude und longitude, URL,  sowie einheitliche Formatierung der Stadt, PLZ und Straße
        for obj in json_data:
            kategorie = obj["kategorie"]

            if "bundesland" in obj:
                bundesland = obj["bundesland"]
            else:
                bundesland = "Undefined"

            restaurantname = obj["restaurantname"]
            url = obj["url"]

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

            

            filtered_dishes = [] # Liste für die gefilterten Gerichte pro Datenobjekt
            skip_restaurant = False #Setzen der Varible auf Default-Wert "False" zum überspringen von Restaurants

            #Filtern der Einträge bei welchen bei allen Sprachaspekten "None" steht, Restaurant wird übersprungen, falls nur eine einzige Speise diese Bedingung nicht erfüllt
            for dish in obj["speisen"]:
                if any(
                    dish[key] != 'None'
                    for key in ['splits_person_ruf', 'splits_person_name', 'splits_region', 'splits_home', 'splits_prep', 'splits_adj', 'splits_dialekte', 'splits_compound_split', 'splits_compound_bind', 'splits_inter_adel']
                ):
                    skip_restaurant = True
                    break

            #Falls alle Splits "None" sind, werden Speisenname, Speisenbeschreibung und Speisenpreis als Gleitkommazahl in die neue JSON-Datei übertragen
            if not skip_restaurant:
                    for dish in obj["speisen"]:
                        filtered_dishes.append({
                            'speisenname': dish['speisenname'],
                            'beschreibung': dish['beschreibung'],
                            'preis': float(dish['preis'])
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


