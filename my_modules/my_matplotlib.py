# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 07:24:23 2022

@author: alber
"""

import pandas as pd
import matplotlib.pyplot as plt

from PIL import Image
import urllib
import os

def generate_fig(fig_width=4, fig_height=3, dpi=200):
    # FIGURE creation.
    # Size in pixels of the figure.
    # Width = width x dpi. Height = height x dpi.
    fig = plt.figure(figsize=(fig_width, fig_height), dpi=dpi)
    
    return fig

def generate_axes(ncols, nrows):
    # AXES.
    # Define the Axes for the Subplot.
    ax = plt.subplot()
    # xlim - Columns.
    ax.set_xlim(0, ncols+1)
    # ylim - Rows.
    ax.set_ylim(0, nrows+1)
    
    return ax

def generate_table_content(ax, df, positions, cols_ha_ori, cols_va_ori,
                           cols_weight, cols_color, spec_limits, margin_column_titles=.25):
    # Derive nrows and col_names from df.
    col_names = df.columns
    nrows = df.shape[0]
    
    # WRITE CONTENT, looping through the DataFrame.
    # Loop through the Rows.
    for i in range(nrows):
        # Loop through the Columns.
        for j, column in enumerate(col_names):
            # Define Initial Color.
            color_to_set = cols_color[j]
            # Define Initial Weight.
            weight_to_set = cols_weight[j]
            # Spec Limits: Check if the Column is within the Color Limits.
            if column in spec_limits:
                # Get Current Value.
                current_value = df[column].iloc[i]
                # Get Limit Value.
                limit_value = spec_limits[column][0]
                # Get Color.
                color_value = spec_limits[column][1]
                # Get Weight.
                weight_value = spec_limits[column][2]
                # Get Operator.
                operator_value = spec_limits[column][3]
                # Check if Value checks the limit.
                if "<" in operator_value:
                    if "=" in operator_value:
                        if current_value <= limit_value:
                            # Modify then the Color.
                            color_to_set = color_value
                            # Modify then the Weight.
                            weight_to_set = weight_value
                    else:
                        if current_value < limit_value:
                            # Modify then the Color.
                            color_to_set = color_value
                            # Modify then the Weight.
                            weight_to_set = weight_value
                elif ">" in operator_value:
                    if "=" in operator_value:
                        if current_value >= limit_value:
                            # Modify then the Color.
                            color_to_set = color_value
                            # Modify then the Weight.
                            weight_to_set = weight_value
                    else:
                        if current_value > limit_value:
                            # Modify then the Color.
                            color_to_set = color_value
                            # Modify then the Weight.
                            weight_to_set = weight_value
            # For a NORMALIZED version of annotate add the xycoords parameter.
            # xycoords='axes fraction'.
            # Annotate to write the content.
            ax.annotate(
                xy=(positions[j], i + .75),
                text=f"{df[column].iloc[i]}",
                ha=cols_ha_ori[j],
                va=cols_va_ori[j],
                weight=weight_to_set,
                color=color_to_set
                )
    
    # COLUMN NAMES.
    for index, c in enumerate(col_names):
        ax.annotate(
                xy=(positions[index], nrows + margin_column_titles),
                text=col_names[index],
                ha=cols_ha_ori[index],
                va=cols_va_ori[index],
                weight="bold"
            )
        
def generate_table_dividing_lines(ax, nrows):
    # BOTTOM LINE.
    ax.plot([ax.get_xlim()[0],
             ax.get_xlim()[1]],
            [nrows, nrows],
            lw=1.5,
            color='black',
            marker='',
            zorder=4)
    # TOP LINE.
    ax.plot([ax.get_xlim()[0],
             ax.get_xlim()[1]],
            [0, 0],
            lw=1.5,
            color='black',
            marker='',
            zorder=4)
    # INTERMEDIATE LINES.
    # Loop through all the Rows.
    for x in range(1, nrows):
        ax.plot([ax.get_xlim()[0],
                 ax.get_xlim()[1]],
                [x, x],
                lw=1.15,
                color='gray',
                marker='',
                zorder=3,
                ls=':')
        
def generate_table_fill_between_lines(ax, nrows):
    # FILL BETWEEN LINES.
    ax.fill_between(
            x=[0, 3.5],
            y1=nrows,
            y2=0,
            color='lightgrey',
            alpha=0.5,
            ec='None'
        )
    
def generate_table_set_title_save_fig(fig, fig_pathfile, ax,
                                      title_fig, nrows, dpi=200):
    # Turn the x and y axis off.
    ax.set_axis_off()
    # Set Title of the Figure as text.
    fig.text(
        x=0.15, y=.91,
        s=title_fig,
        ha='left',
        va='bottom',
        weight='bold',
        size=12
    )
    # SAVE FIGURE.
    plt.savefig(
        fig_pathfile,
        dpi=dpi,
        transparent=False,
        # bbox_inches fix table without margins.
        bbox_inches='tight'
    )
        
    