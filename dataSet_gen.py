#!/usr/bin/env python3

import json
import requests
from PIL import Image
import os
from tqdm import tqdm

"""
    Load data from a JSON file.

    Parameters:
    - file_path (str): The path to the JSON file.

    Returns:
    - dict: The data as a dictionary.
"""
def load_data_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

"""
    Check if a file exists.

    Parameters:
    - file_path (str): The path to the file.

    Returns:
    - bool: True if the file exists, False otherwise.
""" 
def file_exists(file_path):
    return os.path.exists(file_path)

"""
    Gets the up to date url pointer for bulk card data

    Parameters:
    - URL (str): Scryfall url to get bulkcard list data

    Returns:
    - URI (str): URI for card info download

"""
def get_scryfall_bulkdata_url(url):
    print("tring to get uptodate card list")
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
    Runs through list of cards and download images of relivent cards    

    Parameters:
    - output_folder (str): The name of the location where images are stored.
    - cardlist (str): name of json file containing the list of cards
    - filter_data (dic): dic of layout types for filtering
"""
def get_cardimages(output_folder, cardlist, filter_data):

    clist = load_data_from_json(cardlist) 

    for card in tqdm(clist, desc="Downloading Images"):
        if filter_data[card["layout"]]:
            file = output_folder + "(" + card["set_id"] + ")_"+card["id"] + ".jpg"
            if not file_exists(file):
                match(card["layout"]):
                    case "normal" | "adventure" | "leveler" | "prototype" | "mutate":
                        if (not (card["full_art"] and ("Basic Land" in card["type_line"]) )):
                            download_file(card["image_uris"]["normal"], file)
                    case "modal_dfc":
                        download_file(card["card_faces"][0]["image_uris"]["normal"], file)
                        download_file(card["card_faces"][1]["image_uris"]["normal"], file)
                    case _:
                        print("something went very wrong")
        else:
            None

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

        #print(f"Downloaded: {file_name}")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading file from {url}: {e}")

"""
    Take card images and remove everything other than set symbol area

    Parameters:
    - input_path(str): string containing the path to the card images.
    - output_path (str): string containing the location to save cropped images.
"""
def crop_setsymbols(input_path, output_path):
    
    # Create the output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)
    
    # List all files in the input directory
    file_list = os.listdir(input_path)
    
    crop_box = (350,325,475,450)  # (left, upper, right, lower)
    for image_name in tqdm(file_list, desc="Cropping Set Symbols"):
        image_path = os.path.join(input_path, image_name)
        result_path = os.path.join(output_path,image_name)

        if os.path.isfile(image_path) and image_name.lower().endswith('.jpg') and not file_exists(result_path):
            image = Image.open(image_path)

            result = image.crop(crop_box) #normal image size(488x680)

            result.save(result_path)

"""
    Applies multiple different augments to image and saves them

    Parameters:
    - image_path (str): path to folder containing images
    - dataset_path(str): path to where images need to be saved
"""
def image_augment(image_path,dataset_path ):
    os.makedirs(dataset_path, exist_ok=True)

    file_list = os.listdir(image_path)

    for image in tqdm(file_list, desc="Creating Dataset"):
        None

filter_file = "card_layout.json"
scryfall_url = "https://api.scryfall.com/bulk-data"

card_img_folder = "card_images/"
set_symbol_folder = "set_symbols/"
dataset_folder = "symbol_data_set/"
if not os.path.isdir(card_img_folder):
    os.makedirs(card_img_folder)
    

def main():

    #import list of layout types
    filter_data = load_data_from_json(filter_file)

    #download current list of cards from scryfall
    bulkdata_uri = get_scryfall_bulkdata_url(scryfall_url)
    download_file(bulkdata_uri, "bulk_card_list.json")

    #sort list of cards downloading images from layouts that are acceptable
    print("Checking for cards to download(this may take a while)")
    get_cardimages(card_img_folder,"bulk_card_list.json", filter_data)
    
    #crop out the set images
    print("Creating set symbols(this may take a while)")
    crop_setsymbols(card_img_folder, set_symbol_folder)
    
    #aply any filters and variations to the cards

if __name__ == "__main__":
    main()
    
