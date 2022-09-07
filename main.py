# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 07:15:40 2022

@author: alber
"""

from immoDATA.main_page import MainPage
from immoDATA.results_page import ResultsPage
from immoDATA.helpers import export_excel, calculate_limit_date, remove_duplicates_for_export, read_inputs_cities
from immoDATA.immoDB import immoDB

import pandas as pd

import time

# Main Website.
website = "https://www.wg-gesucht.de/"
# City in Germany.
cities_list = read_inputs_cities()
cities_list = cities_list[1:]
#cities_list.reverse()
# True/False depending on the house type you want.
types = {"WG-Zimmer": False, "1-Zimmer-Wohnung": False,
         "Wohnung": True, "Haus": False}
# Angebote or Gesuche.
angebot_gesuche = "Angebote"

if __name__ == "__main__":
    # Loop through all the Cities in the list.
    for city in cities_list:
        print("Scraping data for city: " + city)
        ##########################################
        ###### DB QUERY current information ######
        ##########################################
        # Read immoDB about the city.
        immoDB_city = immoDB(city=city)
        # Checks if we have already the Excel or not.
        if immoDB_city.data is None:
            # City not in dB.
            city_in_dB = False
            # Calculate Limit Date, up to 7 days.
            limit_date = calculate_limit_date(last_days=7)
        else:
            # City in dB.
            city_in_dB = True
            # Get Latest Publication Date.
            limit_date = immoDB_city.get_latest_publication_date()
        
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
        
        # While Limit Date is not reach, then follow go to next page and retrieve data.
        while len(results_web.data[results_web.data["publication_date"] < limit_date]) == 0:
            # Go to the Next Page.
            new_results_URL = results_web.go_to_next_page(driver=main_web.driver)
            time.sleep(5)
            # Create a ResultsPage object with the Results for URL.
            new_results_web = ResultsPage(website=new_results_URL)
            # Get the Full Data for the New Page Results.
            new_results_web.get_full_results_data()
            # Concat the Results to the Final Object.
            results_web.data = pd.concat([results_web.data, new_results_web.data], axis=0)
        
        # Quit the Driver.
        main_web.quit_driver()
        
        # If city in dB, concatenate the results with the ones in immodB.
        if city_in_dB:
            # Concatenate in results_web.
            results_web.data = pd.concat([results_web.data, immoDB_city.data], axis=0)
        
        # Remove Duplicates before exporting.
        results_web.data = remove_duplicates_for_export(results_web)
        
        # Export to Excel.
        export_excel(results_web)
        
        # Time Sleep.
        print("Sleeping...")
        time.sleep(120)
    