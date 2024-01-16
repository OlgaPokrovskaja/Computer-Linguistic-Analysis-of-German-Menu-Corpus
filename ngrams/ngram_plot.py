
"""
Visualisierung der N-Gram Analyse in Lowercase und in Normalschreibweise der Speisennamen und Speisenbeschreibungen

"""


import matplotlib.pyplot as plt
from collections import Counter
import numpy as np

#Gesamtanzahl der N-Grams bestimmen
def count_string_occurrences(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        strings = [line.lower() for line in file.read().splitlines()]  #Lowercase: strings = [line.lower() for line in file.read().splitlines()] ; Normal:strings = file.read().splitlines()
        string_counts = Counter(strings)
    return string_counts

#Anzahl der einzelnen N-Grams mit Anzahl in txt Datei schreiben
def write_string_counts(string_counts, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for string, count in string_counts.most_common():
            file.write(f"{string}: {count}\n")


#Plot-Erstellen
def plot_curve(string_counts, output_image_path):
    counts = [count for _, count in string_counts.most_common()]
    strings = range(1, len(counts) + 1)
    
    #Entweder durch log oder sqrt bestimmen
    counts = np.sqrt(counts) #log, sqrt
    strings = np.sqrt(strings) #log, srt
    
    plt.plot(strings, counts, linestyle='-')
    plt.xlabel('sqrt(String-Ranking)')
    plt.ylabel('sqrt(Anzahl der Vorkommen)')
    plt.title('BESCHREIBUNG_LOW 3-GRAM ANALYSE MIT STOPWÖRTERN')
    
    plt.savefig(output_image_path)
    plt.show()





#Input und Ausgabedateien bestimmen
input_file_path = 'testing/ngrams/beschreibung/normal/mit-stop/beschreibung_ngram3.txt' #ngrams/beschreibung/mit-stop/beschreibung_ngram(1,2,3).txt, ngrams/beschreibung/ohne-stop/beschreibung_ngram1_no.txt
output_file_path = 'testing/ngrams/beschreibung/lowercase/mit-stop/beschreibung_low_ngram3_sorted_copy.txt' #ngrams/beschreibung/ohne-stop/beschreibung_ngram1_sorted.txt   , ngrams/beschreibung/mit-stop/beschreibung_ngram1_sorted.txt
output_image_path = 'testing/ngrams/beschreibung/lowercase/mit-stop/b_low_mitstop_3_sqrt.png' #ngrams/beschreibung/mit-stop/b_mit_stop_1.png  , ngrams/beschreibung/ohne-stop/b_no_3.png



#Methoden aufrufen
string_counts = count_string_occurrences(input_file_path)


write_string_counts(string_counts, output_file_path)


plot_curve(string_counts, output_image_path)


