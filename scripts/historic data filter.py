import pandas as pd

# Define the 30 most popular stops (replace or extend this list as needed)
TOP_30_STOPS = [
    "Zürich HB", "Bern", "Basel SBB", "Luzern", "Genève", "Winterthur", "Lausanne",
    "St. Gallen", "Lugano", "Biel/Bienne", "Thun", "Olten", "Sion", "Schaffhausen",
    "Neuchâtel", "Chur", "Fribourg/Freiburg", "Yverdon-les-Bains", "Aarau", "Zug",
    "Wil SG", "Uster", "Bellinzona", "Locarno", "Baden", "Romanshorn", "Brig",
    "Solothurn", "Rapperswil", "Dietikon"
]

def filter_and_save_csv(filepath):
    """Filter CSV by HALTESTELLEN_NAME and save it"""
    try:
        df = pd.read_csv(filepath, sep=';', dtype=str)
        if 'HALTESTELLEN_NAME' in df.columns:
            filtered_df = df[df['HALTESTELLEN_NAME'].isin(TOP_30_STOPS)]
            if not filtered_df.empty:
                filtered_df.to_csv(filepath, sep=';', index=False)
                print(f"Filtered and saved: {os.path.basename(filepath)}")
            else:
                print(f"No matching stops found in: {os.path.basename(filepath)}")
        else:
            print(f"'HALTESTELLEN_NAME' not in columns of: {os.path.basename(filepath)}")
    except Exception as e:
        print(f"Error processing {os.path.basename(filepath)}: {e}")
