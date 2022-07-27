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
from selenium.webdriver.support.ui import Select

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
    
    def set_select_filter(self, types):
        # Select Filter Find the Button.
        filter_select_button = self.driver.find_element(by=By.XPATH, 
                                                        value="//div[@class='filter-option-inner']")
        # Click in the Filter Select button to open the Dropdown menu.
        filter_select_button.click()
        
        # Get the Elements Selected.
        selected_elements = self.driver.find_elements(by=By.XPATH,
                                  value="//ul[@class='dropdown-menu inner ']/li[@class='selected']")
        # Generate a List with the selected Elements.
        list_selected_elements = []
        for elem in selected_elements:
            list_selected_elements.append(elem.text)
        
        # Get the Elements of the List.
        wg_zimmer_element = self.driver.find_elements(by=By.XPATH,
                                  value="//ul[@class='dropdown-menu inner ']/li")[0]
        # Enable/Disable WG-Zimmer element.
        self.enable_disable_dropdown_element(element=wg_zimmer_element, 
                                        string_element="WG-Zimmer", 
                                        list_selected_elements=list_selected_elements, 
                                        types_dict=types)
        
        one_zimmer_wohnung_element = self.driver.find_elements(by=By.XPATH,
                                  value="//ul[@class='dropdown-menu inner ']/li")[1]
        # Enable/Disable 1-Zimmer-Wohnung element.
        self.enable_disable_dropdown_element(element=one_zimmer_wohnung_element, 
                                        string_element="1-Zimmer-Wohnung", 
                                        list_selected_elements=list_selected_elements, 
                                        types_dict=types)
        wohnung_element = self.driver.find_elements(by=By.XPATH,
                                  value="//ul[@class='dropdown-menu inner ']/li")[2]
        # Enable/Disable Wohnung element.
        self.enable_disable_dropdown_element(element=wohnung_element, 
                                        string_element="Wohnung", 
                                        list_selected_elements=list_selected_elements, 
                                        types_dict=types)
        haus_element = self.driver.find_elements(by=By.XPATH,
                                  value="//ul[@class='dropdown-menu inner ']/li")[3]
        # Enable/Disable Haus element.
        self.enable_disable_dropdown_element(element=haus_element, 
                                        string_element="Haus", 
                                        list_selected_elements=list_selected_elements, 
                                        types_dict=types)
    
    def enable_disable_dropdown_element(self, element, string_element, list_selected_elements, types_dict):
        """
        Enable/Disable the Element in the Dropdown Menu for the Wohnung Type.

        Parameters
        ----------
        element : TYPE
            DESCRIPTION.
        string_element : TYPE
            DESCRIPTION.
        list_selected_elements : TYPE
            DESCRIPTION.
        types_dict : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        # Case True: if not selected, click.
        if types_dict[string_element] == True:
            # Check if WG-Zimmer is in the selected elements list, if not click.
            if string_element not in list_selected_elements:
                element.click()
        elif types_dict[string_element] == False:
            # Check if WG-Zimmer is not in the selected elements list, if yes click to disable.
            if string_element in list_selected_elements:
                element.click()