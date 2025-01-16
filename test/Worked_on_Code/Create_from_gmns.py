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
link_file ='app/userdata/Alternate_link_files/links_no_controids.csv'
node_file ='app/hwy/nodes.csv'

#Location and name for project
folder_location ='app/userdata/tests' #This is the location of your project
folder_name = 'testgmns100'           #This is the name for your project

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
#df_link.rename(columns={'allowed_uses': 'modes'  }, inplace=True)
#df_link.rename(columns={'facility_type': 'link_type' }, inplace=True)

# Save the updated DataFrame back to the CSV file
df_node.to_csv(node_file, index=False)
#df_link.to_csv(link_file, index=False)



" Adding Links and Nodes to the Project"
time_start = time.time()
project.network.create_from_gmns(link_file, node_file)
time_end = time.time()

print('Links and Nodes added to Project:', time_end - time_start, 's')


'''
"       Adding Link_types to Project       "
time_start = time.time()
# The links we have in the data are:
link_types = df_link.link_type.unique()

# And the existing link types are
lt = project.network.link_types
lt_dict = lt.all_types()
existing_types = [ltype.link_type for ltype in lt_dict.values()]

'''
#alphabet = ["n","o","p","q","r","s","t","u","v","w","x","a","b","c","d"]

#,"e","f","g","h","i","j","k","l","m",
'''




# Adding New link Types
types_to_add = [ltype for ltype in link_types if ltype not in existing_types]
for i, ltype in enumerate(types_to_add):
    new_type = lt.new(alphabet[i]) #ID assisned to new link
    new_type.link_type = ltype
    # new_type.description = 'Your custom description here if you have one'
    new_type.save()

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

'''

'''
#Adding Centroid Data to be collected in the parameter

centroid_field = {
    "centroid": {"description": "centroid flag", "type": "boolean", "required": False}}
    
par = Parameters()
par.parameters["network"]["gmns"]["node"]["fields"].update(centroid_field)
par.write_back()
'''



