'''



USE THIS IF YOU DON'T HAVE ANY NODES, ONLY LINKS. THIS WILL CREATE NODES FOR YOU. CENTROIDS WILL STILL NEED TO BE ASSIGNED.


'''
from aequilibrae.project import Project
from aequilibrae.parameters import Parameters
from os.path import join

import time

from shapely.wkt import loads as load_wkt
from string import ascii_lowercase
import pandas as pd
import folium
import logging
import sys


time_start = time.time()
#Path to link and nodes
link_file ='/app/hwy/links.csv'
node_file ='app/hwy/nodes.csv'

#Location and name for project
folder_location ='app/userdata/tests' #This is the location of your project
project_name = 'testlink1'              #This is the name for your project

#Creates file path, and creates a new Aequilibrae project
folder = join(folder_location,project_name) 

#Create New Project
project = Project()
project.new(folder)
time_end = time.time()
print('Project Created:', time_end - time_start, 's')


# Load the CSV file into a DataFrame
df_node = pd.read_csv(node_file)
df_link = pd.read_csv(link_file)
df_node.to_csv(node_file, index=False)


"       Adding Link_types to Project       "

time_start = time.time()
# The links we have in the data are:
link_types = df_link.facility_type.unique()

 
# And the existing link types are
lt = project.network.link_types
lt_dict = lt.all_types()
existing_types = [ltype.link_type for ltype in lt_dict.values()]

# Adding New link Types
types_to_add = [ltype for ltype in link_types if ltype not in existing_types]
for i, ltype in enumerate(types_to_add):
    new_type = lt.new(ascii_lowercase[i]) #ID assisned to new link
    new_type.link_type = ltype
    # new_type.description = 'Your custom description here if you have one'
    new_type.save()

time_end = time.time()
print('Link Types Added:', time_end - time_start, 's')


"       Adding modes to Project       "
time_start = time.time()
# Existing modes 
md = project.network.modes
md_dict = md.all_modes()
existing_modes = {k: v.mode_name for k, v in md_dict.items()}

# All variations of mode types
all_variations_string = "".join(df_link.allowed_uses.unique())
all_modes = set(all_variations_string)

# Adding new modes to the project
modes_to_add = [mode for mode in all_modes if mode not in existing_modes]
for i, mode_id in enumerate(modes_to_add):
    new_mode = md.new(mode_id)
    # Edit to give uniqe names 
    new_mode.mode_name = f"Mode_from_original_data_{mode_id}"
    # new_type.description = 'Your custom description here if you have one' #Use to add descriptions

    # Saving the modes to the project
    project.network.modes.add(new_mode)
    new_mode.save()

time_end = time.time()
print('Mode Types Added:', time_end - time_start, 's')


"       Adding Link File       "
time_start = time.time()
# We cannot use the existing link_id, so we create a new field to not loose
# this information
links = project.network.links
link_data = links.fields

# Create the field and add a good description for it
link_data.add("source_id", "link_id from the data source")

# We need to refresh the fields so the adding method can see it
links.refresh_fields()

# Adding all links to the project!   Note! Change the names on the left side to reflect names in link file.
for idx, record in df_link.iterrows():
    new_link = links.new()
    new_link.source_id = record.link_id      #Link ID name
    new_link.direction = record.directed
    new_link.link_type = record.facility_type
    new_link.modes = record.allowed_uses
    new_link.name = record.name
    new_link.geometry = load_wkt(record.geometry)
    new_link.save()

time_end = time.time()
print('Linked added to Project:', time_end - time_start, 's')

'''
"       Adding Node File       "
time_start = time.time()

#Needed?
nodes = project.network.nodes
nodes_data = nodes.fields

# Create the field and add a good description for it
nodes_data.add("source_id", "node_id from the data source")

# We need to refresh the fields so the adding method can see it
nodes.refresh_fields()

# Adding all links to the project!
for idx, record in df_node.iterrows():
    new_node = nodes.new()
    new_node.nodes_id = record.nodes_id #ID
    new_node.is_centroid = record.Z
    new_node.save()


time_end = time.time()
print('Nodes added to Project:', time_end - time_start, 's')


'''


'''  Suppose to Display Map 
# We grab all the links data as a geopandas GeoDataFrame so we can process it easier
links = project.network.links.data

#Ploting Network
map_osm = links.explore(color="blue", weight=10, tooltip="link_type", popup="link_id", name="links")
folium.LayerControl().add_to(map_osm)
map_osm
'''


