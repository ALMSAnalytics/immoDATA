# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 07:00:11 2022

@author: alber
"""

import pandas as pd
import os
from datetime import datetime, timedelta

# Main Folder for the results.
main_folder = r"c:\immoDATA_dB"

def export_excel(results_web):
    # City.
    # Case we have the City read.
    if len(results_web.cities) > 0:
        city = results_web.cities[0]
        # Export the Results of the Web to Excel.
        results_web.data.to_excel(os.path.join(main_folder, city + ".xlsx"), index=False,
                                  sheet_name="data")
    
def calculate_limit_date(last_days=5):
    # Calculate the Limit Date depending on the input.
    limit_date = datetime.now() - timedelta(days=last_days)
    
    return limit_date

def remove_duplicates_for_export(results_web):
    results_web.data = results_web.data.drop_duplicates(subset=["link", "n_room", "city", "area",
                                             "street"])
    
    return results_web.data

def remove_temporary_houses_for_export(results_web):
    results_web.data = results_web.data[results_web.data["end_date"].isna()]
    
    return results_web.data

def remove_already_rented_houses_start_date(results_web):
    results_web.data = results_web.data[results_web.data["start_date"].isna() == False]
    
    return results_web.data

def remove_person_searches_ads(results_web):
    results_web.data = results_web.data[~results_web.data["title"].str.contains("^Suche ", regex=True)]
    
    return results_web.data

def read_inputs_cities(cities_file=r"inputs\cities.xlsx"):
    # Read Excel with Input Cities.
    df_cities = pd.read_excel(cities_file, sheet_name="Munich_Area")
    # List Cities.
    list_cities = list(df_cities["Stadt/Gemeinde"])
    
    return list_cities

def set_temp_csv_folder_files(csv_folder_temp_data=r"C:\csv_temp_data"):
    # Checks if the CSV folder temp is created or not.
    if os.path.exists(csv_folder_temp_data) == False:
        # Create Dir.
        os.mkdir(csv_folder_temp_data)
        
    # CSV individual items.
    house_csv_file = os.path.join(csv_folder_temp_data, "house.csv")
    city_csv_file = os.path.join(csv_folder_temp_data, "city.csv")
    area_csv_file = os.path.join(csv_folder_temp_data, "area.csv")
    type_csv_file = os.path.join(csv_folder_temp_data, "type.csv")
    vendor_csv_file = os.path.join(csv_folder_temp_data, "vendor.csv")
    heating_csv_file = os.path.join(csv_folder_temp_data, "heating.csv")
    
    return house_csv_file, city_csv_file, area_csv_file, type_csv_file, vendor_csv_file, heating_csv_file

def set_df_tables():
    # DataFrames for the Tables.
    df_house = pd.DataFrame(columns=["title", "link", "n_room", "address", "start_date", "price",
                                       "rent_wo_costs", "costs", "deposit", "size",
                                       "author", "publication_date", "n_floor", "floor_type",
                                       "kitchen", "bath_type", "furnitures", "heating",
                                       "extra_features", "type", "city", "area", "vendor"])
    
    df_city = pd.DataFrame(columns=["name"])
    df_area = pd.DataFrame(columns=["name"])
    df_type = pd.DataFrame(columns=["name"])
    df_vendor = pd.DataFrame(columns=["name"])
    df_heating = pd.DataFrame(columns=["name"])
    
    return df_house, df_city, df_area, df_type, df_vendor, df_heating

def rename_innenstadt_with_city(df_area, city):
    df_area = df_area.replace(r"innenstadt", city + "_innenstadt", regex=True)
    df_area = df_area.replace(r"zentrum", city + "_zentrum", regex=True)
    
    return df_area

def remove_city_name_from_df_area(df_area, city):
    df_area["name"] = [x.replace(city.lower(), "") for x in df_area["name"]]
    
    return df_area
    
    