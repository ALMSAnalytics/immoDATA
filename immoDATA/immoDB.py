# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 10:29:21 2022

@author: alber
"""

import pandas as pd
import os

main_folder = r"c:\immoDATA_dB"

class immoDB():
    """
        Here functions with the immoDB.
    """
    
    def __init__(self, city):
        # Excel folder.
        self.excel_main_folder = main_folder
        # City to check.
        self.city = city
        # Read Excel data.
        self.data = pd.read_excel(os.path.join(self.excel_main_folder, self.city + ".xlsx"))
        
    def get_latest_publication_date(self):
        # Get the Latest Publication Date from the Excel.
        latest_publication_date = self.data["publication_date"][0]
        
        return latest_publication_date