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
    "SoapAction": "http://opentransportdata.swiss/TDP/Soap_Datex2/Pull/v1/pullMeasurementSiteTable"  # Erforderliche SOAP Action
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
    #print(response.text)

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


# XML einlesen (angenommen, response.text enthält die XML-Daten)
root = ET.fromstring(response.text)
namespace = {'dx223': 'http://datex2.eu/schema/2/2_0'}

# Alle measurementSiteRecords finden
measurementSiteRecords = root.findall('.//dx223:measurementSiteRecord', namespace)

# Dictionary für die JSON-Daten
data = {}

for elem in measurementSiteRecords:
    Site_ID = elem.attrib["id"]
    Site_Version = elem.attrib["version"]

    # Allgemeine Informationen extrahieren
    def get_text(element):
        return element.text if element is not None else None

    MeasurementSiteNumberOfLanes = get_text(elem.find(".//dx223:measurementSiteNumberOfLanes", namespace))
    Carriageway = get_text(elem.find(".//dx223:carriageway", namespace))
    Lane = get_text(elem.find(".//dx223:lane", namespace))
    Latitude = get_text(elem.find(".//dx223:latitude", namespace))
    Longitude = get_text(elem.find(".//dx223:longitude", namespace))

    # Struktur im Dictionary anlegen
    data[Site_ID] = {
        "version": Site_Version,
        "number_of_lanes": MeasurementSiteNumberOfLanes,
        "carriageway": Carriageway,
        "lane": Lane,
        "latitude": Latitude,
        "longitude": Longitude,
        "measurements": []  # Liste für die Messwerte
    }

    # Messwerte pro Site_ID sammeln
    MeasurementSpecificCharacteristics_List = elem.findall(".//dx223:measurementSpecificCharacteristics", namespace)

    for elem_Level2 in MeasurementSpecificCharacteristics_List:
        try:
            measurementIndex = int(elem_Level2.attrib["index"])
            specificMeasurementValueType = get_text(elem_Level2.find(".//dx223:specificMeasurementValueType", namespace))
            vehicleType = get_text(elem_Level2.find(".//dx223:vehicleType", namespace))

            # Messwert in die Liste einfügen
            data[Site_ID]["measurements"].append({
                "index": measurementIndex,
                "value_type": specificMeasurementValueType,
                "vehicle_type": vehicleType
            })

        except (KeyError, ValueError, AttributeError) as e:
            print(f"Fehler bei Site {Site_ID}, Index {measurementIndex}: {e}")


# JSON-Datei speichern
with open("output_Site-Data.json", "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, indent=4, ensure_ascii=False)

#print("JSON-Datei erfolgreich gespeichert!")


