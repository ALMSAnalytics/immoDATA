# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 07:15:40 2022

@author: alber
"""

from immoDATA.main_page import MainPage
from immoDATA.results_page import ResultsPage
from immoDATA.helpers import export_excel, calculate_limit_date, remove_duplicates_for_export
from immoDATA.immoDB import immoDB

import pandas as pd

# Main Website.
website = "https://www.wg-gesucht.de/"
# City in Germany.
city = "München"
# True/False depending on the house type you want.
types = {"WG-Zimmer": False, "1-Zimmer-Wohnung": False,
         "Wohnung": True, "Haus": False}
# Angebote or Gesuche.
angebot_gesuche = "Angebote"

if __name__ == "__main__":
    ##########################################
    ###### DB QUERY current information ######
    ##########################################
    # Read immoDB about the city.
    immoDB_city = immoDB(city=city)
    # Get Latest Publication Date.
    latest_publication_date_DB = immoDB_city.get_latest_publication_date()
    
    ##########################################
    ###### MAIN WEB and get the Results ######
    ##########################################
    # Get the Web with ChromeDriverManager.
    main_web = MainPage(website=website)
    # Accept the Cookies of the Main Page.
    main_web.accept_cookies()
    # Input the City.
    main_web.enter_input_city(city=city)
    # Set Filter Select House Type.
    main_web.set_select_filter_house_type(types=types)
    # Angebote/Gesuche Set.
    main_web.set_select_angebote_gesuche(angebot_gesuche)
    # Click Search Button.
    main_web.click_search_button()
    # Wait for Results Page and get Results URL.
    results_URL = main_web.wait_results_get_results_page()
    
    # # Initialize Results Page.
    # results_web = ResultsPage(website=results_URL)
    # # Get the Raw Rows from the Results document.
    # rows_raw = results_web.get_raw_rows()
    # # Get the Data from raw rows.
    # results_web.get_results_data(rows_raw=rows_raw)
    
    # Create a ResultsPage object with the Results for URL and get the full results data.
    results_web = ResultsPage(website=results_URL)
    results_web.get_full_results_data()
    
    # Calculate Limit Date, up to 7 days.
    limit_date = calculate_limit_date(last_days=7)
    # While Limit Date is not reach, then follow go to next page and retrieve data.
    while len(results_web.data[results_web.data["publication_date"] < limit_date]) == 0:
        # Go to the Next Page.
        new_results_URL = results_web.go_to_next_page(driver=main_web.driver)
        # Get the Data.
        # # Initialize Results Page.
        # new_results_web = ResultsPage(website=new_results_URL)
        # # Get the Raw Rows from the Results document.
        # new_rows_raw = new_results_web.get_raw_rows()
        # # Get the Data from raw rows.
        # new_results_web.get_results_data(rows_raw=new_rows_raw)
        # Create a ResultsPage object with the Results for URL.
        new_results_web = ResultsPage(website=new_results_URL)
        # Get the Full Data for the New Page Results.
        new_results_web.get_full_results_data()
        # Concat the Results to the Final Object.
        results_web.data = pd.concat([results_web.data, new_results_web.data], axis=0)
    
    # Quit the Driver.
    main_web.quit_driver()
    
    # Remove Duplicates before exporting.
    results_web.data = remove_duplicates_for_export(results_web)
    
    # Export to Excel.
    export_excel(results_web)
    
    