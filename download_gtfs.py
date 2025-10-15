#!/usr/bin/env python3
import argparse
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def main():
    parser = argparse.ArgumentParser(
        description="Download all GTFS zip files from https://api.transitous.org/gtfs/ with a given prefix."
    )
    parser.add_argument("prefix", help="Prefix of the GTFS zip files (e.g., 'de', 'ch', etc.)")
    args = parser.parse_args()

    base_url = "https://api.transitous.org/gtfs/"
    prefix = args.prefix + "_"

    print(f"Fetching GTFS index from {base_url}...")
    response = requests.get(base_url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a")

    matching_files = [
        link.get("href")
        for link in links
        if link.get("href") and link.get("href").startswith(prefix) and link.get("href").endswith(".zip")
    ]

    if not matching_files:
        print(f"No files found with prefix '{prefix}'.")
        return

    print(f"Found {len(matching_files)} files with prefix '{prefix}':")
    for filename in matching_files:
        print(f"  - {filename}")

    for filename in matching_files:
        file_url = urljoin(base_url, filename)
        output_path = filename

        print(f"Downloading {filename} ...", end=" ", flush=True)
        with requests.get(file_url, stream=True) as r:
            r.raise_for_status()
            with open(output_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print("✅ done")

    print("All files downloaded!")

if __name__ == "__main__":
    main()
