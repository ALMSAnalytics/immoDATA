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

from datetime import timedelta, datetime

class ResultsPage():
    """
        Here page action of the Results page.
    """
    
    def __init__(self, website):
        # Get the Text page to further analyze with BeautifulSoup.
        text = requests.get(website).text
        # Parse with BeautifulSoup the text.
        self.doc = BeautifulSoup(text, "html.parser")
        # Titles list.
        self.titles = []
        # Links list.
        self.links = []
        # N_Rooms list.
        self.n_rooms = []
        # Cities list.
        self.cities = []
        # Areas list.
        self.areas = []
        # Streets list.
        self.streets = []
        # Start_dates list.
        self.start_dates = []
        # End_dates list.
        self.end_dates = []
        # Prices list.
        self.prices = []
        # Sizes list.
        self.sizes = []
        # Authors list.
        self.authors = []
        # Online times list.
        self.online_times = []
        # Publication dates list.
        self.publication_dates = []
        # Data.
        self.data = pd.DataFrame(columns=["title", "link", 
                                     "n_room", "city", "area", "street", 
                                     "start_date", "end_date", "price", "size",
                                     "author", "online_time", "publication_date"])
        
    def get_raw_rows(self):
        """
        Get the raw rows from the BeautifulSoup doc for further analyze.

        Returns
        -------
        rows_raw : TYPE
            DESCRIPTION.

        """
        # Get the classes row noprint and translate into a DataFrame.
        rows_raw = self.doc.find_all("div", 
                                     {"class": ["row noprint", "row noprint middle", "row noprint bottom"]})
        
        return rows_raw
    
    def get_results_data(self, rows_raw):
        """
        Get the full results data from the Results Page.

        Parameters
        ----------
        rows_raw : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        for row in rows_raw:
            # Get the Price and Size.
            self.get_price_size(row)
            # Get the Start and End Date.
            self.get_start_end_date(row)
            # Get the Title and Link.
            self.get_title_link(row)
            # Get the Author and Online Time.
            self.get_author_online_time(row)
            # Get the N Rows, City, Area and Street.
            self.get_n_rooms_city_area_street(row)
            
        # Adds to the full DataFrame.
        self.data["title"] = self.titles
        self.data["link"] = self.links
        self.data["n_room"] = self.n_rooms
        self.data["city"] = self.cities
        self.data["area"] = self.areas
        self.data["street"] = self.streets
        self.data["start_date"] = self.start_dates
        self.data["end_date"] = self.end_dates
        self.data["price"] = self.prices
        self.data["size"] = self.sizes
        self.data["author"] = self.authors
        self.data["online_time"] = self.online_times
        self.data["publication_date"] = self.publication_dates
        
    def get_price_size(self, row):
        """
        Get the price and size of the given row.

        Parameters
        ----------
        row : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        # Search for Price, size.
        price_size_col = row.find_all("div", {"class": "col-xs-3"})
        # Get the Price.
        if len(price_size_col) > 1:
            price = price_size_col[0].get_text(strip=True).replace(" ", "")
            self.prices.append(price)
            # Get the Size.
            size = price_size_col[1].get_text(strip=True).replace(" ", "")
            self.sizes.append(size)
            
    def get_start_end_date(self, row):
        """
        Get the start and end date of the given row.

        Parameters
        ----------
        row : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        # Search for Start Date, End Date.
        start_end_date_col = row.find_all("div", {"class": "col-xs-5 text-center"})
        # Get Start and End Date.
        if len(start_end_date_col) > 0:
            split_dates = start_end_date_col[0].get_text(strip=True).replace(" ", "").split("-")
            # Depending if we have End Date or not.
            if len(split_dates) > 1:
                start_date = split_dates[0].strip()
                end_date = split_dates[1]
            else:
                start_date = split_dates[0].replace("ab", "").strip()
                end_date = None
            # Append Start and End Dates.
            self.start_dates.append(start_date)
            self.end_dates.append(end_date)
            
    def get_title_link(self, row):
        """
        Get the Title and Link of the given Row.

        Parameters
        ----------
        row : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        # Search for Title Link.
        title_link_col = row.find_all("h3", {"class": "truncate_title noprint"})
        if len(title_link_col) > 0:
            # Get Title.
            title = title_link_col[0].get_text(strip=True)
            self.titles.append(title)
            # Get Link.
            link = title_link_col[0].find("a").get("href")
            self.links.append(link)
            
    def get_author_online_time(self, row):
        """
        Get the Author and Online Time of the given row.

        Parameters
        ----------
        row : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        # Search for Author and Online Time.
        author_online_col = row.find_all("div", {"class": "col-sm-12 flex_space_between"})
        if len(author_online_col) > 1:
            # Get Author.
            author = author_online_col[1].get_text(strip=True).split("Online: ")[0]
            self.authors.append(author)
            # Get Online Time.
            online_time = author_online_col[1].get_text(strip=True).split("Online: ")[-1]
            # Convert Online Time to TimeDelta depending on which type we have.
            if ("Sekunden" in online_time) or ("Sekunde" in online_time):
                online_time = timedelta(seconds=int(online_time.split(" ")[0]))
            elif ("Minuten" in online_time) or ("Minute" in online_time):
                online_time = timedelta(minutes=int(online_time.split(" ")[0]))
            elif ("Stunden" in online_time) or ("Stunde" in online_time):
                online_time = timedelta(hours=int(online_time.split(" ")[0]))
            elif ("Tagen" in online_time) or ("Tag" in online_time):
                online_time = timedelta(days=int(online_time.split(" ")[0]))
            else:
                # Case we have directly the date, calculate the Online Time.
                online_time_formatted = datetime.now() - datetime.strptime(online_time, "%d.%m.%Y")
                self.online_times.append(online_time_formatted)
                # Format the publication date.
                publication_date = datetime.strftime(datetime.strptime(online_time, 
                                                                       "%d.%m.%Y"), "%Y-%m-%d %H:%M:%S")
                # Adds the publication date.
                self.publication_dates.append(publication_date)
                # Go out of the function.
                return
            
            # Append to Online Times.
            self.online_times.append(online_time)
            
            # Calculate approximate publication_date.
            # NOW - Online Time.
            publication_date = datetime.now() - online_time
            # Format the Publication Date.
            publication_date = datetime.strftime(publication_date, "%Y-%m-%d %H:%M:%S")
            # Add to the list.
            self.publication_dates.append(publication_date)
            
    def get_n_rooms_city_area_street(self, row):
        """
        Get N_Rooms, City, Area and Street of the given row.

        Parameters
        ----------
        row : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        # Wait until the Cookies object is visible. 10 seconds is the timeout.
        # WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME,
        #                                                                        "col-xs-11")))
        # Search for the # of Rooms, City, Area and Street.
        n_rooms_city_area_street_col = row.find_all("div", {"class": "col-xs-11"})
        if len(n_rooms_city_area_street_col) > 0:
            # Get the Full Text
            full_text = n_rooms_city_area_street_col[0].span.get_text(strip=True).strip()
            # Split full text into the 3 data points.
            full_text_split = full_text.split("|")
            # Get n_rooms, city, area and street.
            n_room = full_text_split[0].strip()
            self.n_rooms.append(n_room)
            city = full_text_split[1].strip().replace(" ", "").split("\n\n")[0]
            self.cities.append(city)
            area = full_text_split[1].strip().replace(" ", "").split("\n\n")[1]
            self.areas.append(area)
            street = full_text_split[2].strip()
            self.streets.append(street)
            
    def go_to_next_page(self, driver):
        """
        Go to the Next Page and Return the URL for the new Page.

        Parameters
        ----------
        driver : TYPE
            DESCRIPTION.

        Returns
        -------
        current_url : TYPE
            DESCRIPTION.

        """
        
        # Search for the Next Page element.
        page_next_element = driver.find_elements(by=By.XPATH, 
                                                value="//*[@id='assets_list_pagination']/ul/li")[-1]
        page_next_element.click()
        
        # Get New Results Page.
        current_url = driver.current_url
        
        return current_url
        
            
        
    
    
        
        
    