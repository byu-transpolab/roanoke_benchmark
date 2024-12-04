'''
Remove from roanoke and place on desktop. Use this code when running container to mount this file. 

docker run -it --name CONTAINERNAME --mount type=bind,source=/FILE/PATH/TO/DATA,target=/app/userdata CONTAINERNAME

'''


from aequilibrae import Project
from os.path import join

import pandas as pd
import logging
import sys

"        Creates a new project      "



folder_location ='app/userdata' #This is the location of your project
folder_name = 'test4'           #This is the name for your project

#Creates file path, and creates a new Aequilibrae project
folder = join(folder_location,folder_name) 
project = Project()
project.new(folder)



"         Adding Links              "


"       Network Skimming        "

#Acesses project location, opens it.
#project = project_test_1.open(folder)


#path to link folder
link_folder ='app/hwy/links.csv'
df = pd.read_csv(link_folder)

# We cannot use the existing link_id, so we create a new field to not loose
# this information
links = project.network.links
link_data = links.fields

# Create the field and add a good description for it
link_data.add("source_id", "link_id from the data source")

# We need to refresh the fields so the adding method can see it
links.refresh_fields()

# We can now add all links to the project!
for idx, record in df.iterrows():
    new_link = links.new()

    # Now let's add all the fields we had
    new_link.source_id = record.link_id
    new_link.direction = record.directed
    new_link.modes = record.facility_type           #adding mode and link_type???
    new_link.link_type = record.facility_type
    new_link.name = record.name
    new_link.geometry = load_wkt(record.geometry)
    new_link.save()

# %%
# We grab all the links data as a geopandas GeoDataFrame so we can process it easier
links = project.network.links.data

logger = project.logger
stdout_handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s;%(levelname)s ; %(message)s")
stdout_handler.setFormatter(formatter)
logger.addHandler(stdout_handler)

from aequilibrae.paths import NetworkSkimming
import numpy as np

#builds the graphs
project.network.build_graphs()
