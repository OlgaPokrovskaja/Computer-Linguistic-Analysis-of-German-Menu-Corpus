"""
Visualisierung der Komplexitätsmessung

"""

import json
import plotly.express as px
import pandas as pd
import statsmodels.api as sm
import plotly.graph_objects as go
import seaborn as sns

# JSON-Daten laden
with open('methods/analysis/outputs_analysis/descriptions_output2.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Durchschnittliche Beschreibungslänge und Durchschnittspreis pro Kategorie berechnen
category_data = {}
all_desc_lengths = []
all_prices = []

for entry in data:
    category = entry['Bundesland'] if 'Bundesland' in entry and entry['Bundesland'] != 'Undefined' else 'Österreich' if 'Bundesland' in entry and entry['Bundesland'] == 'Undefined' else 'Österreich'
    #Zeile oben Ersetzen, um pro Kategorie zu messen: category = entry['kategorie'] if 'kategorie' in entry else 'Undefined'
    description_len = entry['average_word_length']
    #Zeile oben ersetzen um Wortanzahl zu messen: description_len = entry['average_description_length']
    
    price = entry['average_price']

    all_desc_lengths.append(description_len)
    all_prices.append(price)

    if category not in category_data:
        category_data[category] = {'description_lengths': [], 'average_prices': []}

    category_data[category]['description_lengths'].append(description_len)
    category_data[category]['average_prices'].append(price)

# Daten für Plotly Express vorbereiten
data_list = []
# Farbpalette von Seaborn verwenden
colors = sns.color_palette("flare", len(category_data)).as_hex()

for category, values in category_data.items():
    desc_lengths = values['description_lengths']
    prices = values['average_prices']

    avg_description_length = sum(desc_lengths) / len(desc_lengths)
    avg_price = sum(prices) / len(prices)

    data_list.append({'Bundesland': category, 'Avg_Description_Length': avg_description_length, 'Avg_Price': avg_price})
    #Zeile oben ersetzen um auf Kategorie zu wechseln:
    #data_list.append({'Kategorie': category, 'Avg_Description_Length': avg_description_length, 'Avg_Price': avg_price})


# DataFrame erstellen
df = pd.DataFrame(data_list)

X = sm.add_constant(df['Avg_Description_Length'])
y = df['Avg_Price']


# lineare Regression durchführen
model = sm.OLS(y, X).fit()

# Scatter-Plot erstellen
fig = px.scatter(df, x='Avg_Description_Length', y='Avg_Price', color='Bundesland',  color_discrete_sequence=colors, title='Mittelwerte des Preises und Wortlänge pro Bundesland im deutschen Speisekarten-Korpus')
"""
Zeile oben ersetzen um andere Überschriften zu erstellen:

fig = px.scatter(df, x='Avg_Description_Length', y='Avg_Price', color='Kategorie',  color_discrete_sequence=colors, title='Mittelwerte des Preises und Wortlänge pro Restaurantkategorie im deutschen Speisekarten-Korpus')
fig = px.scatter(df, x='Avg_Description_Length', y='Avg_Price', color='Bundesland',  color_discrete_sequence=colors, title='Mittelwerte des Preises und Wortlänge pro Bundesland im deutschen Speisekarten-Korpus')
fig = px.scatter(df, x='Avg_Description_Length', y='Avg_Price', color='Kategorie',  color_discrete_sequence=colors, title='Mittelwerte des Preises und der Wortanzahl pro Restaurantkategorie im deutschen Speisekarten-Korpus')
fig = px.scatter(df, x='Avg_Description_Length', y='Avg_Price', color='Bundesland',  color_discrete_sequence=colors, title='Mittelwerte des Preises und der Wortanzahl pro Bundesland im deutschen Speisekarten-Korpus')
"""
# Lineare Regression als Linie hinzufügen
fig.add_trace(go.Scatter(x=df['Avg_Description_Length'], y=model.predict(X), mode='lines', name='Trendline', line=dict(color='blue', width=2)))
fig.update_traces(marker=dict(size=15))

# Koeffizienten der Regressionsgeraden abrufen
intercept, slope = model.params[0], model.params[1]

# Formel der Regressionsgeraden als Beschriftung erstellen
equation_label = f'Avg_Price = {slope:.2f} * Avg_Word_Lenght + {intercept:.2f}'
#Zeile oben ersetzen um Wortanzahl zu berechnen:
#equation_label = f'Avg_Price = {slope:.2f} * Avg_Word_Number + {intercept:.2f}'


# Beschriftung zur Linie hinzufügen
fig.add_annotation(
    go.layout.Annotation(
        x=0.5,
        y=1.05,
        xref='paper',
        yref='paper',
        text=equation_label,
        showarrow=False,
        font=dict(size=15),
        bgcolor='rgba(255, 255, 255, 0.8)'
    )
)

# Layout-Optionen festlegen
fig.update_layout(
    xaxis=dict(title='Mittelwert der Wortlänge'),
    #xaxis=dict(title='Mittelwert der Wortlänge'),
    #xaxis=dict(title='Mittelwert der Wortanzahl'),
    yaxis=dict(title='Mittelwert des Preises'),
    hovermode='closest'
)

# Graphik als interaktive HTML-Datei speichern
fig.write_html("methods/results/mapping/descriptions_word_bund.html")

"""
Zeile obene rsetzen um anderes Scatter Plot zu erstellen:
#fig.write_html("results/visualisation/complexity/descriptions_word_bund.html")
#fig.write_html("results/visualisation/complexity/descriptions_word_kat.html")
#fig.write_html("results/visualisation/complexity/descriptions_desc_kat.html")
#fig.write_html("results/visualisation/complexity/descriptions_desc_bund.html"
"""


