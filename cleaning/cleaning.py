
"""
Bereinigung des entstandenen Korpus.
Falls keine Speisekarte im Restaurant vorhanden ist, wird das Restaurant entfernt.
Behebung des Scraping-Fehlers bei den Speisenbeschreibungen.
Zusammenführung von Zusatzbeschreibungen zur einer Speisenbeschreibungen.
Entfernung von Sonderzeichen in Speisennamen und Speisenbeschreibungen.
Extrahierung des Speisenpreis aus den Speisenbeschhreibungen, falls nicht im extra HTML-Container
"""


import ijson
import json
import re

input_file_path = 'results/outputs/output_basis.json'  #Pfad der Eingabedatei 
output_file_path = 'results/outputs/output_basis_cleaned.json'  #Pfad der Ausgabedatei 

with open(input_file_path, 'r', encoding='utf-8') as input_file, open(output_file_path, 'w', encoding='utf-8') as output_file:
    json_objects = ijson.items(input_file, 'item')


    for obj in json_objects:
        #nur falls eine Speisekarte vorhanden ist, wird es in die neue Datei übertragen
        if obj['speisen']:
            for speise in obj['speisen']:
                string = speise['beschreibung']

                #Behebung des Scraping Fehlers (Jede Beschreibung war doppelt abgespeichert, falls kein <br> in der HTML vorhanden war):
                repeat_string = string[:len(string) // 2]  # Erster Teil des Strings bis zur Hälfte
                if repeat_string in string and string.count(repeat_string) > 1:  # Überprüfen, ob repeat_string doppelt vorkommt
                    substring = string.replace(repeat_string, '', 1)  # Ersetzen mit nichts (nur das erste Vorkommen entfernen)
                    speise['beschreibung'] = substring.strip() #Beschreibung überschreiben 
                
                #Falls ein speisen_zusatz vorhanden ist, Liste zu einen String zusammenfügen getrennt mit Komma und zu der Beschreibung hinzufügen 
                try: 
                    trennzeichen = ', '
                    list = speise['speisen_zusatz']
                    strings = speise['beschreibung']
                    if strings:
                        speise['beschreibung'] = strings.strip() + ", " + trennzeichen.join(list).strip()
                    else:
                        speise['beschreibung'] = trennzeichen.join(list)

                    del speise['speisen_zusatz']

                except:
                    None
                    
                #Entfernen von einigen Zeichen und aufeinanderfolgenden Whitespaces in der Beschreibung:
                noch_ein_string = speise['beschreibung']
                noch_ein_string = noch_ein_string.replace('\t', ' ').replace('"', ' ').replace('•', ' ').replace('„', ' ').replace('“', ' ').replace('\\', ' ').replace('/', ' ').replace('——', ' ').replace('|', ' ').replace('«', ' ').replace('»',' ').replace('‹',' ').replace('›',' ').replace('€', ' ').replace('+', ' ').strip()
                speise['beschreibung'] = re.sub(r"\s+", " ", noch_ein_string)   

                #Entfernen von einigen Zeichen und aufeinanderfolgenden Whitespaces in den Speisennamen:
                second_string = speise['speisenname']
                second_string = second_string.replace('\t', ' ').replace('"', ' ').replace('•', ' ').replace('„', ' ').replace('“', ' ').replace('\\', ' ').replace('/', ' ').replace('——', ' ').replace('|', ' ').replace('«', '').replace('»',' ').replace('‹',' ').replace('›',' ').replace('€', ' ').replace('+', ' ').strip()
                speise['speisenname'] = re.sub(r"\s+", " ", second_string)

                #Falls ein Preis in den Speisennamen vorhanden ist, wird er zum 'preis' übertragen 
                speisenname = speise['speisenname']
                price_match = re.search(r'(\d+\,\d+)', speisenname) #finden von Zahlen getrennt durch Kommata
                if price_match:
                    price = price_match.group(1)
                    speise['preis'] = price.replace(',', '.') #vereinheitlichen der Preise, wie bei allen Einträgen
                    speise['speisenname'] = speisenname.replace(price, "").strip() #rauslöschen von den Preis aus den Speisennamen, sowie € Zeichen 
                
                #Äquivalent zum Code-Snippet zuvor, nur mit Beschreibungen
                beschreibung = speise['beschreibung']
                price_matchh = re.search(r'(\d+\,\d+)', beschreibung)
                if price_matchh:
                    preis = price_matchh.group(1)
                    speise['preis'] = preis.replace(',', '.')
                    speise['beschreibung'] = speisenname.replace(preis, "").strip()


            
         
            output_file.write(json.dumps(obj, ensure_ascii=False) + ',' + ('\n')) #Schreiben in die neue Datei


