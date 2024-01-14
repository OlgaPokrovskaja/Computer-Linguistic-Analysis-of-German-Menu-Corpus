
"""
Erstellung von 1-,2-,3- Grams der Beschreibungen und Speisennamen

"""


import ijson
import re
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

#Einlesen der Eingabedatei und entweder Speisennamen oder Speisenbeschreibungen

def read_file(input):
    with open(input, 'r', encoding='utf-8') as input_file:
        json_objects = ijson.items(input_file, 'item')
        for obj in json_objects:
            for speise in obj['speisen']:
                text = speise['speisenname'] #beschreibung oder speisenname ändern
                yield text

#Entfernung der Zeichensetzung
def remove_punctuation(text):
    return re.sub(r'[^\w\s-]', '', text)

#Definition von Stopwörtern von der NLTK-Bibliothek
stopwords_set = set(stopwords.words('german'))

def generate_N_grams(text, ngraml):
    words = [word for word in text.split(' ') if word not in stopwords_set] #Ohne Stopwörter: Zeile umändern in "words = [word for word in text.split(' ')]"
    temp = zip(*[words[i:] for i in range(0, int(ngraml))])
    ans = [' '.join(ngram) for ngram in temp]
    return ans

input_file_path = 'results/outputs/output_basis_cleaned2.json'
output_file_path = 'ngrams/speisennamen/mit-stop/speisenname_ngram3.txt' #ngrams/beschreibung/ohne-stop/beschreibung_ngram(1,2,3)_no.txt   ngrams/beschreibung/mit-stop/beschreibung_ngram(1,2,3).txt
ngraml = 3 #1,2,3 umändern für Erstellung von 1-Grams, 2-Grams, 3-Grams
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    for text in read_file(input_file_path):
        text_without_punctuation = remove_punctuation(text)
        text_deleted_whitespace = re.sub(r"\s+", " ", text_without_punctuation.strip())
        if text_deleted_whitespace:
            ngram_list = generate_N_grams(text_deleted_whitespace, ngraml)
            for ngram in ngram_list:
                output_file.write(f"{ngram}\n")


