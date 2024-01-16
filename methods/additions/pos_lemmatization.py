"""
Hinzufügen von POS-Tags und Lemmatisierungen zu Speisennamen
Hinzufügen von Lemmatisierungen zu den Speisenbeschreibungen mit Stanza

"""
import stanza
import ijson
import json
from decimal import Decimal

#Definition der Stanza-Pipeline, mit batch_size für weniger Überlastung
nlp = stanza.Pipeline(lang='de', processors='tokenize,mwt,pos,lemma', pos_batch_size=500)

#Einlesen der Eingabedatei
with open('results/outputs_scraping_cleaning_pos/output5.json', 'r', encoding='utf-8') as input_file:
    json_data = ijson.items(input_file, 'item')

    #Direktes Schreiben in die Ausgabedatei
    with open('results/outputs_scraping_cleaning_pos/output6.json', 'w', encoding='utf-8') as output_file:
        output_file.write('[')
        
        for obj in json_data:
            updated_obj = obj.copy()
            speisen = updated_obj['speisen']
            
            for speise in speisen:
                speisenname = speise['speisenname']
                beschreibung = speise['beschreibung']

                #Bestimmung der Speisenbeschreibungen als doc
                doc = nlp(speisenname)
                doc2 = nlp(beschreibung)

                #Hinzufügen des pos_tags_s Eintrag zu den JSON-Korpus (Speisennamen)
                pos_tags = [(word.text, word.upos) for sent in doc.sentences for word in sent.words]
                speise['pos_tags_s'] = pos_tags

              

                lemma = [(word.lemma) for sent in doc.sentences for word in sent.words]
                lemma2 = [(word.lemma) for sent in doc2.sentences for word in sent.words]

                pos_tags2 = speise['pos_tags']
                for i in range(len(pos_tags2)):
                    pos_tags2[i].insert(1, lemma2[i])  # Hinzufügen von Lemmata nach den Originalwort
                
                pos_tagss = list(speise['pos_tags_s'])  # Konvertierung des Tupels in eine Liste
                
                for i in range(len(pos_tags)):
                    
                    pos_tag_list = list(pos_tagss[i])  # Konvertierung des Tupels in eine Liste
                    pos_tag_list.insert(1, lemma[i])  # Hinzufügen von Lemmata nach den Originalwort
                    pos_tagss[i] = tuple(pos_tag_list) # Konvertierung der Liste zurück in ein Tupel
                
                speise['pos_tags_s'] = pos_tagss  # Aktualisierte Liste der POS-Tags setzen
                speise['preis'] = float(speise['preis'])
            
            output_file.write(json.dumps(updated_obj, ensure_ascii=False, default=lambda x: str(x) if isinstance(x, Decimal) else x))
            output_file.write(',' + '\n')
        output_file.write(']')       



