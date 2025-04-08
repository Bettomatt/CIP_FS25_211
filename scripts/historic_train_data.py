import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

# Get the absolute path to the project directory (root of the repository)
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Define the path to the historic-data folder inside the 'data' directory within the project
HISTORIC_DATA_FOLDER = os.path.join(project_dir, 'data', 'historic-data')

# Make sure the folder exists (create it if it doesn't)
if not os.path.exists(HISTORIC_DATA_FOLDER):
    os.makedirs(HISTORIC_DATA_FOLDER)
    print(f"Folder created: {HISTORIC_DATA_FOLDER}")
else:
    print(f"Saving data in: {HISTORIC_DATA_FOLDER}")

# Define the base URL for fetching CSV links
BASE_URL = "https://data.opentransportdata.swiss/dataset/istdaten"


def fetch_csv_links():
    """Get links to all CSV files from the website"""
    response = requests.get(BASE_URL)

    if response.status_code != 200:
        print("Failed to fetch the webpage.")
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    links = []

    for link in soup.find_all("a", href=True):
        href = link["href"]
        if href.endswith(".csv"):
            full_url = urljoin(BASE_URL, href)
            links.append(full_url)

    return links


def download_csv(url):
    """Download the CSV file and save it to the folder"""
    filename = os.path.basename(url)
    csv_path = os.path.join(HISTORIC_DATA_FOLDER, filename)

    # Skip if file already exists
    if os.path.exists(csv_path):
        print(f"{filename} already exists.")
        return

    # Download the CSV file
    print(f"Downloading {filename}...")
    response = requests.get(url)

    if response.status_code == 200:
        with open(csv_path, "wb") as file:
            file.write(response.content)
        print(f"Downloaded {filename}.")
    else:
        print(f"Failed to download {filename}.")


if __name__ == "__main__":
    # Get all CSV links from the website
    csv_links = fetch_csv_links()

    # If there are links, download each CSV
    if csv_links:
        for link in csv_links:
            download_csv(link)
    else:
        print("No CSV links found.")

