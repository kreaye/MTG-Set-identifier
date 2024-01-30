#!/usr/bin/env python3

import json
import requests
import os

"""
    Load data from a JSON file.

    Parameters:
    - file_path (str): The path to the JSON file.

    Returns:
    - dict: The data as a dictionary.
"""
def load_data_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

"""
    Gets the up to date url pointer for bulk card data

    Parameters:
    - URL (str): Scryfall url to get bulkcard list data

    Returns:
    - URI (str): URI for card info download

"""
def get_scryfall_bulkdata_url(url):
    
    try:
        response = requests.get(url)
        response.raise_for_status()

        bulk_data = response.json()

        for entry in bulk_data["data"]:
            #print( f" {entry["id"]} : {entry["type"]}"  )
            if entry["type"] == "unique_artwork":
                return entry["download_uri"]
            
        print("there was an error getting uri")
    
    except requests.exceptions.RequestException as e:
        print(f"Error downloading bulk data: {e}")

"""
    Download a file from a URL and save it to the specified file name.

    Parameters:
    - url (str): The URL of the file to download.
    - file_name (str): The name of the file to save.
"""
def download_file(url, file_name):

    try:
        # Make a request to download the file
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        # Save the file
        with open(file_name, "wb") as file:
            file.write(response.content)

        print(f"Downloaded: {file_name}")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading file from {url}: {e}")


filter_file = "card_layout.json"
card_img_folder = "card_images/"
scryfall_url = "https://api.scryfall.com/bulk-data"

def main():

    #import list of layout types
    filter_data = load_data_from_json(filter_file)

    #download current list of cards from scryfall
    bulkdata_uri = get_scryfall_bulkdata_url(scryfall_url)
    download_file(bulkdata_uri, "bulk_card_list.json")
    #sort list of cards downloading images from layouts that are acceptable

    #crop out the set images

    #aply any filters and variations to the cards

if __name__ == "__main__":
    try:
        main()
    except:
        print("process failed")
