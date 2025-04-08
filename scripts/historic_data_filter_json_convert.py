import os
import pandas as pd

# Project and folder paths
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_FOLDER = os.path.join(project_dir, 'data', 'historic-data')
FILTERED_DATA_FOLDER = os.path.join(project_dir, 'data', 'filtered-data')

# Ensure the filtered folder exists
os.makedirs(FILTERED_DATA_FOLDER, exist_ok=True)

# Define the 30 most popular stops
top_30_stops = [
    "Zürich HB", "Bern", "Basel SBB", "Genève", "Lausanne", "Luzern", "Winterthur",
    "St. Gallen", "Lugano", "Biel/Bienne", "Thun", "Schaffhausen", "Chur",
    "Olten", "Neuchâtel", "Fribourg", "Sion", "Aarau", "Uster", "Yverdon-les-Bains",
    "Wil SG", "Kreuzlingen", "Zug", "Wädenswil", "Solothurn", "Baden", "Lenzburg",
    "Brugg AG", "Bellinzona", "Montreux"
]

# Iterate through all CSV files
for filename in os.listdir(RAW_DATA_FOLDER):
    if not filename.endswith('.csv'):
        continue

    input_path = os.path.join(RAW_DATA_FOLDER, filename)
    json_filename = os.path.splitext(filename)[0] + '.json'
    output_path = os.path.join(FILTERED_DATA_FOLDER, json_filename)

    # Skip if already filtered
    if os.path.exists(output_path):
        print(f"Skipping {filename} (JSON already exists).")
        continue

    print(f"Processing {filename}...")

    try:
        chunks = pd.read_csv(input_path, sep=';', chunksize=100_000, low_memory=False)
        filtered_chunks = []

        for chunk in chunks:
            filtered = chunk[chunk['HALTESTELLEN_NAME'].isin(top_30_stops)]
            filtered_chunks.append(filtered)

        if filtered_chunks:
            filtered_df = pd.concat(filtered_chunks)
            # Save as JSON
            filtered_df.to_json(output_path, orient='records', lines=True, force_ascii=False)
            print(f"Saved filtered data to: {output_path}")
        else:
            print(f"No relevant data found in {filename}")

    except Exception as e:
        print(f"Failed to process {filename}: {e}")
