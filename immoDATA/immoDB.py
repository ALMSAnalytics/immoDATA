# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 10:29:21 2022

@author: alber
"""

# Import necessary modules.
from configparser import ConfigParser
import psycopg2
import pandas as pd

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
        
    def disconnect(self):
        """
        Disconnects of the PostgreSQL database.
    
        Returns
        -------
        conn : TYPE
            DESCRIPTION.
    
        """
        # Connect to the PostgreSQL server.
        print("Disconnecting of the PostgreSQL server")
        # Close the connection with the Database.
        self.conn_handler.close()
        
    def create_tables_immoDB(self):
        """
        Creates all the tables for the immoDB.
    
        Parameters
        ----------
        conn : TYPE
            DESCRIPTION.
    
        Returns
        -------
        int
            DESCRIPTION.
    
        """
        
        # Define the tables in a commands variable.
        commands = (
            """
            DROP TABLE IF EXISTS house CASCADE;
            DROP TABLE IF EXISTS city CASCADE;
            DROP TABLE IF EXISTS area CASCADE;
            DROP TABLE IF EXISTS type CASCADE;
            DROP TABLE IF EXISTS vendor CASCADE;
            DROP TABLE IF EXISTS heating CASCADE;
            DROP TABLE IF EXISTS house_raw CASCADE;
            """,
            """
            CREATE TABLE vendor (
                id SERIAL UNIQUE NOT NULL,
                name VARCHAR(20) UNIQUE NOT NULL
            )
            """,
            """
            CREATE TABLE city (
                id SERIAL UNIQUE NOT NULL,
                name VARCHAR(50) UNIQUE NOT NULL
            )
            """,
            """
            CREATE TABLE area (
                id SERIAL UNIQUE NOT NULL,
                name VARCHAR(150) UNIQUE NOT NULL
            )
            """,
            """
            CREATE TABLE type (
                id SERIAL UNIQUE NOT NULL,
                name VARCHAR(10) UNIQUE NOT NULL
            )
            """,
            """
            CREATE TABLE heating (
                id SERIAL UNIQUE NOT NULL,
                name VARCHAR(100) UNIQUE NOT NULL
            )
            """,
            """
            CREATE TABLE house (
                id SERIAL UNIQUE NOT NULL,
                title VARCHAR(300) UNIQUE NOT NULL,
                n_room NUMERIC NOT NULL,
                address VARCHAR(50),
                start_date DATE NOT NULL,
                price NUMERIC NOT NULL,
                rent_wo_costs NUMERIC,
                costs NUMERIC,
                deposit NUMERIC,
                size NUMERIC NOT NULL,
                author VARCHAR(50),
                publication_date DATE NOT NULL,
                n_floor NUMERIC,
                floor_type VARCHAR(100),
                kitchen BOOLEAN,
                furnished BOOLEAN,
                bathtub BOOLEAN,
                shower BOOLEAN,
                guest_wc BOOLEAN,
                washing_machine	BOOLEAN,
                dishwasher BOOLEAN,
                garden BOOLEAN,
                pets BOOLEAN,
                balcony	BOOLEAN,
                terrace	BOOLEAN,
                garage BOOLEAN,
                elevator BOOLEAN,
                id_heating INTEGER NOT NULL REFERENCES heating(id) ON DELETE CASCADE,
                id_type INTEGER NOT NULL REFERENCES type(id) ON DELETE CASCADE,
                id_city INTEGER NOT NULL REFERENCES city(id) ON DELETE CASCADE,
                id_area INTEGER NOT NULL REFERENCES area(id) ON DELETE CASCADE,
                id_vendor INTEGER NOT NULL REFERENCES vendor(id) ON DELETE CASCADE,
                UNIQUE (title, author)
            )
            """,
            """
            CREATE TABLE house_raw (
                id SERIAL UNIQUE NOT NULL,
                title VARCHAR(300) UNIQUE NOT NULL,
                n_room NUMERIC NOT NULL,
                address VARCHAR(50),
                start_date DATE NOT NULL,
                price NUMERIC NOT NULL,
                rent_wo_costs NUMERIC,
                costs NUMERIC,
                deposit NUMERIC,
                size NUMERIC NOT NULL,
                author VARCHAR(50),
                publication_date DATE NOT NULL,
                n_floor NUMERIC,
                floor_type VARCHAR(100),
                kitchen BOOLEAN,
                bath_type VARCHAR(50),
                furnitures VARCHAR(50),
                heating VARCHAR(100),
                extra_features VARCHAR(300),
                type VARCHAR(10) NOT NULL,
                city VARCHAR(50) NOT NULL,
                area VARCHAR(150) NOT NULL,
                vendor VARCHAR(20) NOT NULL,
                UNIQUE (title, author)
            )
            """
            )
        
        cursor = self.conn_handler.cursor()
        try:
            for command in commands:
                # Execute the command.
                cursor.execute(command)
            # Close the cursor.
            cursor.close()
            # Commit the changes.
            self.conn_handler.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            # Rollback to previous status of the connection.
            self.conn_handler.rollback()
            # Close cursor.
            cursor.close()
            return 1
        # Print message insertion was done.
        print("create_tables_immoDB() DONE")
        
    def exists_table(self, table_name):
        try:
            # Creates cursor.
            cursor = self.conn_handler.cursor()
            sql = f"""
                SELECT EXISTS (
                    SELECT 1
                    FROM pg_tables
                    WHERE tablename='{table_name}'
                )
                """
            # Read SQL query in Pandas.
            is_table = pd.read_sql_query(sql, self.conn_handler)["exists"].iloc[0]
            # Executes SQL statement => This with execute/fetchall from psycopg2.
            #cursor.execute(sql)
            #data = cursor.fetchall()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            self.conn_handler.rollback()
            cursor.close()
            return 1
        print("exists_table() DONE from TABLE: " + table_name)
        
        return is_table
        
    def copy_csv_to_db(self, table_name, csv_file, columns):
        # Get the columns string variable.
        if len(columns) > 1:
            columns_string = str(tuple(columns.to_list())).replace("'", "")
        else:
            columns_string = str(columns.to_list()).replace("'", "").replace("[", "(").replace("]", ")")
        try:
            # Creates cursor.
            cursor = self.conn_handler.cursor()
            sql = f"""
                COPY {table_name}{columns_string}
                FROM '{csv_file}'
                DELIMITER ',' CSV HEADER;
                """
            # Execute the command.
            cursor.execute(sql)
            # Commit the changes.
            self.conn_handler.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            self.conn_handler.rollback()
            cursor.close()
            return 1
        print("copy_csv_to_db() DONE for TABLE: " + table_name)
        
    def csv_export_and_copy_to_db(self, csv_file, df, db_table_name):
        # Export to CSV.
        df.to_csv(csv_file, index=False)
        # Copy CSV to DB.
        self.copy_csv_to_db(db_table_name, 
                                  csv_file, 
                                  df.columns)
        
    def is_city_exists(self, city):
        # Executes SQL statement.
        try:
            # Creates cursor.
            cursor = self.conn_handler.cursor()
            # Generates SQL statement.
            sql = f"SELECT * FROM city WHERE unaccent(name)='{city}';"
            # Read SQL query in Pandas.
            data = pd.read_sql_query(sql, self.conn_handler)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            self.conn_handler.rollback()
            cursor.close()
            return 1
        
        # Checks if we have results.
        if len(data) == 0:
            city_exists = False
        else:
            city_exists = True
        
        return city_exists
    
    def is_type_exists(self, type_name):
        # Executes SQL statement.
        try:
            # Creates cursor.
            cursor = self.conn_handler.cursor()
            # Generates SQL statement.
            sql = f"SELECT * FROM type WHERE unaccent(name)='{type_name}';"
            # Read SQL query in Pandas.
            data = pd.read_sql_query(sql, self.conn_handler)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            self.conn_handler.rollback()
            cursor.close()
            return 1
        
        # Checks if we have results.
        if len(data) == 0:
            type_exists = False
        else:
            type_exists = True
        
        return type_exists
    
    def is_vendor_exists(self, vendor):
        # Executes SQL statement.
        try:
            # Creates cursor.
            cursor = self.conn_handler.cursor()
            # Generates SQL statement.
            sql = f"SELECT * FROM vendor WHERE unaccent(name)='{vendor}';"
            # Read SQL query in Pandas.
            data = pd.read_sql_query(sql, self.conn_handler)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            self.conn_handler.rollback()
            cursor.close()
            return 1
        
        # Checks if we have results.
        if len(data) == 0:
            vendor_exists = False
        else:
            vendor_exists = True
        
        return vendor_exists
    
    def is_area_exists(self, area):
        # Executes SQL statement.
        try:
            # Creates cursor.
            cursor = self.conn_handler.cursor()
            # Generates SQL statement.
            sql = f"SELECT * FROM area WHERE unaccent(name)='{area}';"
            # Read SQL query in Pandas.
            data = pd.read_sql_query(sql, self.conn_handler)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            self.conn_handler.rollback()
            cursor.close()
            return 1
        
        # Checks if we have results.
        if len(data) == 0:
            area_exists = False
        else:
            area_exists = True
        
        return area_exists
    
    def is_heating_exists(self, heating):
        # Executes SQL statement.
        try:
            # Creates cursor.
            cursor = self.conn_handler.cursor()
            # Generates SQL statement.
            sql = f"SELECT * FROM heating WHERE unaccent(name)='{heating}';"
            # Read SQL query in Pandas.
            data = pd.read_sql_query(sql, self.conn_handler)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            self.conn_handler.rollback()
            cursor.close()
            return 1
        
        # Checks if we have results.
        if len(data) == 0:
            heating_exists = False
        else:
            heating_exists = True
        
        return heating_exists
    
    def normalize_house(self, city_name):
        # Generates SQL statement.
        sql = f"""
            INSERT INTO house(title, 
                              n_room, 
                              address, 
                              start_date, 
                              price, 
                              rent_wo_costs, 
                              costs,
                              deposit, 
                              size, 
                              author, 
                              publication_date,
                              n_floor, 
                              floor_type, 
                              kitchen,
                              furnished,
                              bathtub,
                              shower,
                              guest_wc,
                              washing_machine,
                              dishwasher,
                              garden,
                              pets,
                              balcony,
                              terrace,
                              garage,
                              elevator,
                              id_heating,
                              id_type,
                              id_city,
                              id_area,
                              id_vendor) 
            SELECT title, n_room, address, start_date, price, rent_wo_costs,
                costs, deposit, size, author, publication_date, n_floor, floor_type,
                kitchen,
                CASE WHEN house_raw.furnitures LIKE '%möbliert%'
                THEN CAST('t' AS BOOLEAN)
                ELSE CAST('f' AS BOOLEAN)
                END AS furnished,
                CASE WHEN house_raw.bath_type LIKE '%Badewanne%'
                THEN CAST('t' AS BOOLEAN)
                ELSE CAST('f' AS BOOLEAN)
                END AS bathtub,
                CASE WHEN house_raw.bath_type LIKE '%Dusche%'
                THEN CAST('t' AS BOOLEAN)
                ELSE CAST('f' AS BOOLEAN)
                END AS shower,
                CASE WHEN house_raw.bath_type LIKE '%Gäste WC%'
                THEN CAST('t' AS BOOLEAN)
                ELSE CAST('f' AS BOOLEAN)
                END AS guest_wc,
                CASE WHEN house_raw.extra_features LIKE '%Waschmaschine%'
                THEN CAST('t' AS BOOLEAN)
                ELSE CAST('f' AS BOOLEAN)
                END AS washing_machine,
                CASE WHEN house_raw.extra_features LIKE '%Spülmaschine%'
                THEN CAST('t' AS BOOLEAN)
                ELSE CAST('f' AS BOOLEAN)
                END AS dishwasher,
                CASE WHEN house_raw.extra_features LIKE '%Garten%'
                THEN CAST('t' AS BOOLEAN)
                ELSE CAST('f' AS BOOLEAN)
                END AS garden,
                CASE WHEN house_raw.extra_features LIKE '%Haustiere erlaubt%'
                THEN CAST('t' AS BOOLEAN)
                ELSE CAST('f' AS BOOLEAN)
                END AS pets,
                CASE WHEN house_raw.extra_features LIKE '%Balkon%'
                THEN CAST('t' AS BOOLEAN)
                ELSE CAST('f' AS BOOLEAN)
                END AS balcony,
                CASE WHEN house_raw.extra_features LIKE '%Terrasse%'
                THEN CAST('t' AS BOOLEAN)
                ELSE CAST('f' AS BOOLEAN)
                END AS terrace,
                CASE WHEN house_raw.extra_features LIKE '%Keller%'
                THEN CAST('t' AS BOOLEAN)
                ELSE CAST('f' AS BOOLEAN)
                END AS garage,
                CASE WHEN house_raw.extra_features LIKE '%Aufzug%'
                THEN CAST('t' AS BOOLEAN)
                ELSE CAST('f' AS BOOLEAN)
                END AS elevator,
                heating.id AS id_heating, type.id AS id_type, city.id AS id_city, 
                area.id AS id_area, vendor.id AS id_vendor
            FROM house_raw 
            JOIN vendor ON vendor.name=house_raw.vendor
            JOIN city ON city.name=house_raw.city
            JOIN type ON type.name=house_raw.type
            JOIN area ON area.name=house_raw.area
            JOIN heating ON heating.name=house_raw.heating
            WHERE unaccent(house_raw.city)='{city_name}';
            """
                
        # Executes SQL statement.
        try:
            # Creates new Cursor.
            cursor = self.conn_handler.cursor()
            # Executes INSERT statement.
            cursor.execute(sql)
            # Commit the changes.
            self.conn_handler.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            self.conn_handler.rollback()
            cursor.close()
            return 1
        # Print message insertion was done.
        print("normalize_house() DONE")
        
    def truncate_raw_tables(self):
    
        # Generates SQL statement.
        sql = r"""
            TRUNCATE TABLE house_raw;
            """
                
        # Executes SQL statement.
        try:
            # Creates new Cursor.
            cursor = self.conn_handler.cursor()
            # Executes INSERT statement.
            cursor.execute(sql)
            # Commit the changes.
            self.conn_handler.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            self.conn_handler.rollback()
            cursor.close()
            return 1
        # Print message insertion was done.
        print("truncate_raw_tables() DONE")
