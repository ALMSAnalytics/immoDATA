# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 07:15:40 2022

@author: alber
"""

from immoDATA.main_page import MainPage
from immoDATA.results_page import ResultsPage

# Define variables.
website = "https://www.wg-gesucht.de/"
city = "München"
types = {"WG-Zimmer": False, "1-Zimmer-Wohnung": False,
         "Wohnung": False, "Haus": False}

if __name__ == "__main__":
    # Get the Web with ChromeDriverManager.
    main_web = MainPage(website=website)
    # Accept the Cookies of the Main Page.
    main_web.accept_cookies()
    # Input the City.
    main_web.enter_input_city(city=city)
    # Set Filter Select.
    a=main_web.set_select_filter(types=types)
    # # Click Search Button.
    # main_web.click_search_button()
    # # Wait for Results Page and get Results URL.
    # results_URL = main_web.wait_results_get_results_page()
    
    # # Initialize Results Page.
    # results_web = ResultsPage(website=results_URL)
    # # Get the Raw Rows from the Results document.
    # rows_raw = results_web.get_raw_rows()
    # # Get the Data from raw rows.
    # results_web.get_results_data(rows_raw=rows_raw)
    
    