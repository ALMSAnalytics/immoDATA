# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 07:15:40 2022

@author: alber
"""

from immoDATA.main_page import MainPage
from immoDATA.results_page import ResultsPage
from immoDATA.helpers import calculate_limit_date, remove_duplicates_for_export, remove_person_searches_ads
from immoDATA.helpers import read_inputs_cities, remove_temporary_houses_for_export
from immoDATA.helpers import remove_already_rented_houses_start_date, rename_innenstadt_with_city
from immoDATA.helpers import set_temp_csv_folder_files, set_df_tables, remove_city_name_from_df_area
from immoDATA.immoDB import immoDB
from immoDATA.details_page import DetailsPage

import pandas as pd
import numpy as np

import time

from itertools import islice

# Main Website.
website = "https://www.wg-gesucht.de/"
# City in Germany.
cities_list = read_inputs_cities()
#cities_list = cities_list[23:]
#cities_list.reverse()
# True/False depending on the house type you want.
types = {"WG-Zimmer": False, "1-Zimmer-Wohnung": False,
         "Wohnung": True, "Haus": False}
# Angebote or Gesuche.
angebot_gesuche = "Angebote"

# List of length in which we have to split.
block_n_cities = 5
length_to_split = [block_n_cities for x in list(range(0, int(np.ceil(len(cities_list)/block_n_cities))))]
length_to_split[-1] = int(len(cities_list)%3)
 
# Using islice.
input_list = iter(cities_list)
output_list = [list(islice(input_list, elem)) for elem in length_to_split]

# Connect with immoDB database.
immoDB_obj = immoDB()
immoDB_obj.connect()

# Create Tables for immoDB.
#immoDB_obj.create_tables_immoDB()

if __name__ == "__main__":
    # Loop through the Sublists with Cities in the Output List.
    for cities in output_list:
        # Loop through all the Cities in the list.
        for city in cities:
            print("Scraping data for city: " + city)
            # Initialize go_to_next_page.
            go_next_page = True
            # Set CSV temporary files.
            house_csv_file, city_csv_file, area_csv_file, type_csv_file, vendor_csv_file, heating_csv_file = \
                set_temp_csv_folder_files()
            # Initialize DataFrames.
            df_house, df_city, df_area, df_type, df_vendor, df_heating = set_df_tables()
            ##########################################
            ###### DB QUERY current information ######
            ##########################################
            # Read immoDB about the city.

            # Calculate Limit Date, up to 7 days.
            limit_date = calculate_limit_date(last_days=7)
            
            ##########################################
            ###### MAIN WEB and get the Results ######
            ##########################################
            # Get the Web with ChromeDriverManager.
            main_web = MainPage(website=website)
            time.sleep(2)
            # Accept the Cookies of the Main Page.
            main_web.accept_cookies()
            # Input the City.
            time.sleep(2)
            main_web.enter_input_city(city=city)
            # Set Filter Select House Type.
            time.sleep(2)
            main_web.set_select_filter_house_type(types=types)
            # Angebote/Gesuche Set.
            time.sleep(2)
            #main_web.set_select_angebote_gesuche(angebot_gesuche)
            # Click Search Button.
            time.sleep(2)
            main_web.click_search_button()
            # Wait for Results Page and get Results URL.
            results_URL = main_web.wait_results_get_results_page()
            
            # Create a ResultsPage object with the Results for URL and get the full results data.
            results_web = ResultsPage(website=results_URL)
            # Click Weitere Filter.
            results_web.click_weitere_filter_button(driver=main_web.driver)
            time.sleep(2)
            results_web.set_maximal_distance(driver=main_web.driver)
            time.sleep(0.5)
            results_web.click_filter_anwenden(driver=main_web.driver)
            time.sleep(2)
            # Get Data.
            results_web.get_full_results_data()
            
            # Checks in the results_web data if we already have any ad.
            links_already_in_DB = results_web.data["link"].apply(immoDB_obj.exists_link_house)
            # Check if we have any True, meaning there are registries already in DB.
            links_in_DB = links_already_in_DB[links_already_in_DB == True]
            # Case we have True, we have something in DB, no need to go next page.
            if len(links_in_DB) > 0:
                # Select until the True index.
                last_index = links_in_DB.index[0]
                # Change Results_web data.
                results_web.data = results_web.data.loc[:last_index-1,:]
                # Go to next page.
                go_next_page = False
            
            # While Limit Date is not reach, then follow go to next page and retrieve data.
            if go_next_page == True:
                while (len(results_web.data[results_web.data["publication_date"] < limit_date]) == 0) \
                    and go_next_page == True:
                    # Go to the Next Page.
                    try:
                        new_results_URL = results_web.go_to_next_page(driver=main_web.driver)
                    except:
                        continue
                    
                    time.sleep(5)
                    # Create a ResultsPage object with the Results for URL.
                    new_results_web = ResultsPage(website=new_results_URL)
                    # Get the Full Data for the New Page Results.
                    new_results_web.get_full_results_data()
                    # Checks in the results_web data if we already have any ad.
                    links_already_in_DB = new_results_web.data["link"].apply(immoDB_obj.exists_link_house)
                    # Check if we have any True, meaning there are registries already in DB.
                    links_in_DB = links_already_in_DB[links_already_in_DB == True]
                    # Case we have True, we have something in DB, no need to go next page.
                    if len(links_in_DB) > 0:
                        # Select until the True index.
                        last_index = links_in_DB.index[0]
                        # Change Results_web data.
                        new_results_web.data = new_results_web.data.loc[:last_index-1,:]
                        # Go to next page.
                        go_next_page = False
                    # Concat the Results to the Final Object.
                    results_web.data = pd.concat([results_web.data, new_results_web.data], axis=0)
            
            # Quit the Driver.
            main_web.quit_driver()
            
            # Remove Duplicates before exporting.
            results_web.data = remove_duplicates_for_export(results_web)
            # Remove Temporary Houses before exporting.
            results_web.data = remove_temporary_houses_for_export(results_web)
            # Remove Ads from people searching for flat.
            results_web.data = remove_person_searches_ads(results_web)
            # Remove Already Rented Houses with Start Date empty.
            results_web.data = remove_already_rented_houses_start_date(results_web)
            # Reset the Index to Match with the Details.
            results_web.data = results_web.data.reset_index(drop=True)  
            
            # Loop through the Link of the Results Web.
            df_full_details = pd.DataFrame()
            n_links = len(results_web.data["link"])
            indexes_details_list = []
            for i, link in enumerate(results_web.data["link"]):
                print(str(i+1) + "/" + str(n_links) + " - " + link)
                # Create a DetailsPage object with the Link for the Results.
                details_web = DetailsPage(website=link)
                # Get the Costs data.
                is_data_there = details_web.get_costs_data()
                # If Data is NOT There, Offer probably already OFF, next iteration.
                if is_data_there == False:
                    # Next iteration.
                    continue
                # Get Features of the House.
                details_web.get_pictures_data()
                # Concat for the full Details DataFrame.
                df_full_details = pd.concat([df_full_details, details_web.data], axis=0)
                # Add the index.
                indexes_details_list.append(i)
            # Reindex the DataFrame with the full Details.
            df_full_details.index = indexes_details_list
            
            # Concat and generate DataFrame to Export.
            df_to_export = pd.concat([results_web.data, df_full_details], axis=1, join="inner")
            # Assign to results_web object.
            results_web.data = df_to_export
            
            # Assign Results Web Data to df_house.
            if len(results_web.data) == 0:
                continue
            df_house = results_web.data[df_house.columns]
            # Assign City.
            df_city["name"] = list(df_house["city"].unique())
            # Assign Vendor.
            df_vendor["name"] = list(df_house["vendor"].unique())
            # Assign Type.
            df_type["name"] = list(df_house["type"].unique())
            # Assign Area.
            df_area["name"] = list(df_house["area"].unique())
            # Remove City from Area.
            if (df_area["name"][0] == df_city["name"][0]) == False:
                df_area = remove_city_name_from_df_area(df_area, city=df_city["name"][0])
            # Rename Innenstadt with City.
            df_area = rename_innenstadt_with_city(df_area, city=df_city["name"][0])
            df_house.loc[:, "area"] = rename_innenstadt_with_city(df_house["area"], city)
            # Assign Heating.
            df_heating["name"] = list(df_house["heating"].unique())
            # Drop NA for heating.
            df_heating = df_heating.dropna()
            
            # COPY AND EXPORT THE DataFrames INTO IMMODB.
            # house_raw table.
            immoDB_obj.csv_export_and_copy_to_db(house_csv_file, 
                                                  df_house, 
                                                  "house_raw")
            # city table.
            df_city = df_city[df_city["name"].apply(immoDB_obj.is_city_exists) == False]
            if len(df_city) > 0:
                immoDB_obj.csv_export_and_copy_to_db(city_csv_file, 
                                                      df_city, 
                                                      "city")
            # vendor table.
            df_vendor = df_vendor[df_vendor["name"].apply(immoDB_obj.is_vendor_exists) == False]
            if len(df_vendor) > 0:
                immoDB_obj.csv_export_and_copy_to_db(vendor_csv_file, 
                                                      df_vendor, 
                                                      "vendor")
            # type table.
            df_type = df_type[df_type["name"].apply(immoDB_obj.is_type_exists) == False]
            if len(df_type) > 0:
                immoDB_obj.csv_export_and_copy_to_db(type_csv_file, 
                                                      df_type, 
                                                      "type")
            # area table.
            df_area = df_area[df_area["name"].apply(immoDB_obj.is_area_exists) == False]
            if len(df_area) > 0:
                immoDB_obj.csv_export_and_copy_to_db(area_csv_file, 
                                                      df_area, 
                                                      "area")
            # heating table.
            df_heating = df_heating[df_heating["name"].apply(immoDB_obj.is_heating_exists) == False]
            if len(df_heating) > 0:
                immoDB_obj.csv_export_and_copy_to_db(heating_csv_file, 
                                                      df_heating, 
                                                      "heating")
                
            # Normalize house table.
            immoDB_obj.normalize_house(city_name=city.lower().replace("ü", 
                                                                      "u").replace("ö", 
                                                                                   "o").replace("ä", 
                                                                                                "a").replace("ß", 
                                                                                                             "ss"))
            
            # Truncate RAW table for houses.
            immoDB_obj.truncate_raw_tables()
            
            
            # Time Sleep.
            print("Sleeping...")
            time.sleep(30)
            
        # Time Sleep.
        print("Big Sleeping after chunk of " + str(block_n_cities) + " Cities...")
        time.sleep(1800)

# Disconnect from immoDB database.
immoDB_obj.disconnect()
        
    