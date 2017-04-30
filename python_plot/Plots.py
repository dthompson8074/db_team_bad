'''-----------------------------------------------------------------------------
Antonio Bujanda
CS 4354 - Concepts of Database Systems
April 10, 2017

This script generates a bar chart that compares the number of crimes between 
months in years 2014-2015 for Montgomery County. It also generates the pie
chart detailing the percentage crime distribution among different districts
for 2014-2015 as well as a bar chart for common offenses. 

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
month = 1

while month <= 12:
    select_str = "SELECT COUNT([Dispatch Date/Time]) AS monthlyCount\
            FROM dbo.crime\
            WHERE Month([Dispatch Date/Time]) = " + str(month) + " " + "AND Year([Dispatch Date/Time]) = 2014;"
    data = sql_select(select_str)
    crimeData2014.append(data[0][0])
    
    select_str = "SELECT COUNT([Dispatch Date/Time]) AS monthlyCount\
            FROM dbo.crime\
            WHERE Month([Dispatch Date/Time]) = " + str(month) + " " + "AND Year([Dispatch Date/Time]) = 2015;"
    data = sql_select(select_str)
    crimeData2015.append(data[0][0])
    
    month+=1
    
months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

CrimeComparison = plt.figure(1)
bar_width = 0.35
plt.title("Crime Comparison: 2014 & 2015")
plt.xlabel("Months")
plt.ylabel("# of Crimes")
x_pos = np.arange(len(crimeData2014))

bar2014 = plt.bar(x_pos,crimeData2014,bar_width,color='b',alpha=0.8,label='2014')
bar2015 = plt.bar(x_pos+bar_width,crimeData2015,bar_width,color='r',alpha=0.8,label='2015')

if max(crimeData2014) > max(crimeData2015):
    limit = max(crimeData2014) + 100
else:
     limit = max(crimeData2015) + 100   

plt.xticks(x_pos+float(bar_width/2),months)
plt.legend()
plt.ylim(0,limit)
plt.grid(True)
mngr = plt.get_current_fig_manager()
mngr.window.setGeometry(0,0,450,600)
CrimeComparison.show()
#plt.savefig('CrimeComparison.png')

###############################################################################

#Pie Chart for District Percentage Table JOINED with Police Districts

select_str = "Select * FROM [dbo].[District Percentage Table] DBT\
              LEFT OUTER JOIN [dbo].[Police Districts] PD\
              ON DBT.[Police District Number] = PD.[Police District Number]"

districts = []
districtPercentage = []
view = sql_select(select_str)

for row in view:
    districts.append(row[0]+"-"+row[3])
    districtPercentage.append(row[1])

# Data to plot
DistrictDataPie = plt.figure(2)
labels = districts
sizes = districtPercentage
colors = ['blue','yellow', 'cyan','lightcoral','green','red'] 
explode = (0, 0, 0.1, 0,0,0)  # explode 3rd slice

# Plot

patches, texts = plt.pie(sizes,explode=explode, colors=colors,
        shadow=True, startangle=225)
plt.pie(sizes,explode=explode,colors=colors,autopct='%1.1f%%',startangle=225)

plt.legend(patches,labels,loc="best")
plt.axis('equal')
plt.tight_layout()
plt.title("Crime Percentage Distribution Across Districts: 2014 & 2015")
mngr = plt.get_current_fig_manager()
mngr.window.setGeometry(450,0,450,600)
DistrictDataPie.show()
#plt.savefig('CrimePercentages.png')
################################################################################

#Bar Chart for Common Offenses: 2014 & 2015

crimeTypes = ["LARCENY","ASSAULT","AUTO THEFT","ARSON", "VANDALISM","WEAPON",
                "DRUG","JUVENILE","FAMILY","CONDUCT","DEATH","FORGERY","DRIVING"]
                
crimeStats = []

for crime in crimeTypes:
    select_str = "SELECT COUNT([Crime Description]) AS crimeCount FROM [dbo].[crime]\
                  WHERE [Crime Description] LIKE '%" + crime + "%'"              
    crimeStats.append(sql_select(select_str)[0][0])


crimeTypes = ["Larceny","Assault","Auto Theft","Arson", "Vandalism","Weapons",
                "Drug Possession","Juvenile","Family Offense","Disorderly Conduct","Death","Forgery",
                "DUI"]

offenseBarChart = plt.figure(3)

bar_width = 0.1
plt.title("Common Offenses: 2014 & 2015")
plt.ylabel("# of Occurrences")
x_pos = np.arange(1)

colors = ['red','yellow', 'cyan','lightcoral','green', 'blue','purple','pink',
          'orange','skyblue','magenta','grey','brown'] 

barPos = 0 
for index, stat in enumerate(crimeStats):
    plotOffenses = plt.bar(x_pos+barPos,[stat],bar_width,color=colors[index],alpha=0.8,label=crimeTypes[index])
    barPos += bar_width

limit = max(crimeStats)+100 

plt.xticks([],[])
plt.legend()
plt.ylim(0,limit)
plt.grid(True)

mngr = plt.get_current_fig_manager()
mngr.window.setGeometry(900,0,500,600)
offenseBarChart.show()