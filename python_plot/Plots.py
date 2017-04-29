'''-----------------------------------------------------------------------------
Antonio Bujanda
CS 4354 - Concepts of Database Systems
April 10, 2017

This script generates a bar chart that compares the number of crimes between 
months in years 2014-2015 for Montgomery County. It also generates the pie
chart detailing the percentage crime distribution among different districts
for 2014-2015.

All data originates from a database. 
-----------------------------------------------------------------------------'''
import pyodbc
import matplotlib.pyplot as plt
import numpy as np

server = 'davidtho.database.windows.net'
database = 'davidtho_db'
username = 'davidtho'
password = 'M@pl3l3af'
driver= '{ODBC Driver 13 for SQL Server}'
cnxn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)

def sql_select(query):
    cursor = cnxn.cursor()
    cursor.execute(query)
    columns = cursor.fetchall()
    return columns

################################################################################
#Plot for Crime Comparison: 2014 & 2015
crimeData2014 = []
crimeData2015 = []
months = ['01','02','03','04','05','06','07','08','09','10','11','12']

for month in months:
    select_str = "SELECT COUNT([Dispatch Date   Time]) AS myCount\
            FROM dbo.crime\
            WHERE [Dispatch Date   Time] BETWEEN" + " " + "'" + month + "/01/2014' AND" + " "+ "'" + month +"/31/2014'"
    data = sql_select(select_str)
    crimeData2014.append(data[0][0])
    
    select_str = "SELECT COUNT([Dispatch Date   Time]) AS myCount\
            FROM dbo.crime\
            WHERE [Dispatch Date   Time] BETWEEN" + " " + "'" + month + "/01/2015' AND" + " "+ "'" + month +"/31/2015'"
    data = sql_select(select_str)
    crimeData2015.append(data[0][0])
    

months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

CrimeComparison = plt.figure(1)
bar_width = 0.35
plt.title("Crime Comparison: 2014 & 2015")
plt.xlabel("Months")
plt.ylabel("# of Crimes")
x_pos = np.arange(len(crimeData2014))

bar2014 = plt.bar(x_pos,crimeData2014,bar_width,color='b',alpha=0.8,label='2014')
bar2015 = plt.bar(x_pos+bar_width,crimeData2015,bar_width,color='r',alpha=0.8,label='2015')

plt.xticks(x_pos+bar_width,months)
plt.legend()
plt.ylim(0,15000)
plt.grid(True)
CrimeComparison.show()
plt.savefig('CrimeComparison.png')
################################################################################
#pie chart for District Count Table
select_str = "Select * FROM [dbo].[District Count Table]"
districts = []
districtData = []
view = sql_select(select_str)

for row in view:
    districts.append(row[0])
    districtData.append(row[1])

crimeTotal = sum(districtData)

#obtaining the percentages
for index,crimenum in enumerate(districtData):
    districtData[index] = float(float(crimenum) / float(crimeTotal))*100
 
# Data to plot
DistrictDataPie = plt.figure(2)
labels = districts
sizes = districtData
colors = ['red', 'white', 'skyblue', 'blue','yellow','cyan','lightcoral','darkgreen'] 
explode = (0, 0, 0, 0,0,0.1,0,0)  # explode 1st slice

# Plot
#patches = plt.pie(sizes, colors=colors,
#        autopct='%1.1f%%', shadow=True, startangle=180)

patches, texts = plt.pie(sizes,explode=explode, colors=colors,
        shadow=True, startangle=180)
plt.pie(sizes,explode=explode,colors=colors,autopct='%1.1f%%',startangle=180)

plt.legend(patches,labels,loc="best")
plt.axis('equal')
plt.tight_layout()
plt.title("Crime Percentage Distribution Across Districts: 2014 & 2015")
DistrictDataPie.show()
plt.savefig('CrimePercentages.png')
