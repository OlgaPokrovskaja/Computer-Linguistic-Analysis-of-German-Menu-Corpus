"""
Daten für deskriptive Analyse der Sprachaspekte zu generieren

"""


import json


#Einlesen der Input-Datei
def read_json_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        return json.load(file)


#Deskriptive Werte berechnen
def count_words_and_avg_length(data):
    total_words_speisenname = 0
    total_words_beschreibung = 0
    total_length_speisenname_no_punctuation = 0
    total_length_beschreibung_no_punctuation = 0
    total_word_count_speisenname = 0
    total_word_count_beschreibung = 0
    total_price = 0

    total_dish_entries = sum(len(entry.get('speisen', [])) for entry in data)

    for entry in data:
        for dish in entry.get('speisen', []):
            speisenname_words = dish.get('speisenname', '').split()
            beschreibung_words = dish.get('beschreibung', '').split()

            total_words_speisenname += len([word for word in speisenname_words if word.isalnum()])
            total_words_beschreibung += len([word for word in beschreibung_words if word.isalnum()])

            for word in speisenname_words:
                # Zählen der Länge ohne Satzzeichen für Speisennamen
                word_no_punctuation = ''.join(char for char in word if char.isalnum())
                total_length_speisenname_no_punctuation += len(word_no_punctuation)
                total_word_count_speisenname += 1

            for word in beschreibung_words:
                # Zähle der Länge ohne Satzzeichen für Beschreibungen
                word_no_punctuation = ''.join(char for char in word if char.isalnum())
                total_length_beschreibung_no_punctuation += len(word_no_punctuation)
                total_word_count_beschreibung += 1
            
            total_price += dish.get('preis', 0)

    avg_words_speisenname = total_words_speisenname / total_dish_entries 
    avg_words_beschreibung = total_words_beschreibung / total_dish_entries 
    avg_length_speisenname_no_punctuation = total_length_speisenname_no_punctuation / total_word_count_speisenname 
    avg_length_beschreibung_no_punctuation = total_length_beschreibung_no_punctuation / total_word_count_beschreibung
    avg_price = total_price / total_dish_entries

    return avg_words_speisenname, avg_words_beschreibung, avg_length_speisenname_no_punctuation, avg_length_beschreibung_no_punctuation, avg_price


#Definition der Input-Dateien und Aufruf der Methode

file_name1 = 'results/outputs_language_aspects/adjectives.json'  
json_data1 = read_json_file(file_name1)
avg_words_speisenname1, avg_words_beschreibung1, avg_length_speisenname_no_punctuation1, avg_length_beschreibung_no_punctuation1, avg_price1 = count_words_and_avg_length(json_data1)

print(f"adjectives: Durchschnittliche Anzahl der Wörter in Speisennamen: {avg_words_speisenname1}")
print(f"adjectives: Durchschnittliche Anzahl der Wörter in Beschreibungen: {avg_words_beschreibung1}")
print(f"adjectives: Durchschnittliche Länge der Wörter ohne Satzzeichen in Speisennamen: {avg_length_speisenname_no_punctuation1}")
print(f"adjectives: Durchschnittliche Länge der Wörter ohne Satzzeichen in Beschreibungen: {avg_length_beschreibung_no_punctuation1}")
print(f"adjectives: Durchschnittlicher Preis: {avg_price1}")


file_name2 = 'results/outputs_language_aspects/homemade.json'  

json_data2 = read_json_file(file_name2)
avg_words_speisenname2, avg_words_beschreibung2, avg_length_speisenname_no_punctuation2, avg_length_beschreibung_no_punctuation2, avg_price2 = count_words_and_avg_length(json_data2)

print(f"hausgemacht: Durchschnittliche Anzahl der Wörter in Speisennamen: {avg_words_speisenname2}")
print(f"hausgemacht: Durchschnittliche Anzahl der Wörter in Beschreibungen: {avg_words_beschreibung2}")
print(f"hausgemacht: Durchschnittliche Länge der Wörter ohne Satzzeichen in Speisennamen: {avg_length_speisenname_no_punctuation2}")
print(f"hausgemacht: Durchschnittliche Länge der Wörter ohne Satzzeichen in Beschreibungen: {avg_length_beschreibung_no_punctuation2}")
print(f"hausgemacht: Durchschnittlicher Preis: {avg_price2}")


file_name4 = 'results/outputs_language_aspects/preposition.json'  

json_data4 = read_json_file(file_name4)
avg_words_speisenname4, avg_words_beschreibung4, avg_length_speisenname_no_punctuation4, avg_length_beschreibung_no_punctuation4, avg_price4 = count_words_and_avg_length(json_data4)

print(f"prep: Durchschnittliche Anzahl der Wörter in Speisennamen: {avg_words_speisenname4}")
print(f"prep: Durchschnittliche Anzahl der Wörter in Beschreibungen: {avg_words_beschreibung4}")
print(f"prep: Durchschnittliche Länge der Wörter ohne Satzzeichen in Speisennamen: {avg_length_speisenname_no_punctuation4}")
print(f"prep: Durchschnittliche Länge der Wörter ohne Satzzeichen in Beschreibungen: {avg_length_beschreibung_no_punctuation4}")
print(f"prep: Durchschnittlicher Preis: {avg_price4}")


file_name5 = 'results/outputs_language_aspects/region.json'  

json_data5 = read_json_file(file_name5)
avg_words_speisenname5, avg_words_beschreibung5, avg_length_speisenname_no_punctuation5, avg_length_beschreibung_no_punctuation5, avg_price5  = count_words_and_avg_length(json_data5)

print(f"region: Durchschnittliche Anzahl der Wörter in Speisennamen: {avg_words_speisenname5}")
print(f"region: Durchschnittliche Anzahl der Wörter in Beschreibungen: {avg_words_beschreibung5}")
print(f"region: Durchschnittliche Länge der Wörter ohne Satzzeichen in Speisennamen: {avg_length_speisenname_no_punctuation5}")
print(f"region: Durchschnittliche Länge der Wörter ohne Satzzeichen in Beschreibungen: {avg_length_beschreibung_no_punctuation5}")
print(f"region: Durchschnittlicher Preis: {avg_price5}")

file_name6 = 'results/outputs_language_aspects/dialekte.json'  

json_data6 = read_json_file(file_name6)
avg_words_speisenname6, avg_words_beschreibung6, avg_length_speisenname_no_punctuation6, avg_length_beschreibung_no_punctuation6, avg_price6  = count_words_and_avg_length(json_data6)

print(f"dialect: Durchschnittliche Anzahl der Wörter in Speisennamen: {avg_words_speisenname6}")
print(f"dialect: Durchschnittliche Anzahl der Wörter in Beschreibungen: {avg_words_beschreibung6}")
print(f"dialect: Durchschnittliche Länge der Wörter ohne Satzzeichen in Speisennamen: {avg_length_speisenname_no_punctuation6}")
print(f"dialect: Durchschnittliche Länge der Wörter ohne Satzzeichen in Beschreibungen: {avg_length_beschreibung_no_punctuation6}")
print(f"dialect: Durchschnittlicher Preis: {avg_price6}")


file_name8 = 'results/outputs_language_aspects/personen_ruf.json'  

json_data8 = read_json_file(file_name8)
avg_words_speisenname8, avg_words_beschreibung8, avg_length_speisenname_no_punctuation8, avg_length_beschreibung_no_punctuation8, avg_price8  = count_words_and_avg_length(json_data8)

print(f"person_ruf: Durchschnittliche Anzahl der Wörter in Speisennamen: {avg_words_speisenname8}")
print(f"person_ruf: Durchschnittliche Anzahl der Wörter in Beschreibungen: {avg_words_beschreibung8}")
print(f"person_ruf: Durchschnittliche Länge der Wörter ohne Satzzeichen in Speisennamen: {avg_length_speisenname_no_punctuation8}")
print(f"person_ruf: Durchschnittliche Länge der Wörter ohne Satzzeichen in Beschreibungen: {avg_length_beschreibung_no_punctuation8}")
print(f"person_ruf: Durchschnittlicher Preis: {avg_price8}")

file_name9 = 'results/outputs_language_aspects/personen_name.json'  

json_data9 = read_json_file(file_name9)
avg_words_speisenname9, avg_words_beschreibung9, avg_length_speisenname_no_punctuation9, avg_length_beschreibung_no_punctuation9, avg_price9  = count_words_and_avg_length(json_data9)

print(f"person_name: Durchschnittliche Anzahl der Wörter in Speisennamen: {avg_words_speisenname9}")
print(f"person_name: Durchschnittliche Anzahl der Wörter in Beschreibungen: {avg_words_beschreibung9}")
print(f"person_name: Durchschnittliche Länge der Wörter ohne Satzzeichen in Speisennamen: {avg_length_speisenname_no_punctuation9}")
print(f"person_name: Durchschnittliche Länge der Wörter ohne Satzzeichen in Beschreibungen: {avg_length_beschreibung_no_punctuation9}")
print(f"person_name: Durchschnittlicher Preis: {avg_price9}")


file_name10 = 'results/outputs_language_aspects/compounds_adel_deutsch_split.json'  

json_data10 = read_json_file(file_name10)
avg_words_speisenname10, avg_words_beschreibung10, avg_length_speisenname_no_punctuation10, avg_length_beschreibung_no_punctuation10, avg_price10  = count_words_and_avg_length(json_data10)

print(f"compound_split: Durchschnittliche Anzahl der Wörter in Speisennamen: {avg_words_speisenname10}")
print(f"compound_split: Durchschnittliche Anzahl der Wörter in Beschreibungen: {avg_words_beschreibung10}")
print(f"compound_split: Durchschnittliche Länge der Wörter ohne Satzzeichen in Speisennamen: {avg_length_speisenname_no_punctuation10}")
print(f"compound_split: Durchschnittliche Länge der Wörter ohne Satzzeichen in Beschreibungen: {avg_length_beschreibung_no_punctuation10}")
print(f"compound_split: Durchschnittlicher Preis: {avg_price10}")

file_name11 = 'results/outputs_language_aspects/compounds_adel_deutsch.json'  

json_data11 = read_json_file(file_name11)
avg_words_speisenname11, avg_words_beschreibung11, avg_length_speisenname_no_punctuation11, avg_length_beschreibung_no_punctuation11, avg_price11  = count_words_and_avg_length(json_data11)

print(f"compound_bind: Durchschnittliche Anzahl der Wörter in Speisennamen: {avg_words_speisenname11}")
print(f"compound_bind: Durchschnittliche Anzahl der Wörter in Beschreibungen: {avg_words_beschreibung11}")
print(f"compound_bind: Durchschnittliche Länge der Wörter ohne Satzzeichen in Speisennamen: {avg_length_speisenname_no_punctuation11}")
print(f"compound_bind: Durchschnittliche Länge der Wörter ohne Satzzeichen in Beschreibungen: {avg_length_beschreibung_no_punctuation11}")
print(f"compound_bind: Durchschnittlicher Preis: {avg_price11}")


file_name12 = 'results/outputs_language_aspects/international_adel.json'  

json_data12 = read_json_file(file_name12)
avg_words_speisenname12, avg_words_beschreibung12, avg_length_speisenname_no_punctuation12, avg_length_beschreibung_no_punctuation12, avg_price12  = count_words_and_avg_length(json_data12)

print(f"inter: Durchschnittliche Anzahl der Wörter in Speisennamen: {avg_words_speisenname12}")
print(f"inter: Durchschnittliche Anzahl der Wörter in Beschreibungen: {avg_words_beschreibung12}")
print(f"inter: Durchschnittliche Länge der Wörter ohne Satzzeichen in Speisennamen: {avg_length_speisenname_no_punctuation12}")
print(f"inter: Durchschnittliche Länge der Wörter ohne Satzzeichen in Beschreibungen: {avg_length_beschreibung_no_punctuation12}")
print(f"inter: Durchschnittlicher Preis: {avg_price12}")


file_name13 = 'results/outputs_scraping_cleaning_pos/output_basis.json' 

json_data13 = read_json_file(file_name13)
avg_words_speisenname13, avg_words_beschreibung13, avg_length_speisenname_no_punctuation13, avg_length_beschreibung_no_punctuation13, avg_price13  = count_words_and_avg_length(json_data13)

print(f"alles: Durchschnittliche Anzahl der Wörter in Speisennamen: {avg_words_speisenname13}")
print(f"alles: Durchschnittliche Anzahl der Wörter in Beschreibungen: {avg_words_beschreibung13}")
print(f"alles: Durchschnittliche Länge der Wörter ohne Satzzeichen in Speisennamen: {avg_length_speisenname_no_punctuation13}")
print(f"alles: Durchschnittliche Länge der Wörter ohne Satzzeichen in Beschreibungen: {avg_length_beschreibung_no_punctuation13}")
print(f"alles: Durchschnittlicher Preis: {avg_price13}")


file_name14 = 'results/outputs_language_aspects/none-corpus.json'  

json_data14 = read_json_file(file_name14)
avg_words_speisenname14, avg_words_beschreibung14, avg_length_speisenname_no_punctuation14, avg_length_beschreibung_no_punctuation14, avg_price14  = count_words_and_avg_length(json_data14)

print(f"nothing: Durchschnittliche Anzahl der Wörter in Speisennamen: {avg_words_speisenname14}")
print(f"nothing: Durchschnittliche Anzahl der Wörter in Beschreibungen: {avg_words_beschreibung14}")
print(f"nothing: Durchschnittliche Länge der Wörter ohne Satzzeichen in Speisennamen: {avg_length_speisenname_no_punctuation14}")
print(f"nothing: Durchschnittliche Länge der Wörter ohne Satzzeichen in Beschreibungen: {avg_length_beschreibung_no_punctuation14}")
print(f"nothing: Durchschnittlicher Preis: {avg_price14}")