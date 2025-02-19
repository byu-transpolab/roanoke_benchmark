from aequilibrae.project import Project
from aequilibrae.parameters import Parameters
from os.path import join
from shapely.geometry import LineString
import os

import time
from shapely.wkt import loads as load_wkt
from string import ascii_lowercase
import pandas as pd
import logging
import sys



#Opens a specific project
existing_project = Project()
dir_to_project = 'app/userdata/tests'                          #Path to the projects
current_project = 'testgmns7'                                  #This is the project you want to open
existing_project.open( join(dir_to_project,current_project) )


#Acesses all links in project
time_start = time.time()
project_links = existing_project.network.links

link1 = project_links.get(1)
print(link1)

time_end = time.time()
print('Acesses Link', time_end - time_start, 's')


#Acesses the Nodes in the Project
time_start = time.time()
project_nodes  = existing_project.network.nodes

node1 = project_nodes.get(1)

print(node1)
time_end = time.time()
print('Access Node', time_end - time_start, 's')

'''

#Export Curent Project into gmns
gmns_test = 'app/userdata/tests/project_to_gmns'
# Create a new folder for gmns data
try:
    os.mkdir(join(gmns_test,current_project))
    print(f"Directory '{current_project}' created successfully.")
except FileExistsError:
    print(f"Directory '{current_project}' already exists.")
existing_project.network.export_to_gmns(path=join(gmns_test,directory_name))


'''

'''
newlinks = {
    "interstate_principal_freeway": {"description": "link type", "lane_capacity": "9000", "lanes": 4, "link_type_id": "a", "required": False},
    "minor_freeway": {"description": "link type", "lane_capacity": "9000", "lanes": 4, "link_type_id": "b", "required": False},
    "principal_arterial": {"description": "link type", "lane_capacity": "9000", "lanes": 4, "link_type_id": "c", "required": False},
    "major_arterial": {"description": "link type", "lane_capacity": "9000", "lanes": 4, "link_type_id": "d", "required": False},
    "minor_arterial": {"description": "link type", "lane_capacity": "9000", "lanes": 4, "link_type_id": "e", "required": False},
    "major_collector": {"description": "link type", "lane_capacity": "9000", "lanes": 4, "link_type_id": "f", "required": False},
    "minor_collector": {"description": "link type", "lane_capacity": "9000", "lanes": 4, "link_type_id": "g", "required": False},
    "local": {"description": "link type", "lane_capacity": "9000", "lanes": 4, "link_type_id": "h", "required": False},
    "highspeed_ramp": {"description": "link type", "lane_capacity": "9000", "lanes": 4, "link_type_id": "i", "required": False},
    "lowspeed_ramp": {"description": "link type", "lane_capacity": "9000", "lanes": 4, "link_type_id": "j", "required": False},
    "centroid_connector": {"description": "link type", "lane_capacity": "9000", "lanes": 4, "link_type_id": "k", "required": False},
    "external_station_connector": {"description": "link type", "lane_capacity": "9000", "lanes": 4, "link_type_id": "l", "required": False}
    }
     
par = Parameters()
par.parameters["network"]["links"].update(newlinks)
par.write_back()
'''