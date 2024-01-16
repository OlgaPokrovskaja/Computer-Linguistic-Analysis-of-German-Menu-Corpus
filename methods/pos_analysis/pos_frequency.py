
"""
N-Gram Analyse durch POS-Tags von Adjektiven (ADJ), Verben (VERB), Eigennamen (PROPN), Nomen (NOUN), Prepositionen (ADP), Adverbien (ADV)
"""


import ijson

#Einlesen der Input-Json und extrahieren der POS-Tags
def read_file(input):
    with open(input, 'r', encoding='utf-8') as input_file:
        json_objects = ijson.items(input_file, 'item')
        for obj in json_objects:
            for speise in obj['speisen']:
                pos_tags = speise['pos_tags']
                yield pos_tags

#BEstimmung der Input und Output-Pfade
input_file_path = 'results/outputs/output6.json'
output_noun_file_path = 'pos/output/nouns.txt'
output_adj_file_path = 'adjectives.txt'
output_verb_file_path = 'pos/output/verbs.txt'
output_adv_file_path = 'pos/output/adverbs.txt'
output_propn_file_path = 'pos/output/propernouns.txt'
output_adp_file_path = 'adpositions.txt'

#Öffnen der Output-Files und Frequenzlisten mit Lemma erstellen
with open(output_adj_file_path, 'w', encoding='utf-8') as adj_file, \
     open(output_adp_file_path , 'w', encoding='utf-8') as adp_file, \
     open(output_verb_file_path, 'w', encoding='utf-8') as verb_file, \
     open(output_propn_file_path, 'w', encoding='utf-8') as propn_file, \
     open(output_adv_file_path, 'w', encoding='utf-8') as adv_file, \
     open(output_noun_file_path, 'w', encoding='utf-8') as noun_file:
    
    for pos_tags in read_file(input_file_path):
        for word, lemma, tag in pos_tags:
            if tag.startswith('ADJ'):
                adj_file.write(f"{lemma}\n")
            elif tag.startswith('ADP'):
                adp_file.write(f"{lemma}\n") 
            elif tag.startswith('VERB'):
                verb_file.write(f"{lemma}\n")
            elif tag.startswith('PROPN'):
                propn_file.write(f"{lemma}\n")
            elif tag.startswith('ADV'):
                adv_file.write(f"{lemma}\n")
            elif tag.startswith('NOUN'):
                noun_file.write(f"{lemma}\n")

