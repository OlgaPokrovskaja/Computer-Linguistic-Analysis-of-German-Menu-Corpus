"""
Entfernen jeder Speise mit keinen eindeutigen Preis

"""
import json


input_file_path = 'results/outputs/output_basis_cleaned.json'  # Pfad der Eingabedatei
output_file_path = 'results/outputs/output_basis_cleaned2.json'  # Pfad der Ausgabedatei

with open(input_file_path, 'r', encoding='utf-8') as input_file, open(output_file_path, 'w', encoding='utf-8') as output_file:
    data = json.load(input_file)

    output_file.write('['+ ('\n'))

    updated_data = []
    for obj in data:
        speisen = obj['speisen']
        obj['speisen'] = [speise for speise in speisen if speise.get('preis') is not None]
        updated_data.append(obj)
        
        if obj['speisen']:
            output_file.write(json.dumps(obj, ensure_ascii=False) + ',' + ('\n'))
    
    output_file.write(']'+ ('\n'))
