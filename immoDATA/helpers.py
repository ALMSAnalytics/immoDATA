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

def read_inputs_cities(cities_file=r"inputs\cities.xlsx"):
    # Read Excel with Input Cities.
    df_cities = pd.read_excel(cities_file, sheet_name="Munich_Area")
    # List Cities.
    list_cities = list(df_cities["Stadt/Gemeinde"])
    
    return list_cities
    