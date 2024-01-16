"""
Visualisierung der Sprachaspekte nach der Varianz der Restaurantkategorien in Form von Hexagons (Umkreis ca. 50 km) 

"""
import pandas as pd
import plotly.figure_factory as ff
import numpy as np

#Einlesen der Input-Datei und Konvertieren in Pandas-Frame
df = pd.read_json('results/outputs_scraping_cleaning_pos/output_basis.json')

"""
Zeile oben ersetzen um einen anderen Sprachaspekt zu visualisieren:
df = pd.read_json('results/outputs_language_aspects/none-corpus.json')
df = pd.read_json('results/outputs_language_aspects/adjectives.json')
df = pd.read_json('results/outputs_language_aspects/compounds_adel_deutsch_split.json')
df = pd.read_json('results/outputs_language_aspects/compounds_adel_deutsch.json')
df = pd.read_json('results/outputs_language_aspects/dialekte.json')
df = pd.read_json('results/outputs_language_aspects/homemade.json')
df = pd.read_json('results/outputs_language_aspects/international_adel.json')
df = pd.read_json('results/outputs_language_aspects/personen_name.json')
df = pd.read_json('results/outputs_language_aspects/personen_ruf.json')
df = pd.read_json('results/outputs_language_aspects/preposition.json')
df = pd.read_json('results/outputs_language_aspects/region.json')
"""

#Funktion zum Erzeugen kleiner Verschiebungen der Koordinaten definieren
def shift_coordinates(lat, lon, count, index):
    lat = float(lat)
    lon = float(lon)
    shift = 0.0001 * np.sin(2*np.pi*(index/count))
    return lat + shift, lon + shift

#Anzahl der Kategorien zählen
def count_categories(x):
    return len(set(x))

# Überprüfung auf Duplikate von latitude und longitude
df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
df = df.dropna(subset=['latitude', 'longitude'])
df['latitude'] = df['latitude'].astype(float)
df['longitude'] = df['longitude'].astype(float)
duplicates = df.duplicated(subset=['latitude', 'longitude'], keep=False)

# Datenframe für duplizierte Einträge erstellen
duplicated_df = df[duplicates]

# Datenframe für nicht-duplizierte Einträge erstellen
non_duplicates_df = df[~duplicates]

# Koordinaten der duplizierten Einträge anpassen
duplicated_df['latitude'], duplicated_df['longitude'] = zip(*duplicated_df.apply(
        lambda row: shift_coordinates(row['latitude'], row['longitude'], len(duplicated_df), row.name), axis=1
    ))

# Zusammenführen der beiden DataFrames
merged_df = pd.concat([non_duplicates_df, duplicated_df])

# Kategorien nach Häufigkeit sortieren
sorted_categories = merged_df['kategorie'].value_counts().index

# Hexbin Mapbox erstellen
fig = ff.create_hexbin_mapbox(
    data_frame=merged_df, lat='latitude', lon='longitude',
    nx_hexagon=15, opacity=0.7, labels={'color': 'Category Count'},
    color='kategorie',
    agg_func=count_categories, 
    min_count=1, color_continuous_scale="ice_r",
    color_continuous_midpoint=len(sorted_categories) / 2,
    show_original_data=False
)

# Mapbox-API-Token einfügen (erhalten von https://account.mapbox.com/)
fig.update_layout(mapbox={'accesstoken': 'HIER API-TOKEN EINFÜGEN'})

#Speichern der erstellten Karte als interaktive HTML
fig.write_html('results/visualisation/maps/corpus.html')


"""
Zeile oben ersetzen um einen anderen Sprachaspekt zu visualisieren:

fig.write_html('results/visualisation/maps/none-corpus.html') 
fig.write_html('results/visualisation/maps/adjectives.html') 
fig.write_html('results/visualisation/maps/comp_split.html') 
fig.write_html('results/visualisation/maps/comp_bund.html') 
fig.write_html('results/visualisation/maps/dialekte.html') 
fig.write_html('results/visualisation/maps/homemade.html') 
fig.write_html('results/visualisation/maps/international.html') 
fig.write_html('results/visualisation/maps/person_name.html') 
fig.write_html('results/visualisation/maps/person_name.html') 
fig.write_html('results/visualisation/maps/preposition.html') 
fig.write_html('results/visualisation/maps/region.html') 
"""


