#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import time
import math
import pyodbc
import gmplot
from scipy.misc import imread


server = 'davidtho.database.windows.net'
database = 'davidtho_db'
username = 'davidtho'
password = 'M@pl3l3af'
driver= '{ODBC Driver 13 for SQL Server}'
cnxn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)

#function definition

#sql
def sql_select(query):
    cursor = cnxn.cursor()
    cursor.execute(query)
    columns = cursor.fetchall()
    return columns

select_str = "SELECT Latitude,Longitude FROM crime WHERE (Longitude Between -77.6 AND -76.81) AND (Latitude between 38.885 AND 39.8 )AND Agency like '%MC%'"


#clusters
k_long = [-77.236469,-77.093449 ,-76.990898,-77.048494,-77.262873, -77.234093]
k_lat =[39.113024, 38.983552,39.045244,39.058405,39.184389,39.149697]

colors_cluster = ['red','pink','black','blue','cyan','orange','purple','green','magenta','teal']

#data
columns = sql_select(select_str)

i_long = []
i_lat = []
for row in columns:
    i_long.append(row[1])
    i_lat.append(row[0])





#google maps
gmap = gmplot.GoogleMapPlotter(38.983552, -77.093449, 11)

#gmap.plot(k_lat, k_long, 'cornflowerblue', edge_width=10)
#gmap.scatter(k_lat, k_long,'k', size=100, marker=False)
gmap.scatter(k_lat, k_long, size=200, marker=True)
#gmap.scatter(k_lat, k_long, 'k', marker=True)
gmap.heatmap(i_lat, i_long,1,20,None,.8,True)

gmap.draw("crime_heatmap.html")


