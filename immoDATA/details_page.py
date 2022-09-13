# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 07:50:51 2022

@author: alber
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests

from bs4 import BeautifulSoup

import pandas as pd
import numpy as np

from datetime import timedelta, datetime

class DetailsPage():
    """
        Here page action of the Details page.
    """
    
    def __init__(self, website):
        # Get the Text page to further analyze with BeautifulSoup.
        text = requests.get(website).text
        # Parse with BeautifulSoup the text.
        self.doc = BeautifulSoup(text, "html.parser")
        # Data.
        self.data = pd.DataFrame(columns=["rent_wo_costs", "costs", "deposit", 
                                          "n_floor", "furnitures", "heating",
                                          "floor_type", "bath_type", "kitchen",
                                          "extra_features"])
        
    def get_costs_data(self):
        """
        Get the Costs data table.

        Returns
        -------
        rows_raw : TYPE
            DESCRIPTION.

        """
        # Initialize lists.
        rents_wo_costs = []
        costss = []
        deposits = []
        
        # Get the classes row noprint and translate into a DataFrame.
        costs_table_raw = self.doc.find_all("div", 
                                     {"class": ["col-sm-5"]})
        # Check if offer still available.
        if len(costs_table_raw) == 0:
            # Offer not available.
            return False
        # Select the first occurrence for costs_table_raw.
        costs_table_raw = costs_table_raw[0]
        
        # Checks if offer still available.
        if len(costs_table_raw.find_all("td")) == 0:
            return False
        
        # Rent without Costs.
        if "n.a." not in costs_table_raw.find_all("td")[1].get_text(strip=True):
                    rents_wo_costs.append(float(costs_table_raw.find_all("td")[1].get_text(strip=True).replace("€", "")))
        else:
            rents_wo_costs.append(np.nan)

        # Costs.
        if "n.a." not in costs_table_raw.find_all("td")[3].get_text(strip=True):
            costss.append(float(costs_table_raw.find_all("td")[3].get_text(strip=True).replace("€", "")))
        else:
            costss.append(np.nan)
            
        # Case Rent + Cost is NaN, then offer not available.
        if (rents_wo_costs[0] is np.nan) and (costss[0] is np.nan):
            return False
            
        # Extra Costs.
        #extra_costs = kosten_table_raw.find_all("td")[5].get_text(strip=True).replace("€", "")
        # Deposit.
        if len(costs_table_raw.find_all("td")) > 7:
            if "n.a." not in costs_table_raw.find_all("td")[7].get_text(strip=True):
                deposits.append(float(costs_table_raw.find_all("td")[7].get_text(strip=True).replace("€", "")))
            else:
                deposits.append(np.nan)
        else:
            deposits.append(np.nan)
        
        # Assign parameters to the data DataFrame.
        if len(rents_wo_costs) > 0:
            self.data["rent_wo_costs"] = rents_wo_costs
        if len(costss) > 0:
            self.data["costs"] = costss
        if len(deposits) > 0:
            self.data["deposit"] = deposits
            
        return True
    
    def get_pictures_data(self):
        """
        Get the Pictures data table.

        Returns
        -------
        rows_raw : TYPE
            DESCRIPTION.

        """
        # Initialize lists.
        n_floors = []
        furnituress = []
        heatings = []
        extra_featuress = []
        floor_types = []
        bath_types = []
        kitchens = []
        # Pictures Table.
        pictures_table_raw = self.doc.find_all("div", 
                                     {"class": ["col-xs-6 col-sm-4 text-center print_text_left"]})
        # Loop through the Pictures table raw and extract properties of the house.
        for picture in pictures_table_raw:
            # Case n_floor.
            if "mdi mdi-office-building mdi-36px noprint" in str(picture):
                n_floors.append(picture.get_text(strip=True))
            elif "mdi mdi-bed-double-outline mdi-36px noprint" in str(picture):
                furnituress.append(picture.get_text(strip=True))
            elif "mdi mdi-fire mdi-36px noprint" in str(picture):
                heatings.append(picture.get_text(strip=True))
            elif "mdi mdi-folder mdi-36px noprint" in str(picture):
                extra_featuress.append(picture.get_text(strip=True))
            elif "mdi mdi-layers mdi-36px noprint" in str(picture):
                floor_types.append(picture.get_text(strip=True))
            elif "mdi mdi-shower mdi-36px noprint" in str(picture):
                bath_types.append(picture.get_text(strip=True))
            elif "mdi mdi-silverware-fork-knife mdi-36px noprint" in str(picture):
                kitchens.append(picture.get_text(strip=True))
        
        # Assign parameters to the data DataFrame.
        if len(n_floors) > 0:
            self.data["n_floor"] = n_floors
        if len(furnituress) > 0:
            self.data["furnitures"] = furnituress
        if len(heatings) > 0: 
            self.data["heating"] = heatings
        if len(extra_featuress) > 0:
            self.data["extra_features"] = extra_featuress
        if len(floor_types) > 0:
            self.data["floor_type"] = floor_types
        if len(bath_types) > 0:
            self.data["bath_type"] = bath_types
        if len(kitchens) > 0:
            self.data["kitchen"] = kitchens   

        

        
            
        
    
    
        
        
    