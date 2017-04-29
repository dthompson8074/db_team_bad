#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import time
import math
import pyodbc
import gmplot
from scipy.misc import imread

img = imread("moco_map2.png")
server = 'davidtho.database.windows.net'
database = 'davidtho_db'
username = 'davidtho'
password = 'M@pl3l3af'
driver= '{ODBC Driver 13 for SQL Server}'
cnxn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)

#function definition

# Distance function
def distance(xi,xii,yi,yii):
    sq1 = (xi-xii)*(xi-xii)
    sq2 = (yi-yii)*(yi-yii)
    return math.sqrt(sq1 + sq2)

def sse(xi,xii,yi,yii):
    sq1 = (xi-xii)*(xi-xii)
    sq2 = (yi-yii)*(yi-yii)
    return sq1+sq2
#sql
def sql_select(query):
    cursor = cnxn.cursor()
    cursor.execute(query)
    columns = cursor.fetchall()
    return columns

select_str = "SELECT Latitude,Longitude FROM crime WHERE (Longitude Between -77.6 AND -76.81) AND (Latitude between 38.885 AND 39.8 )"

#k-mean parameters
dim = 2

k = 10
kxdim = 4
precision = .001

count=0
close_k = 0

police_sse = 0
k_sse = 0

cluster_size = np.random.rand(k)
cluster_sum_z = np.random.rand(k)
cluster_sum_w = np.random.rand(k)

center_z = 0
center_w = 0

color_assign = []

#clusters
police_long = [-77.093449 , -77.048494,-76.943832,-76.990898,-77.064992,-77.148360,-77.132083,-77.234093,-77.262873, -77.236469]
police_lat =  [38.983552, 39.058405,39.078524,39.045244,39.149304,39.083774,39.098038,39.149697,39.184389,39.113024]
k_long = [-77.093449 , -77.048494,-76.943832,-76.990898,-77.064992,-77.148360,-77.132083,-77.234093,-77.262873, -77.236469]
k_lat = [38.983552, 39.058405,39.078524,39.045244,39.149304,39.083774,39.098038,39.149697,39.184389,39.113024]

colors_cluster = ['red','pink','black','blue','cyan','orange','purple','green','magenta','teal']

#data
columns = sql_select(select_str)

i_long = []
i_lat = []
for row in columns:
    i_long.append(row[1])
    i_lat.append(row[0])

for i in range(len(i_long)):
    color_assign.append('grey')

print("incident count:")
print(len(columns))



#google maps
gmap = gmplot.GoogleMapPlotter(38.983552, -77.093449, 11)

#gmap.plot(k_lat, k_long, 'cornflowerblue', edge_width=10)
#gmap.scatter(k_lat, k_long,'k', size=100, marker=False)
gmap.scatter(k_lat, k_long, size=200, marker=True)
#gmap.scatter(k_lat, k_long, 'k', marker=True)
gmap.heatmap(i_lat, i_long,1,20,None,.8,True)

gmap.draw("crime_heatmap.html")


