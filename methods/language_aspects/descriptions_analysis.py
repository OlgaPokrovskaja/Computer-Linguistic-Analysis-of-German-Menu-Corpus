"""
Erstellung des Teilkorpus "descriptions_output" zur detaillierten Analyse der Speisenbeschreibungen
"""

import json
import re

#Einheitliches Konvertieren der Restaurantadresse
def get_address(restaurant):
    if 'adresse_stadt' in restaurant:
        stadt = restaurant['adresse_stadt'][0]
    elif 'adresse_stadt_p' in restaurant:
        plz = restaurant['adresse_stadt_p'].split(' ')[0]
        stadt = restaurant['adresse_stadt_p'][0]
    else:
        stadt = None

    if 'adresse_plz' in restaurant:
        plz = restaurant['adresse_plz'][0]
    else:
        plz = None

    if 'adresse_straße' in restaurant:
        straße = restaurant['adresse_straße'][0]
    elif 'adresse_str_h' in restaurant:
        straße = restaurant['adresse_str_h']
    else:
        straße = None

    return stadt, plz, straße

#Methode zum Bestimmen der einzelnen Wortlängen und der Wortanzahl
def process_restaurants(restaurants):
    items = []
    
    for restaurant in restaurants:
        item = {}
        
        #Übertragung der Restaurantinformationen Restaurantname, Kategorie, URL, Datum, Geokoordinaten und Bundesland
        item['restaurantname'] = restaurant['restaurantname']
        item['kategorie'] = restaurant['kategorie']
        item['url'] = restaurant['url']
        item['datum'] = restaurant['datum']
        if "latitude" in restaurant:
            item['latitude'] = restaurant['latitude']
        if "longitude" in restaurant:
            item['longitude'] = restaurant['longitude']
        if 'Bundesland' in restaurant:
            item['Bundesland'] = restaurant['Bundesland']
        else:
            item['Bundesland'] = "Undefined"

        #Aufrufen der Methode get_adress
        stadt, plz, straße = get_address(restaurant)
        item['adresse_stadt'] = stadt
        item['adresse_plz'] = plz
        item['adresse_straße'] = straße

        speisen = restaurant['speisen']
        processed_speisen = []

        #Setzen der zu berechnenden Werte
        shortest_word = None
        longest_word = None
        shortest_word_price = None
        shortest_word_length = None
        longest_word_price = None
        longest_word_length = None
        total_description_length = 0
        total_word_length = 0
        total_number_of_dishes = 0
        shortest_description = None
        shortest_word_count = None
        longest_description = None
        longest_word_count = None
        total_price = 0
        

        for speise in speisen:
            processed_speise = {}
            
            price = speise['preis']
            total_price += price

            #Speisennamen und Speisenbeschreibungen extrahieren
            if speise["beschreibung"] == "":
                description = speise['speisenname']
            else:
                description = speise['beschreibung']  

            #Regex zum finden von allen Wörtern ohne Satzzeichen
            words = re.findall(r'\b\w+\b', description)

            #Anzahl der Wörter in der Beschreibung speichern
            word_count = len(words)
            total_description_length += word_count

            #Suche nach der kürzesten und längsten Beschreibung der Restaurant_Speisekarte
            if shortest_description is None or word_count < shortest_word_count:
                shortest_description = description
                shortest_word_count = word_count

            if longest_description is None or word_count > longest_word_count:
                longest_description = description
                longest_word_count = word_count

            #Durchschnitlliche Wortlänge berechnen
            if "avg_wl" in speise:
                avg_wl = speise['avg_wl']
            elif word_count > 0:
                avg_wl = sum(len(word) for word in words) / word_count
            else:
                avg_wl = 0

            #Erhöhung der Gesamtlänge der Wörter 
            total_word_length += float(avg_wl)
            #Erhöhen der Anzahl der Speisen
            total_number_of_dishes += 1

            #Wenn die Beschreibung leer ist, wird in den Speisennamen nach den kürzesten und längsten Wort gesucht und den dazugehörigen Speisenpreis mit den kürzesten/längsten Wort
            if speise["beschreibung"] == "":
                words = re.findall(r'\b\w+\b', speise['speisenname'])
                for word in words:
                    if len(word) >= 2 and word.isalpha():
                        if shortest_word is None or len(word) < len(shortest_word):
                            shortest_word = word
                            shortest_word_length = len(shortest_word)
                            shortest_word_price = speise['preis']

                        if longest_word is None or len(word) > len(longest_word):
                            longest_word = word
                            longest_word_length = len(longest_word)
                            longest_word_price = speise['preis']

            #Wenn die Beschreibung  nicht leer ist, wird in den Speisennamen nach den kürzesten und längsten Wort gesucht und den dazugehörigen Speisenpreis mit den kürzesten/längsten Wort
            else:
                words = re.findall(r'\b\w+\b', speise['beschreibung'])
                for word in words:
                    if len(word) >= 2 and word.isalpha():
                        if shortest_word is None or len(word) < len(shortest_word):
                            shortest_word = word
                            shortest_word_length = len(shortest_word)
                            shortest_word_price = speise['preis']

                        if longest_word is None or len(word) > len(longest_word):
                            longest_word = word
                            longest_word_length = len(longest_word)
                            longest_word_price = speise['preis']

            processed_speisen.append(processed_speise)

        #Durchschnittliche Wortanzahl, Wortlänge und Speisenpreis des Restaurants berechnen
        average_description_length = total_description_length / len(speisen)
        average_word_length = total_word_length / total_number_of_dishes
        average_price = total_price / len(speisen)
        


        
        #JSON-Einträge erstellen
        item['shortest_description'] = shortest_description
        item['shortest_description_length'] = shortest_word_count
        item['longest_description'] = longest_description
        item['longest_description_length'] = longest_word_count
        item['shortest_word'] = shortest_word
        item['shortest_word_price'] = shortest_word_price
        item['shortest_word_length'] = shortest_word_length
        item['longest_word'] = longest_word
        item['longest_word_price'] = longest_word_price
        item['longest_word_length'] = longest_word_length
        item['average_description_length'] = average_description_length
        item['average_word_length'] = average_word_length
        item['average_price'] = average_price

        items.append(item)

    return items

#Methode zum Schreiben in die Output-Datei
def write_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


#Main Methode zum Aufrufen des Programms
def main():
    with open('results/outputs_scraping_cleaning_pos/output_basis.json', 'r', encoding='utf-8') as file:
        json_data = json.load(file)


    processed_items = process_restaurants(json_data)


    write_to_json(processed_items, 'results/outputs_language_aspects/descriptions_output.json')

if __name__ == '__main__':
    main()
