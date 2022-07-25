# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 07:13:20 2022

@author: alber
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class MainPage():
    """ Main page action methods come here.
        https://www.wg-gesucht.de/
    """
    
    def __init__(self, website):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get(website)

    def accept_cookies(self):
        """
        Accept the cookies in the main page.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """

        # Accept Cookies.
        # Wait until the Cookies object is visible. 10 seconds is the timeout.
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "cmpbntyestxt")))
        # Find Element and Click.
        cookie_button = self.driver.find_element(by=By.ID, value="cmpbntyestxt")
        cookie_button.click()

    def enter_input_city(self, city):
        """
        Enter the Input City in the main page.

        Parameters
        ----------
        driver : TYPE
            DESCRIPTION.
        city : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """

        # Input City, find the element.
        input_city = self.driver.find_element(by=By.ID, value="autocompinp")
        # Send the name of the city.
        input_city.send_keys(city)
        # Wait until the Autocomplete suggestion is showed.
        WebDriverWait(self.driver, 
                      10).until(EC.visibility_of_element_located((By.CLASS_NAME, "autocomplete-suggestion")))
        # Enter the autocompletion suggestion.
        input_city.send_keys(Keys.ENTER)
        
    def click_search_button(self):
        """
        Click the search button.

        Parameters
        ----------
        driver : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        
        # Search Button Click.
        search_button = self.driver.find_element(by=By.ID, value="search_button")
        search_button.click()
        
    def wait_results_get_results_page(self):
        """
        Wait until Results Page is loaded and return Results web URL.

        Returns
        -------
        current_url : TYPE
            DESCRIPTION.

        """
        
        # Wait until the Results page is loaded, with 10 seconds of timeout.
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "dropdownMenu1")))
        # Get Results Page.
        current_url = self.driver.current_url
        
        return current_url