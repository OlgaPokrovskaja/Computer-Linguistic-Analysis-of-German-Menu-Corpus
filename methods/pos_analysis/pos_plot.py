
"""
Plot der 1-Gram Analyse der Wortarten

"""

import matplotlib.pyplot as plt
from collections import Counter
import numpy as np


#Gesamtanzahl der N-Grams bestimmen
def count_string_occurrences(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        strings = [line.lower() for line in file.read().splitlines()]
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
    counts = np.sqrt(counts)
    strings = np.sqrt(strings)
    
    plt.plot(strings, counts, linestyle='-')
    plt.xlabel('sqrt(String-Ranking)')
    plt.ylabel('sqrt(Anzahl der Vorkommen)')
    plt.title('Wortkombinationen Vorkommen')
    
    plt.savefig(output_image_path)
    plt.show()

#Einsetzen der Input und Output-Pfade
input_file_path = 'testing/pos_analysis/adpositions.txt'
output_file_path = 'testing/pos_analysis/adpositions_counts.txt'
output_image_path = 'testing/pos_analysis/adpositions_plot_sqrt.txt'

#Methoden aufrufen
string_counts = count_string_occurrences(input_file_path)
write_string_counts(string_counts, output_file_path)
plot_curve(string_counts, output_image_path)
