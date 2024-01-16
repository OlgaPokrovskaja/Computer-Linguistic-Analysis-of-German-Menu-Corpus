"""
Suche nach Komposita Kombinationen durch POS-Tags Kombinationen

"""

import ijson

#Einlesen des Korpus
def read_file(input):
    with open(input, 'r', encoding='utf-8') as input_file:
        json_objects = ijson.items(input_file, 'item')
        for obj in json_objects:
            for speise in obj['speisen']:
                pos_tags = speise['pos_tags']
                yield pos_tags

#Kombinationen von Komposita suchen
def generate_combinations(pos_tags):
    combinations = []
    #Alle Kombinationen von zwei Wörtern und einen Bindestrich durchgehen
    for i in range(len(pos_tags) - 2):
        tag1 = pos_tags[i][1]
        tag2 = pos_tags[i + 1][1]
        tag3 = pos_tags[i + 2][1]
        word1 = pos_tags[i][0]
        word2 = pos_tags[i + 1][0]
        word3 = pos_tags[i + 2][0]
        if (tag1.startswith('NOUN') and tag2 == 'PUNCT' and tag3.startswith('NOUN') and word2 == '-') or \
           (tag1.startswith('PROPN') and tag2 == 'PUNCT' and tag3.startswith('PROPN') and word2 == '-') or \
           (tag1.startswith('NOUN') and tag2 == 'PUNCT' and tag3.startswith('PROPN') and word2 == '-') or \
           (tag1.startswith('PROPN') and tag2 == 'PUNCT' and tag3.startswith('NOUN') and word2 == '-'):
            combinations.append((word1, word2, word3))
    return combinations

input_file_path = 'results/outputs/output3.json'
output_file_path = 'testing/pos_analysis/word_combinations.txt' 

with open(output_file_path, 'w', encoding='utf-8') as output_file:
    for pos_tags in read_file(input_file_path):
        combinations = generate_combinations(pos_tags)
        for combination in combinations:
            output_file.write(f"{combination[0]}{combination[1]}{combination[2]}\n")