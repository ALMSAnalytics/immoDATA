# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 10:29:21 2022

@author: alber
"""

# Import necessary modules.
from configparser import ConfigParser
import psycopg2
import pandas as pd
import os

# Database Creation: CREATE DATABASE immodb;
# User Creation: CREATE USER waits WITH PASSWORD 'bitchesbrew';

class immoDB():
    """
        Here functions with the immoDB.
    """
    
    def __init__(self, filename="database.ini", section="postgresql_immoDB"):
        # Create Parser.
        parser = ConfigParser()
        # Read the Config File.
        parser.read(filename)
        # Get Section.
        db = {}
        if parser.has_section(section):
            # Get Parameters of the Section.
            params = parser.items(section)
            # Loop through the Parameters and add to Dict.
            for param in params:
                db[param[0]] = param[1]
        else:
            # Case we do not have that section, raise the error.
            raise Exception("Section {0} not found in the {1} file".format(section, filename))
        # Assign the dB object.
        self.db_object = db
        self.conn_handler = ""
    
    def connect(self):
        """
        Connects with PostgreSQL database with configuration parameters.
    
        Returns
        -------
        conn : TYPE
            DESCRIPTION.
    
        """
        # Read config connection parameters.
        params = self.db_object
        # Connect to the PostgreSQL server.
        print("Connecting to PostgreSQL server")
        conn = psycopg2.connect(**params)
        
        # Return the connection Handler.
        self.conn_handler = conn
