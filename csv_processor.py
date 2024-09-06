# csv_processor.py

import csv

def extract_text_from_csv(file_path):
    text = ''
    with open(file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            text += ', '.join(row) + '\n'  # Concatenar cada fila del CSV con comas y saltos de línea
    return text
