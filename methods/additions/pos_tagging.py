"""
Hinzufügen von POS-Tags zu den Scpeisenbeschreibungen mit Stanza

"""

import stanza
import ijson
import json


#Definition der Stanza-Pipeline, mit batch_size für weniger Überlastung
nlp = stanza.Pipeline(lang='de', processors='tokenize,mwt,pos', pos_batch_size=500)


#Einlesen der Eingabedatei
with open('results/outputs_scraping_cleaning_pos/output2', 'r', encoding='utf-8') as input_file: 
    json_data = ijson.items(input_file, 'item')
    
    #Direktes Schreiben in die Ausgabedatei
    with open('results/outputs_scraping_cleaning_pos/output3', 'w', encoding='utf-8') as output_file:  
        output_file.write('[')
        for obj in json_data:
            updated_obj = obj.copy()
            speisen = updated_obj['speisen']
            for speise in speisen:
                beschreibung = speise['beschreibung']
                #Bestimmung der Speisenbeschreibungen als doc
                doc = nlp(beschreibung)
                #Hinzufügen des pos_tags Eintrag zu den JSON-Korpus
                pos_tags = [(word.text, word.upos) for sent in doc.sentences for word in sent.words]
                speise['pos_tags'] = pos_tags
            
            output_file.write(json.dumps(updated_obj, ensure_ascii=False))
            output_file.write(',' + '\n')
        output_file.write(']')    

