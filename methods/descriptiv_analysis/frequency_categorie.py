"""
Erstellung der Frequenzlisten der Restaurantkategorien für jeden Sprachaspekt

"""

import json
from collections import defaultdict

#Einlesen der Input-Datei
def read_json_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        return json.load(file)

#Erstellung der Frequenzlisten
def generate_frequency_list(data):
    state_frequency = defaultdict(int)
    category_frequency = defaultdict(int)

    for entry in data:
        bundesland = entry.get('bundesland', 'Undefined')
        category = entry.get('kategorie', 'Undefined')

        state_frequency[bundesland] += 1
        category_frequency[category] += 1

    return state_frequency, category_frequency

#Schreiben der Frequenzlisten in eine txt-Datei
def write_frequency_list_to_txt(file_name, frequency_data):
    with open(file_name, 'w', encoding='utf-8') as output_file:
        for key, value in frequency_data.items():
            output_file.write(f"{key}: {value}\n")


#Definition der Input-Dateien und Aufruf der Methoden
            
file_name1 = 'results/outputs_language_aspects/adjectives.json'
json_data1 = read_json_file(file_name1)
state_frequency1, category_frequency1 = generate_frequency_list(json_data1)

output_file_name_state = 'results/descriptive_analysis/bundesland/adj_bu.txt'
output_file_name_category = 'results/descriptive_analysis/kategorie/adj_kat.txt'

write_frequency_list_to_txt(output_file_name_state, state_frequency1)
write_frequency_list_to_txt(output_file_name_category, category_frequency1)


file_name2 = 'results/outputs_language_aspects/compounds_adel_deutsch_split.json'
json_data2 = read_json_file(file_name2)
state_frequency2, category_frequency2 = generate_frequency_list(json_data2)


output_file_name_state2 = 'results/descriptive_analysis/bundesland/comp_split_bu.txt'
output_file_name_category2 = 'results/descriptive_analysis/kategorie/comp_split_kat.txt'

write_frequency_list_to_txt(output_file_name_state2, state_frequency2)
write_frequency_list_to_txt(output_file_name_category2, category_frequency2)


file_name3 = 'results/outputs_language_aspects/compounds_adel_deutsch.json'
json_data3 = read_json_file(file_name3)
state_frequency3, category_frequency3 = generate_frequency_list(json_data3)


output_file_name_state3 = 'results/descriptive_analysis/bundesland/comp_bund_bu.txt'
output_file_name_category3 = 'results/descriptive_analysis/kategorie/comp_bund_kat.txt'

write_frequency_list_to_txt(output_file_name_state3, state_frequency3)
write_frequency_list_to_txt(output_file_name_category3, category_frequency3)


file_name4 = 'results/outputs_language_aspects/dialekte.json'
json_data4 = read_json_file(file_name4)
state_frequency4, category_frequency4 = generate_frequency_list(json_data4)


output_file_name_state4 = 'results/descriptive_analysis/bundesland/dialekte_bu.txt'
output_file_name_category4 = 'results/descriptive_analysis/kategorie/dialekte_kat.txt'

write_frequency_list_to_txt(output_file_name_state4, state_frequency4)
write_frequency_list_to_txt(output_file_name_category4, category_frequency4)

file_name5 = 'results/outputs_language_aspects/homemade.json'
json_data5 = read_json_file(file_name5)
state_frequency5, category_frequency5 = generate_frequency_list(json_data5)


output_file_name_state5 = 'results/descriptive_analysis/bundesland/hausgemacht_bu.txt'
output_file_name_category5 = 'results/descriptive_analysis/kategorie/hausgemacht_kat.txt'

write_frequency_list_to_txt(output_file_name_state5, state_frequency5)
write_frequency_list_to_txt(output_file_name_category5, category_frequency5)


file_name6 = 'results/outputs_language_aspects/international_adel.json'
json_data6 = read_json_file(file_name6)
state_frequency6, category_frequency6 = generate_frequency_list(json_data6)


output_file_name_state6 = 'results/descriptive_analysis/bundesland/international_bu.txt'
output_file_name_category6 = 'results/descriptive_analysis/kategorie/international_kat.txt'

write_frequency_list_to_txt(output_file_name_state6, state_frequency6)
write_frequency_list_to_txt(output_file_name_category6, category_frequency6)



file_name7 = 'results/outputs_language_aspects/personen_name.json'
json_data7 = read_json_file(file_name7)
state_frequency7, category_frequency7 = generate_frequency_list(json_data7)


output_file_name_state7 = 'results/descriptive_analysis/bundesland/personen_name_bu.txt'
output_file_name_category7 = 'results/descriptive_analysis/kategorie/personen_name_kat.txt'

write_frequency_list_to_txt(output_file_name_state7, state_frequency7)
write_frequency_list_to_txt(output_file_name_category7, category_frequency7)


file_name8 = 'results/outputs_language_aspects/personen_ruf.json'
json_data8 = read_json_file(file_name8)
state_frequency8, category_frequency8 = generate_frequency_list(json_data8)


output_file_name_state8 = 'results/descriptive_analysis/bundesland/personen_ruf_bu.txt'
output_file_name_category8 = 'results/descriptive_analysis/kategorie/personen_ruf_kat.txt'

write_frequency_list_to_txt(output_file_name_state8, state_frequency8)
write_frequency_list_to_txt(output_file_name_category8, category_frequency8)

file_name9 = 'results/outputs_language_aspects/preposition.json'
json_data9 = read_json_file(file_name9)
state_frequency9, category_frequency9 = generate_frequency_list(json_data9)


output_file_name_state9 = 'results/descriptive_analysis/bundesland/prep_bu.txt'
output_file_name_category9 = 'results/descriptive_analysis/kategorie/prep_kat.txt'

write_frequency_list_to_txt(output_file_name_state9, state_frequency9)
write_frequency_list_to_txt(output_file_name_category9, category_frequency9)



file_name10 = 'results/outputs_language_aspects/region.json'
json_data10 = read_json_file(file_name10)
state_frequency10, category_frequency10 = generate_frequency_list(json_data10)


output_file_name_state10 = 'results/descriptive_analysis/bundesland/region_bu.txt'
output_file_name_category10 = 'results/descriptive_analysis//kategorie/region_kat.txt'

write_frequency_list_to_txt(output_file_name_state10, state_frequency10)
write_frequency_list_to_txt(output_file_name_category10, category_frequency10)


