"""
Visualisierung des gesamten Korpus 

"""
import json
import pandas as pd
import plotly.express as px
import seaborn as sns
import numpy as np

# JSON-Daten laden
df = pd.read_json('results/outputs_scraping_cleaning_pos/output_basis.json')

# Funktion zum Erzeugen kleiner Verschiebungen der Koordinaten definieren
def shift_coordinates(lat, lon, count, index):
    shift = 0.0001 * np.sin(2*np.pi*(index/count))
    return lat + shift, lon + shift

# Überprüfung auf Duplikate von latitude und longitude
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

# Kategorien extrahieren und ihre Häufigkeit zählen
kategorien_counts = merged_df['kategorie'].value_counts().reset_index()
kategorien_counts.columns = ['kategorie', 'count']

# Kategorien nach Häufigkeit sortieren
kategorien_counts = kategorien_counts.sort_values(by='count', ascending=False)

# Farbenpalette von seaborn verwenden
colors = sns.color_palette("Spectral", n_colors=len(kategorien_counts)).as_hex()

# Karte erstellen
fig = px.scatter_mapbox(merged_df, lat='latitude', lon='longitude', hover_name='restaurantname',
                        hover_data=['adresse_stadt', 'adresse_plz', 'adresse_straße'],
                        color='kategorie', zoom=10, color_discrete_sequence=colors,
                        category_orders={'kategorie': kategorien_counts['kategorie'].tolist()})

# Mapbox-API-Token einfügen (erhalten von https://account.mapbox.com/)
fig.update_layout(mapbox={'accesstoken': 'HIER API-TOKEN EINFÜGEN'})

fig.write_html('results/visualisation/maps/corpus_dot.html') 