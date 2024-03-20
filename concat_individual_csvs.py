import os
import pandas as pd

# Path to the directory containing all CSV files
directory = '/Users/juliankilchling/Documents/Le Wagon Final Project/Fileshare/Markstammdatenregister'

# Initialize an empty list to store DataFrames
dfs = []

# Iterate over each file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        filepath = os.path.join(directory, filename)
        print("Reading file:", filepath)  # Add this line for debugging
        # Read the CSV file into a DataFrame and append to the list
        df = pd.read_csv(filepath, delimiter=';', encoding='utf-8')

        # # Drop columns based on their names
        # df = df.drop(columns=['Datum der geplanten Inbetriebnahme',
        #                       'Datum der endgültigen Stilllegung',
        #                       'Hersteller der Windenergieanlage',
        #                       'Hauptbrennstoff der Einheit',
        #                       'MaStR-Nr. der Genehmigung',
        #                       'MaStR-Nr. der KWK-Anlage',
        #                       'Elektrische KWK-Leistung',
        #                       'MaStR-Nr. der Genehmigung',
        #                       'Netzbetreiberprüfung',
        #                       'Name des Anschluss-Netzbetreibers',
        #                       'MaStR-Nr. des Anschluss-Netzbetreibers',
        #                       'Thermische Nutzleistung in kW'])
        
        # Append the filtered DataFrame to the list
        dfs.append(df)

# Concatenate all DataFrames in the list into a single DataFrame
merged_df = pd.concat(dfs, ignore_index=True)

# Export the merged DataFrame to a new CSV file
merged_df.to_csv('/Users/juliankilchling/Documents/Le Wagon Final Project/Fileshare/merged_market_registry.csv', index=False)

