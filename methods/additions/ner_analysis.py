"""
Erstellung von Frequenzlisten für die NER-Tags Personennamen (PER), Ortsnennungen (LOC), Organisationen (ORG) und Verschiedenes (MISC)

"""



import ijson
from collections import Counter

#Einlesen der Input-Json und extrahieren der NER-Tags
def read_file(input):
    with open(input, 'r', encoding='utf-8') as input_file:
        json_objects = ijson.items(input_file, 'item')
        for obj in json_objects:
            for speise in obj['speisen']:
                entities = speise['entity']
                yield entities

#Erstellung von Listen für Personennamen, Ortsnennungen, Organisationen und Verschiedenes, falls der NER-Tag übereinstimmt
def generate_lists(entities):
    per = []
    loc = []
    org = []
    misc = []
    for entity in entities:
        for ent in entity:
            tag = ent[1]
            word = ent[0]
            
            if tag == "PER":
                per.append(word)
            elif tag == "LOC":
                loc.append(word)
            elif tag == "ORG":
                org.append(word)
            elif tag == "MISC":
                misc.append(word)
    return per, loc, org, misc

#Bestimmung der Input und Output-Pfade
input_file_path = 'results/outputs_language_aspects/ner_tagging.json' 
output_per = 'testing/ner_analysis/person.txt' 
output_loc = 'testing/ner_analysis/location.txt'
output_org = 'testing/ner_analysis/organisation.txt'
output_misc = 'testing/ner_analysis/misc.txt'

# Einlesen der JSON-Datei und Generierung von Listen für die Tags
entities_generator = read_file(input_file_path)
per_list, loc_list, org_list, misc_list = generate_lists(entities_generator)

# Vorkommen der Wörter zählen
per_counts = Counter(per_list)
loc_counts = Counter(loc_list)
org_counts = Counter(org_list)
misc_counts = Counter(misc_list)

# Schreiben der Ergebnisse in separate TXT-Dateien
with open(output_per, 'w', encoding='utf-8') as file:
    for word, count in per_counts.most_common():
        file.write(f'{word}: {count}\n')

with open(output_loc, 'w', encoding='utf-8') as file:
    for word, count in loc_counts.most_common():
        file.write(f'{word}: {count}\n')

with open(output_org, 'w', encoding='utf-8') as file:
    for word, count in org_counts.most_common():
        file.write(f'{word}: {count}\n')

with open(output_misc, 'w', encoding='utf-8') as file:
    for word, count in misc_counts.most_common():
        file.write(f'{word}: {count}\n')
