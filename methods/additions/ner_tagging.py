"""
Hinzufügen von NER-Tags zu den Scpeisenbeschreibungen und Speisennamen mit Stanza

"""

import stanza
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

#Definition der Stanza-Pipeline, mit batch_size für weniger Überlastung
nlp = stanza.Pipeline(lang='de', processors='tokenize, mwt, ner',  package={"ner": ["germeval2014"]}, pos_batch_size=500)

#Bestimmung der Input und Output-Pfade
input_file_name = 'results/outputs_scraping_cleaning_pos/output_basis.json' 
output_file_name = 'results/outputs_language_aspects/ner_tagging.json'

#Einlesen der Input-Datei
with open(input_file_name, 'r', encoding='utf-8') as input_file:
    json_data = ijson.items(input_file, 'item')
    
    #Direktes Schreiben in die Output-Datei
    with open(output_file_name, 'w', encoding='utf-8') as output_file:
        output_file.write('[')
        
        #Übertragung der Kategorie, des Bundeslandes, latitude und longitude, sowie einheitliche Formatierung der Stadt, PLZ und Straße
        for obj in json_data:
            kategorie = obj["kategorie"]
            
            if "Bundesland" in obj:
                bundesland = obj["Bundesland"]
            else:
                bundesland = "Undefined"

            restaurantname = obj["restaurantname"]

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
            
            filtered_dishes = []  # Liste für die gefilterten Gerichte pro Datenobjekt

            #Umwandlung der Lemmata in eine Liste
            for dish in obj["speisen"]:
                speisen = []
                beschreiben = []
                if 'pos_tags_s' in dish:
                    speisenname = dish['pos_tags_s']
                    for speise in speisenname:
                        speisen.append(speise[1])
                elif 'pos_tags' in dish: 
                    beschreibung = dish['pos_tags']
                    for besch in beschreibung:
                        beschreiben.append(besch[1])
                
                #Speichern der Orginalschreibweise der Speisennamen und Speisenbeschreibungen
                speisenname2 = dish['speisenname']
                beschreibung2 = dish['beschreibung']
                
                #Umwandlung des Preises in eine Gelitkommazahl
                preis = float(dish['preis'])

                #Bestimmung der Liste der lemmatisierten Wörter als docs für NER-Tagging
                doc = nlp(' '.join(speisen))  # Liste in Text umwandeln
                doc2 = nlp(' '.join(beschreiben))  # Liste in Text umwandeln

                entity = []  # Liste für die gefundenen Entities pro Gericht

                #Falls ein NER-Tag gesetzt werden konnte, wird ein neuer entity Eintrag in der JSON hinzugefügt
                for ent in doc.ents:
                    if ent: 
                        entity.append((ent.text, ent.type))

                for ent2 in doc2.ents:
                    if ent2:
                        entity.append((ent2.text, ent2.type))
                
                #Falls ein NER-Eintrag erstellt wird, wird der dazugehörige Speisenname, die Speisenbeschreibung und der Speisenpreis mit in die Liste der Speisen übertragen
                if entity:
                    filtered_dishes.append({
                        'speisenname': speisenname2,
                        'beschreibung': beschreibung2,
                        'entity': entity,
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
