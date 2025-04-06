import json


# Dateien laden

def load_json(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def merge_json(metadata, measurements):
    merged_data = {}

    for site_id, meta_info in metadata.items():
        merged_data[site_id] = meta_info.copy()
        merged_data[site_id]["measurements"] = []

        # Falls Messwerte existieren
        if site_id in measurements:
            measurement_data = measurements[site_id]
            timestamp = measurement_data.get("timestamp")
            merged_data[site_id]["timestamp"] = timestamp

            measurement_dict = measurement_data.get("measurements", {})
            for measurement in meta_info.get("measurements", []):
                index = str(measurement["index"])
                value_data = measurement_dict.get(index, {})

                merged_entry = {**measurement, **value_data}
                merged_data[site_id]["measurements"].append(merged_entry)

    return merged_data


# JSON-Dateien laden
metadata = load_json("output_Site-Data.json")  # Datei mit Messstations-Informationen
measurements = load_json("output_Livedata.json")  # Datei mit Messwerten

# Zusammenführen
data_merged = merge_json(metadata, measurements)
#print(data_merged)


# Speichern der kombinierten Datei
with open("merged_data.json", "w", encoding="utf-8") as file:
    json.dump(data_merged, file, indent=4, ensure_ascii=False)
print("JSON-Dateien erfolgreich zusammengeführt!")
