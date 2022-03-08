"""
Process the JSON file named univ.json. Create 3 maps per instructions below.
The size of the point on the map should be based on the size of total enrollment. Display only those schools 
that are part of the ACC, Big 12, Big Ten, Pac-12 and SEC divisons (refer to valueLabels.csv file)
The school name and the specific map criteria should be displayed when you hover over it.
(For example for Map 1, when you hover over Baylor, it should display "Baylor University, 81%")
Choose appropriate tiles for each map.


Map 1) Graduation rate for Women is over 50%
Map 2) Percent of total enrollment that are Black or African American over 10%
Map 3) Total price for in-state students living off campus over $50,000

"""

import json
import csv

infile = open('univ.json', 'r')
school_data = json.load(infile)

infile_csv = open('ValueLabels.csv', 'r')
csvfile_reader = csv.reader(infile_csv, delimiter = ',')
next(csvfile_reader)  #Read header row


#Map 1
#Graduation rate for Women is over 50%
grad_rates_women = []
lons = []
lats = []
hover_texts = []
enrollments = []
division_names = ["Atlantic Coast Conference", "Big Twelve Conference", "Big Ten Conference", "Pacific-12 Conference", "Southeastern Conference"]
division_dict = {}

#Store school values
for line in csvfile_reader:
    if line[2] in division_names:
        division_dict[line[2]] = line[1]



for school in school_data:
    if str(school["NCAA"]["NAIA conference number football (IC2020)"]) in division_dict.values():
        if school["Graduation rate  women (DRVGR2020)"] > 50:
            grad_rate_women = school["Graduation rate  women (DRVGR2020)"]
            lon = school["Longitude location of institution (HD2020)"]
            lat = school["Latitude location of institution (HD2020)"]
            name = school["instnm"]
            enrollment = school["Total  enrollment (DRVEF2020)"]

            grad_rates_women.append(grad_rate_women)
            lons.append(lon)
            lats.append(lat)
            hover_texts.append(name+', '+ str(grad_rate_women) +'%')
            enrollments.append(enrollment)



print(len(grad_rates_women))

#Map 1 visualization
from plotly.graph_objs import Scattergeo, Layout
from plotly import offline

data = [
    {'type': 'scattergeo',
    'lon':lons,
    'lat':lats,
    'text':hover_texts,
    'marker':{
        'size':[enrollment/2000 for enrollment in enrollments],
        'color':enrollments,
        'colorscale':'Viridis',
        'reversescale':True,
        'colorbar':{'title':'Number of Enrollments'}
    },
    }]
        

my_layout = Layout(title='Schools with graduation rate for women over 50%')
fig = {'data':data, 'layout':my_layout}

offline.plot(fig, filename='Map 1 - Graduation rate for women.html')






