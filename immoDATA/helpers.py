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
    # Export the Results of the Web to Excel.
    results_web.data.to_excel(os.path.join(main_folder, "test.xlsx"), index=False)
    
def calculate_limit_date(last_days=5):
    # Calculate the Limit Date depending on the input.
    limit_date = datetime.now() - timedelta(days=last_days)
    
    return limit_date