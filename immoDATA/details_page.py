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
        Here page action of the Results page.
    """
    
    def __init__(self, website):
        # Get the Text page to further analyze with BeautifulSoup.
        text = requests.get(website).text
        # Parse with BeautifulSoup the text.
        self.doc = BeautifulSoup(text, "html.parser")
        # Kautions list.
        self.kautions = []
        # Data.
        self.data = pd.DataFrame(columns=["kaution"])
        
            
        
    
    
        
        
    