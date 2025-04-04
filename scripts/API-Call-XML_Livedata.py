import requests
import xml.etree.ElementTree as ET
import json

# URL der OpenTransportData API
url = "https://api.opentransportdata.swiss/TDP/Soap_Datex2/Pull"

# Dein API-Schlüssel
api_key = "eyJvcmciOiI2NDA2NTFhNTIyZmEwNTAwMDEyOWJiZTEiLCJpZCI6ImJhZTA1NGM4YzYwMjQwNzQ4ZjRjZGFlOGJjZTIxNGYzIiwiaCI6Im11cm11cjEyOCJ9"  # Ersetze dies durch deinen tatsächlichen API-Schlüssel

# Header mit Authorization und Content-Type
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "text/xml",  # SOAP benötigt "text/xml" als Content-Type
    "SoapAction": "http://opentransportdata.swiss/TDP/Soap_Datex2/Pull/v1/pullMeasuredData"  # Erforderliche SOAP Action
}

# Erstellen des XML für die SOAP-Anfrage (pullMeasuredData Operation)
soap_body = """
<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:tdpplv1="http://datex2.eu/wsdl/TDP/Soap_Datex2/Pull/v1" xmlns:dx223="http://datex2.eu/schema/2/2_0">
	<SOAP-ENV:Body>
		<dx223:d2LogicalModel xsi:type="dx223:D2LogicalModel" modelBaseVersion="2">
			<dx223:exchange xsi:type="dx223:Exchange">
				<dx223:supplierIdentification xsi:type="dx223:InternationalIdentifier">
				<dx223:country xsi:type="dx223:CountryEnum">ch</dx223:country>
				<dx223:nationalIdentifier xsi:type="dx223:String">FEDRO</dx223:nationalIdentifier>
				</dx223:supplierIdentification>
			</dx223:exchange>
		</dx223:d2LogicalModel>
	</SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""

# Sendet die SOAP POST-Anfrage an den API-Server
response = requests.post(url, headers=headers, data=soap_body)


# Überprüfen der Antwort
if response.status_code == 200:
    # Erfolgreiche Antwort
    print("Daten erfolgreich abgerufen.")


else:
    # Fehlerbehandlung
    print(f"Fehler {response.status_code}: Anfrage fehlgeschlagen.")


# Die XML-Daten
xml_data = '''<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:tdpplv1="http://datex2.eu/wsdl/TDP/Soap_Datex2/Pull/v1" xmlns:dx223="http://datex2.eu/schema/2/2_0">
    <SOAP-ENV:Body>
        <dx223:d2LogicalModel xsi:type="dx223:D2LogicalModel" modelBaseVersion="2">
            <dx223:exchange xsi:type="dx223:Exchange">
                <dx223:supplierIdentification xsi:type="dx223:InternationalIdentifier">
                    <dx223:country xsi:type="dx223:CountryEnum">ch</dx223:country>
                    <dx223:nationalIdentifier xsi:type="dx223:String">OTD</dx223:nationalIdentifier>
                </dx223:supplierIdentification>
            </dx223:exchange>
            <dx223:payloadPublication xsi:type="dx223:MeasuredDataPublication" lang="en">
                <dx223:publicationTime xsi:type="dx223:DateTime">2024-09-20T10:00:18.145096Z</dx223:publicationTime>
                <dx223:publicationCreator xsi:type="dx223:InternationalIdentifier">
                    <dx223:country xsi:type="dx223:CountryEnum">ch</dx223:country>
                    <dx223:nationalIdentifier xsi:type="dx223:String">OTD</dx223:nationalIdentifier>
                </dx223:publicationCreator>
                <dx223:measurementSiteTableReference xsi:type="dx223:_MeasurementSiteTableVersionedReference" targetClass="MeasurementSiteTable" id="OTD:TrafficData" version="3"></dx223:measurementSiteTableReference>
                <dx223:headerInformation xsi:type="dx223:HeaderInformation">
                    <dx223:confidentiality xsi:type="dx223:ConfidentialityValueEnum">noRestriction</dx223:confidentiality>
                    <dx223:informationStatus xsi:type="dx223:InformationStatusEnum">real</dx223:informationStatus>
                </dx223:headerInformation>
                <dx223:siteMeasurements xsi:type="dx223:SiteMeasurements">
                    <dx223:measurementSiteReference xsi:type="dx223:_MeasurementSiteRecordVersionedReference" targetClass="MeasurementSiteRecord" id="CH:0677.01" version="1"></dx223:measurementSiteReference>
                    <dx223:measurementTimeDefault xsi:type="dx223:DateTime">2024-09-20T09:59:00.000000Z</dx223:measurementTimeDefault>
                    <dx223:measuredValue xsi:type="dx223:_SiteMeasurementsIndexMeasuredValue" index="11">
                        <dx223:measuredValue xsi:type="dx223:MeasuredValue">
                            <dx223:basicData xsi:type="dx223:TrafficFlow">
                                <dx223:vehicleFlow xsi:type="dx223:VehicleFlowValue">
                                    <dx223:vehicleFlowRate xsi:type="dx223:VehiclesPerHour">1200</dx223:vehicleFlowRate>
                                </dx223:vehicleFlow>
                            </dx223:basicData>
                        </dx223:measuredValue>
                    </dx223:measuredValue>
                </dx223:siteMeasurements>
            </dx223:payloadPublication>
        </dx223:d2LogicalModel>
    </SOAP-ENV:Body>
</SOAP-ENV:Envelope>'''

# Die XML-Daten parsen
root = ET.fromstring(response.text)
#print("root: ",root)

###################### Extrahieren der XML Daten und schreiben der JSON Datei



namespace = {'dx223': 'http://datex2.eu/schema/2/2_0'}

# Alle siteMeasurements extrahieren
site_measurements_list = root.findall('.//dx223:siteMeasurements', namespace)

# Dictionary für die JSON-Daten
data = {}

for elem in site_measurements_list:
    site_reference = elem.find('.//dx223:measurementSiteReference', namespace)
    site_id = site_reference.attrib["id"]
    site_version = int(site_reference.attrib["version"])

    site_timestamp = elem.find('.//dx223:measurementTimeDefault', namespace).text

    # Initialisiere die Struktur für diese SiteReference
    if site_id not in data:
        data[site_id] = {
            "version": site_version,
            "timestamp": site_timestamp,
            "measurements": {}
        }

    site_value_list = elem.findall('.//dx223:measuredValue', namespace)

    for lev2_elem in site_value_list:
        try:
            site_measurement_index = lev2_elem.attrib["index"]

            if site_measurement_index not in data[site_id]["measurements"]:
                data[site_id]["measurements"][site_measurement_index] = {}

            # Vehicle Flow Rate
            site_measurement_values = lev2_elem.find('.//dx223:vehicleFlowRate', namespace)
            if site_measurement_values is not None:
                data[site_id]["measurements"][site_measurement_index]["VehiclesPerHour"] = int(
                    site_measurement_values.text)

            # Average Vehicle Speed
            site_measurement_values_num_used = lev2_elem.find('.//dx223:averageVehicleSpeed', namespace)
            if site_measurement_values_num_used is not None:
                num_values_used = int(site_measurement_values_num_used.attrib.get("numberOfInputValuesUsed", 0))
                data[site_id]["measurements"][site_measurement_index]["NumberOfInputValuesUsed"] = num_values_used

                site_measurement_values_avg = lev2_elem.find('.//dx223:averageVehicleSpeed/dx223:speed', namespace)
                if site_measurement_values_avg is not None:
                    data[site_id]["measurements"][site_measurement_index]["AverageSpeed"] = float(
                        site_measurement_values_avg.text)

        except (KeyError, ValueError, AttributeError) as e:
            #print(f"Fehler bei Site {site_id}, Index {site_measurement_index}: {e}")
            pass
# JSON-Datei speichern
with open("output_Livedata.json", "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, indent=4, ensure_ascii=False)

    print("JSON-Datei erfolgreich gespeichert!")
