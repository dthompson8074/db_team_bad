#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import time
import math
import pyodbc
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

select_str = "SELECT Latitude,Longitude,[Police District Number] FROM crime WHERE (Longitude Between -77.6 AND -76.81) AND (Latitude between 38.885 AND 39.8 ) AND Agency like '%MC%'"

#k-mean parameters
dim = 2

k = 6
kxdim = 4
precision = .001

count=0
close_k = 0

police_sse = 0
k_sse = 0

cluster_size = []
cluster_sum_z = []
cluster_sum_w = []

center_z = 0
center_w = 0

color_assign = []
dict = {'1D':0,'2D':1,'3D':2,'4D':3,'5D':4,'6D':5,'TPPD':2}

police_assign=[]
cluster_assign =[]
#clusters
police_long = [-77.236469,-77.093449 ,-76.990898,-77.048494,-77.262873, -77.234093]

police_lat =  [39.113024, 38.983552,39.045244,39.058405,39.184389,39.149697]
k_long = [-77.236469,-77.093449 ,-76.990898,-77.048494,-77.262873, -77.234093]
k_lat =[39.113024, 38.983552,39.045244,39.058405,39.184389,39.149697]

colors_cluster = ['red','black','blue','orange','purple','green']

#data
columns = sql_select(select_str)

i_long = []
i_lat = []
for row in columns:
    i_long.append(row[1])
    i_lat.append(row[0])
    color_assign.append(colors_cluster[dict[row[2]]])
    cluster_assign.append(dict[row[2]])
    police_assign.append(dict[row[2]])

for i in range(len(k_long)):
    cluster_sum_z.append(0)
    cluster_sum_w.append(0)
    cluster_size.append(0)

print("incident count:")
print(len(columns))

#initialize plot
plt.ion()
plt.scatter(i_long, i_lat, c= color_assign,alpha=0.3,s = 5)
plt.title('Unassigned Incident Locations')
plt.imshow(img,extent = [-77.6,-76.81,38.885,39.385])
plt.waitforbuttonpress()
plt.title('Police Stations as Initial Cluster Centers')
plt.scatter(k_long,k_lat, c=colors_cluster, s=200)
plt.waitforbuttonpress()
plt.clf()


while(count < 30):
    flag = 1
    
    for i in range(len(i_long)):
        min_dist = 10000.0
        cur_dist = 0.0
        
        for j in range(len(k_long)):
            cur_dist = distance(i_long[i],k_long[j],i_lat[i],k_lat[j])
            if(cur_dist < min_dist):
                    min_dist = cur_dist
                    cluster_assign[i] = j
                    close_k = j
    
        cluster_size[close_k]+=1
        color_assign[i] = colors_cluster[close_k]
       

    plt.scatter(i_long, i_lat, c= color_assign,alpha=0.1,s=5)
    plt.scatter(k_long,k_lat, c='grey', s=200)
    plt.title('k - means clustering')
    plt.imshow(img,extent = [-77.6,-76.81,38.885,39.385])
    plt.draw()

    for i in range(len(i_long)):
            cluster_sum_z[int(cluster_assign[i])] += i_long[i]
            cluster_sum_w[int(cluster_assign[i])] += i_lat[i]


    for i in range(len(k_long)):
            prev_z = k_long[i]
            prev_w = k_lat[i]
            k_long[i] = cluster_sum_z[i]/cluster_size[i]
            k_lat[i] = cluster_sum_w[i]/cluster_size[i]
            prev_z = abs(prev_z - k_long[i])
            prev_w = abs(prev_w - k_lat[i])
            if (prev_z > precision or prev_w > precision):
                flag = 0

    #reset cluster
    for i in range(len(k_long)):
        cluster_sum_z[i] =0
        cluster_sum_w[i] =0
        cluster_size[i] = 0

    plt.pause(1)
    plt.clf()

    count+=1
    if (flag == 1):
        break

plt.scatter(i_long, i_lat, c= color_assign,alpha=0.1,s=5)
plt.scatter(k_long,k_lat,c= 'grey', s=200)
plt.scatter(police_long,police_lat, c= colors_cluster, s=200)
plt.title('Final Cluster Centers vs. Police Stations')
plt.imshow(img,extent = [-77.6,-76.81,38.885,39.385])
plt.draw()

for i in range(len(i_long)):
    police_sse += sse(i_long[i],police_long[int(police_assign[i])],i_lat[i],police_lat[int(police_assign[i])])
    k_sse += sse(i_long[i],k_long[int(cluster_assign[i])],i_lat[i],k_lat[int(cluster_assign[i])])

plt.waitforbuttonpress()
plt.clf

print('\nIterations: {}'.format(count))
print("Sum of Squares Error(degrees)")
print('Police Stations: {:8.6f}'.format(police_sse))
print('Final Custer Centers: {:8.6f}'.format(k_sse))
print('Percent decrease: {}%'.format(int(100*(1-(k_sse/police_sse)))))
