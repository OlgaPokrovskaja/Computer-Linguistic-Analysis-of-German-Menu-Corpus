"""
Kombinieren der Teilkorpora zu einen gemeinsamen Korpus Teil 1

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

#Bestimmung der Input und Output-Pfade
input_file_name = 'results/outputs_scraping_cleaning_pos/output_basis.json'
output_file_name = 'methods/combine_outputs/full_output1.json'
file_name = 'results/outputs_language_aspects/ner_tagging.json'

#Einlesen der Eingabedateien und direktes Schreiben in die Ausgabedatei
with open(input_file_name, 'r', encoding='utf-8') as input_file, \
     open(file_name, 'r', encoding='utf-8') as ner_file, \
     open(output_file_name, 'w', encoding='utf-8') as output_file:

    output_file.write('[')

    #Üebrtragung der Eingabedaten in Listen
    kombiniert2_data = ijson.items(input_file, 'item')
    ner_tagging_data = list(ijson.items(ner_file, 'item'))

    #Suche nach einen Match durch den Vergleich von Restaurantnamen, Adresse und Geokoordinaten
    for entry in kombiniert2_data:
        restaurant_match = None
        for ner_entry in ner_tagging_data:
            if (entry['restaurantname'] == ner_entry['restaurantname'] and (get_value(entry, 'adresse_plz')[0] == ner_entry['plz']) and ((get_value(entry, 'adresse_stadt')[0] == ner_entry['stadt']) or (get_value(entry, 'adresse_stadt_p')[0] == ner_entry['stadt'])) and (get_value(entry, 'adresse_straße')[0] == ner_entry['straße']) or (get_value(entry, 'adresse_str_h') == ner_entry['straße']) and (get_value(entry, 'latitude') == get_value(ner_entry, 'latitude')) and (get_value(entry, 'longitude') == get_value(ner_entry, 'longitude'))):  # Hinzugefügt fehlende schließende Klammer
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
                            'pos_tags_s': get_value(g, 'pos_tags_s'),
                            'beschreibung': g['beschreibung'],
                            'pos_tags_b': get_value(g, 'pos_tags'),
                            'preis': get_value(g, 'preis'),
                            'length_b': get_value(g, 'length_b'),
                            'avg_wl_b': get_value(g, 'avg_wl'),
                            'ner_entity': get_value(ner_speise, 'entity')
                        })
                        found_match = True
                        break

                #Falls kein Match gefunden wurde, wird der Eintrag auf "None" gesetzt und die dazugehörigen Informtaionen der Speise werden übertragen
                if not found_match:
                    dishes.append({
                        'speisenname': g['speisenname'],
                        'pos_tags_s': get_value(g, 'pos_tags_s'),
                        'beschreibung': g['beschreibung'],
                        'pos_tags_b': get_value(g, 'pos_tags'),
                        'preis': get_value(g, 'preis'),
                        'length_b': get_value(g, 'length_b'),
                        'avg_wl_b': get_value(g, 'avg_wl'),
                        'ner_entity': 'None'
                    })

            #Einheitliche Anpassung der Adressinformationen
            stadt = get_value(entry, 'adresse_stadt')
            plz = get_value(entry, 'adresse_plz')
            straße = get_value(entry, 'adresse_straße')

            if stadt == "Undefined":
                stadt = get_value(entry, 'adresse_stadt_p')[0]

            if plz == "Undefined":
                plz = get_value(entry, 'adresse_stadt_p').split(' ')[0]

            if straße == "Undefined":
                straße = get_value(entry, 'adresse_str_h')

            #Übertragung der Restaurantinformationen
            output_entry = {
                "restaurantname": entry["restaurantname"],
                "kategorie": entry["kategorie"],
                "stadt": stadt,
                "plz": plz,
                "straße": straße,
                "url": get_value(entry, "url"),
                "datum": get_value(entry, "datum"),
                "latitude": get_value(entry, "latitude"),
                "longitude": get_value(entry, "longitude"),
                "bundesland": get_value(entry, "Bundesland"),
                "speisen": dishes
        
            }
     #Falls kein Match des Restaurants gefunden wurde, wird der Eintrag in die neue JSON-Datei übertragen mit dazugehörigen Informationen der Speise
        else:
            dishes = []
            for g in entry["speisen"]:
                dishes.append({
                    'speisenname': g['speisenname'],
                    'pos_tags_s': get_value(g, 'pos_tags_s'),
                    'beschreibung': g['beschreibung'],
                    'pos_tags_b': get_value(g, 'pos_tags'),
                    'preis': get_value(g, 'preis'),
                    'length_b': get_value(g, 'length_b'),
                    'avg_wl_b': get_value(g, 'avg_wl'),
                    'ner_entity': 'None'
                })

            #Einheitliche Anpassung der Adressinformationen
            stadt = get_value(entry, 'adresse_stadt')
            plz = get_value(entry, 'adresse_plz')
            straße = get_value(entry, 'adresse_straße')

            if stadt == "Undefined":
                stadt = get_value(entry, 'adresse_stadt_p')[0]

            if plz == "Undefined":
                plz = get_value(entry, 'adresse_stadt_p').split(' ')[0]

            if straße == "Undefined":
                straße = get_value(entry, 'adresse_str_h')

            #Übertragung der Restaurantinformationen
            output_entry = {
                "restaurantname": entry["restaurantname"],
                "kategorie": entry["kategorie"],
                "stadt": stadt,
                "plz": plz,
                "straße": straße,
                "url": get_value(entry, "url"),
                "datum": get_value(entry, "datum"),
                "latitude": get_value(entry, "latitude"),
                "longitude": get_value(entry, "longitude"),
                "bundesland": get_value(entry, "Bundesland"),
                "speisen": dishes
            }

        json.dump(output_entry, output_file, ensure_ascii=False, default=lambda x: str(x) if isinstance(x, Decimal) else x)
        output_file.write(',' + '\n')


    output_file.write(']')

remove_last_comma(output_file_name)

