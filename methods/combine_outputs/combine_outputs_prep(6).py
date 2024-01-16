"""
Kombinieren der Teilkorpora zu einen gemeinsamen Korpus Teil 6

"""


import ijson
import json
from decimal import Decimal

#Methode, um einen Default-Wert = "Undefined" zu setzen, falls ein Aspekt nicht vorhanden ist 
def get_value(obj, key, default="Undefined"):
    return obj[key] if key in obj else default

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

#Bestimmung der Input und Output-Pfad
input_file_name = 'methods/combine_outputs/full_output5.json'
output_file_name = 'methods/combine_outputs/full_output6.json'
file_name = 'results/outputs_language_aspects/region.json'

#Einlesen der Eingabedateien und direktes Schreiben in die Ausgabedatei
with open(input_file_name, 'r', encoding='utf-8') as input_file, \
     open(file_name, 'r', encoding='utf-8') as ner_file, \
     open(output_file_name, 'w', encoding='utf-8') as output_file:

    output_file.write('[')

    #Übertragung der Eingabedaten in Listen
    kombiniert2_data = ijson.items(input_file, 'item')
    ner_tagging_data = list(ijson.items(ner_file, 'item'))

    #Suche nach einen Match durch die URL
    for entry in kombiniert2_data:
        restaurant_match = None
        for ner_entry in ner_tagging_data:
            if (entry['url'] == ner_entry['url']):
                restaurant_match = ner_entry
                break

        #Falls ein Match gefunden wurde, wird der Eintrag in die neue JSON-Datei übertragen mit dazugehörigen Informationen der Speise
        if restaurant_match:
            dishes = []
            for g in entry["speisen"]:
                ner_speisen = restaurant_match['speisen']
                found_match = False
                for ner_speise in ner_speisen:
                    g_beschreibung = g.get('beschreibung', '')
                    ner_beschreibung = ner_speise.get('beschreibung', '')

                    #Überprüfung der Übereinstimmung des Speisennamen und Speisenbeschreibungen
                    if g['speisenname'] == ner_speise['speisenname'] and g_beschreibung == ner_beschreibung:
                        dishes.append({
                            'speisenname': g['speisenname'],
                            'pos_tags_s': g['pos_tags_s'],
                            'beschreibung': g['beschreibung'],
                            'pos_tags_b': g['pos_tags_b'],
                            'preis': g['preis'],
                            'length_b': g['length_b'],
                            'avg_wl_b': g['avg_wl_b'],
                            'ner_entity': g['ner_entity'],
                            'splits_person_ruf': g['splits_person_ruf'],
                            'splits_person_name': g['splits_person_name'],
                            'splits_region': g['splits_region'],
                            'splits_home': g['splits_home'],
                            'splits_prep': get_value(ner_speise, 'splits_prep')
                        })
                        found_match = True
                        break
                #Falls kein Match gefunden wurde, wird der Eintrag auf "None" gesetzt und die dazugehörigen Informtaionen der Speise werden übertragen    
                if not found_match:
                    dishes.append({
                        'speisenname': g['speisenname'],
                        'pos_tags_s': g['pos_tags_s'],
                        'beschreibung': g['beschreibung'],
                        'pos_tags_b': g['pos_tags_b'],
                        'preis': g['preis'],
                        'length_b': g['length_b'],
                        'avg_wl_b': g['avg_wl_b'],
                        'ner_entity': g['ner_entity'],
                        'splits_person_ruf': g['splits_person_ruf'],
                        'splits_person_name': g['splits_person_name'],
                        'splits_region': g['splits_region'],
                        'splits_home': g['splits_home'],
                        'splits_prep': 'None'
                    })


            #Übertragung der Restaurantinformationen
            output_entry = {
                'restaurantname': entry['restaurantname'],
                'kategorie': entry['kategorie'],
                'stadt': entry['stadt'],
                'plz': entry['plz'],
                'straße': entry['straße'],
                'url': entry['url'],
                'datum': entry['datum'],
                'latitude': entry['latitude'],
                'longitude': entry['longitude'],
                'bundesland': entry['bundesland'],
                "speisen": dishes
            }
        #Falls kein Match des Restaurants gefunden wurde, wird der Eintrag in die neue JSON-Datei übertragen mit dazugehörigen Informationen der Speise
        else:
            dishes = []
            for g in entry["speisen"]:
                dishes.append({
                    'speisenname': g['speisenname'],
                    'pos_tags_s': g['pos_tags_s'],
                    'beschreibung': g['beschreibung'],
                    'pos_tags_b': g['pos_tags_b'],
                    'preis': g['preis'],
                    'length_b': g['length_b'],
                    'avg_wl_b': g['avg_wl_b'],
                    'ner_entity': g['ner_entity'],
                    'splits_person_ruf': g['splits_person_ruf'],
                    'splits_person_name': g['splits_person_name'],
                    'splits_region': g['splits_region'],
                    'splits_home': g['splits_home'],
                    'splits_prep': 'None'
                })


            #Übertragung der Restaurantinformationen
            output_entry = {
                'restaurantname': entry['restaurantname'],
                'kategorie': entry['kategorie'],
                'stadt': entry['stadt'],
                'plz': entry['plz'],
                'straße': entry['straße'],
                'url': entry['url'],
                'datum': entry['datum'],
                'latitude': entry['latitude'],
                'longitude': entry['longitude'],
                'bundesland': entry['bundesland'],
                "speisen": dishes
            }

        json.dump(output_entry, output_file, ensure_ascii=False, default=lambda x: str(x) if isinstance(x, Decimal) else x)
        output_file.write(',' + '\n')


    output_file.write(']')

remove_last_comma(output_file_name)
