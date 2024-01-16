"""
Hinzufügen von Koordinaten nach den Mittelpunkt der PLZ

"""


import csv
import json

#Einlesen der csv Datei mit PLZ, latitude und langitude
def load_csv(csv_filename):
    csv_data = {}
    with open(csv_filename, 'r', encoding='ISO-8859-1') as file:
        reader = csv.DictReader(file)
        for row in reader:
            plz = row['zip']
            lat = float(row['lat'])
            lng = float(row['lng'])
            csv_data[plz] = {'lat': lat, 'lng': lng}
    return csv_data

def update_json(csv_data, json_filename, json_filename_new):
    with open(json_filename, 'r', encoding='utf-8') as inputfile:
        data = json.load(inputfile)
        not_found = []  # Liste für nicht gefundene PLZ und Stadt
        
        with open(json_filename_new, 'w', encoding='utf-8') as outputfile:
            outputfile.write('[')
            
            for item in data:
                if 'adresse_plz' in item:
                    plz = item['adresse_plz'][0]  # PLZ als erstes Element der Liste extrahieren
                    
                    if plz in csv_data:
                        item['latitude'] = csv_data[plz]['lat']
                        item['longitude'] = csv_data[plz]['lng']
                    
                    else:
                        not_found.append(f"{plz} - {item['adresse_stadt'][0]}")
                
                elif 'adresse_stadt_p' in item:
                    plz = item['adresse_stadt_p'][0]
                    plznew = plz.split(' ')[0]
                    plzstadt = plz
        
                    if plznew in csv_data:
                        item['latitude'] = csv_data[plznew]['lat']
                        item['longitude'] = csv_data[plznew]['lng']
                    
                    else:
                        not_found.append(f"{plznew} - {plzstadt}")
            
                outputfile.write(json.dumps(item, ensure_ascii=False))
                outputfile.write(',' + '\n')
            outputfile.write(']')
        

    with open('not_found.txt', 'w', encoding='utf-8') as file:
        for item in not_found:
            file.write(item + '\n')
        
#Entfernen des letztes Komma nach den schreiben in die Ausgangsdatei
def remove_last_comma(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    if len(lines) >= 2:
        second_last_line = lines[-2].rstrip()
        if second_last_line.endswith(','):
            lines[-2] = second_last_line[:-1]

    with open(json_file, 'w', encoding='utf-8') as file:
        file.writelines(lines)

#Input und Output-Pfade bestimmen
csv_filename = 'datasets/lang_long.csv'
json_filename = 'results/outputs_scraping_cleaning_pos/output6.json'
json_filename_new = 'results/outputs_scraping_cleaning_pos/output7.json'

#Aufrufen der Methoden
csv_data = load_csv(csv_filename)
update_json(csv_data, json_filename, json_filename_new)
remove_last_comma(json_filename_new)
