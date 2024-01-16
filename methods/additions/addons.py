"""
Hinzufügen vom Mittelwert jeder Wortlänge und Wortanzahl in den Speisenbeschreibungen

"""



import json


input_file_path = 'results/outputs_scraping_cleaning_pos/output4.json'  # Pfad der Eingabedatei
output_file_path = 'results/outputs_scraping_cleaning_pos/output5.json'  # Pfad der Ausgabedatei

with open(input_file_path, 'r', encoding='utf-8') as input_file, open(output_file_path, 'w', encoding='utf-8') as output_file:
    data = json.load(input_file)

    output_file.write('['+ ('\n'))

    updated_data = []
    for obj in data:
        speisen = obj['speisen']
        for speise in speisen:
            beschreibung = speise.get('beschreibung')
            if beschreibung:
                words = beschreibung.split() #Trennen der einzelnen Wörter der Beschreibung
                length_b = len(words) #Anzahl der Wörter bestimmen in den Bescreibungen
                avg_wl = sum(len(word) for word in words) / length_b if length_b > 0 else 0  #Durschnittliche Wortlänge jeder Beschreibung hinzufügen

                #Hinzufügen von neuen Einträgen lengt_b: Wörteranzahl der Beschreibung und avg_wl: Durschnittliche Wortlänge der Beschreibung zur JSON-Datei
                speise['length_b'] = length_b
                speise['avg_wl'] = avg_wl

        #Direktes Schreiben in die Ausgabedatei
        output_file.write(json.dumps(obj, ensure_ascii=False) + ',\n')

    
    output_file.write(']'+ ('\n'))

