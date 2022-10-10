# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 08:00:20 2022

@author: alber
"""
from immoDATA.immoDB import immoDB
import pandas as pd
import numpy as np

import my_modules.my_matplotlib as my_mpl

import os

publication_date = "2022-10-08"

main_path = r"C:\immoDATA_dB\DAILY"

# Connect with immoDB database.
immoDB_obj = immoDB()
immoDB_obj.connect()

# Get the Data from the publication date.
df_houses = immoDB_obj.get_data_w_publication_date(publication_date)

# INPUTS for the table.
positions = [0.25, 1.0, 2.0, 3.25, 3.75, 4.25, 4.75, 5.25, 5.75, 6.25, 6.75]
cols_ha_ori = ["left", "left", "left", "center", "center", "center", "center", "center",
               "center", "center", "left"]
cols_va_ori = ["center", "center", "center", "center", "center", "center", "center", "center",
               "center", "center", "center"]
cols_weight = ["normal", "bold", "normal", "normal", "normal", "bold", "normal", "normal",
               "normal", "normal", "normal"]
cols_color = ["black", "black", "black", "black", "black", "black", "black", "black",
              "black", "black", "blue"]
fig_height = 10
fig_width = 30
margin_column_titles = .25
# Get nrows and ncols.
nrows = df_houses.shape[0]
ncols = df_houses.shape[1]
# Specs Limits.
# Key: Column.
# 01. Value: Limit Value.
# 02. Color: Color Value.
# 03. Operator: <, <=, >, >=.
spec_limits = {"price": [1700, "green", "bold", "<="], 
                "n_room": [3, "green", "bold", ">="],
                "size": [70, "green", "bold", ">="]}

# Generate filepath.
fig_pathfile = os.path.join(main_path, publication_date.replace("-", "_") + "_houses.pdf")
# Title of the Figure.
fig_title = publication_date

# 01. Generate FIG.
fig = my_mpl.generate_fig(fig_width=fig_width, fig_height=fig_height, dpi=300)
# 02. Generate AX.
ax = my_mpl.generate_axes(ncols, nrows)
# 03. Generate Table Content.
my_mpl.generate_table_content(ax,
                              df_houses,
                              positions,
                              cols_ha_ori,
                              cols_va_ori,
                              cols_weight,
                              cols_color,
                              spec_limits,
                              margin_column_titles)
# 04. Add Dividing Lines to the Table.
my_mpl.generate_table_dividing_lines(ax, nrows)
# 05. Fill Between Lines.
my_mpl.generate_table_fill_between_lines(ax, nrows)
# 06. Set Title and Save Fig.
my_mpl.generate_table_set_title_save_fig(fig, fig_pathfile, ax,
                                         fig_title, nrows, dpi=200)


# Disconnect from immoDB database.
immoDB_obj.disconnect()