from aequilibrae.project import Project
from aequilibrae.project import Project
from aequilibrae.parameters import Parameters
from os.path import join

import time

from shapely.wkt import loads as load_wkt
from string import ascii_lowercase
import pandas as pd
import logging
import sys

time_start = time.time()

#Path to link and nodes
link_file ='app/userdata/ASU/link.csv'
node_file ='app/userdata/ASU/node.csv'
#use_group ='app/userdata/test_use_group.csv'   #May or may not be needed in the future. Adding this currently fixes 'Resolved_group' error.

#Location and name for project
folder_location ='app/userdata/tests' #This is the location of your project
folder_name = 'ASU_test_10'           #This is the name for your project

#Creates file path, and creates a new Aequilibrae project
folder = join(folder_location,folder_name) 

#Create New Project
project = Project()
project.new(folder)
time_end = time.time()
print('Project Created:', time_end - time_start, 's')



"       Renaming Columns       "
# Load the CSV file into a DataFrame
df_node = pd.read_csv(node_file)
df_link = pd.read_csv(link_file)

# Rename ID Column column
df_node.rename(columns={'ID':  'node_id'}, inplace=True) #NEEDED!!!
df_link.rename(columns={'allowed_uses': 'modes'  }, inplace=True)
df_link.rename(columns={'facility_type': 'link_type' }, inplace=True)
df_link.rename(columns={'dir_flag': 'directed' }, inplace=True)

# Save the updated DataFrame back to the CSV file
df_node.to_csv(node_file, index=False)
df_link.to_csv(link_file, index=False)



time_start = time.time()
project.network.create_from_gmns(link_file, node_file) #, use_group
time_end = time.time()

print('Links and Nodes added to Project:', time_end - time_start, 's')
'''


"       Adding Link_types to Project       "
time_start = time.time()
# The link types we have in the link file are:
link_types = df_link.link_type.unique()

# And the existing link types are:
lt = project.network.link_types
lt_dict = lt.all_types()
existing_types = [ltype.link_type for ltype in lt_dict.values()]

alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","n","o","p","q","r","s","t","u","v","w","x"]
types_to_add = [ltype for ltype in link_types if ltype not in existing_types]
par = Parameters()

for i, ltype in enumerate(types_to_add):
    newlinks = {
        ltype: {"description": "link type", "lane_capacity": "9000", "lanes": 4, "link_type_id": alphabet, "required": False}}
    
    if ltype not in par.parameters["network"]["links"]:
        par.parameters["network"]["links"].update(newlinks)
        par.write_back()
        
time_end = time.time()
print('Link Types Added:', time_end - time_start, 's')



"       Adding mode types to Project       "
time_start = time.time()
# Existing modes 
md = project.network.modes
md_dict = md.all_modes()
existing_modes = {k: v.mode_name for k, v in md_dict.items()}

# All variations of mode types
all_variations_string = "".join(df_link.modes.unique())
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




" Adding Links and Nodes to the Project"



'''