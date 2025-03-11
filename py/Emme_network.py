

import pandas as pd
import inro.emme.desktop.app as _app
import inro.modeller as _m

# Define paths
emme_project = r"C:\Users\kmsquire\source\EMME networks\Roanoke\Roanoke.emp"
nodes_file = r"C:\Users\kmsquire\source\repos\roanoke_benchmark\hwy\node.csv"
links_file = r"C:\Users\kmsquire\source\repos\roanoke_benchmark\hwy\link.csv"
use_group_file = r"C:\Users\kmsquire\source\repos\roanoke_benchmark\hwy\use_group.csv"

# Start EMME session
my_desktop = _app.start_dedicated(project=emme_project, visible=True, user_initials="KMS")
my_modeller = _m.Modeller(my_desktop)

# Load CSV data
nodes_df = pd.read_csv(nodes_file)
links_df = pd.read_csv(links_file)
modes_df = pd.read_csv(use_group_file)


#Do not delete any code above this

# Get active scenario and network
my_scenario = my_modeller.scenario
network = my_scenario.get_network()


# Create the modes table using the use_group_file

# Code
# Codey
# Coding
# Very nice code


#Create Modes table
for _, row in modes_df.iterrows():
    mode_id = row['mode']
    description = row['description']
    mode_type = row['type']  # "AUTO", "TRANSIT", or "AUXILIARY"
    
    if not network.mode(mode_id):
        # Create mode with only id and type
        mode = network.create_mode(id=mode_id, type=mode_type)
        mode.description = description  # Set description separately


#Create Nodes
for i, row in nodes_df.iterrows():
    node_id = row['node_id']
    x_coord = row['x_coord']
    y_coord = row['y_coord']
    zone_id = row['zone_id']
    is_centroid = row['is_centroid']
    
    if network._nodes[node_id]:
        #node = network.create_node(id=node_id,  is_centroid=is_centroid) ALREADY CREATED???
        network._nodes[node_id].x = x_coord
        network._nodes[node_id].y = y_coord
        network._nodes[node_id].data1 = zone_id #For now saved under data1


#The code as it is will create the link file. However, it will only populate the From, To, and Modes columns. 
#It does not populate the length, type, or lanes columns, and I do not know why.

#Work in progress
#Create Links

""" link_type_map = {
    'interstate_principal_freeway': 1,
    'minor_freeway': 2,
    'principal_arterial': 3,
    'major_arterial': 4,
    'minor_arterial': 5,
    'major_collector': 6,
    'minor_collector': 7,
    'local': 8,
    'highspeed_ramp': 9,
    'lowspeed_ramp': 10,
    'centroid_connector': 11,
    'external_station_connector': 12
}

# Create Links
for _, row in links_df.iterrows():
    from_node = row['from_node_id']
    to_node = row['to_node_id']
    length = float(row['length']) if not pd.isna(row['length']) else 0.0
    link_type = row['link_type']
    capacity = row['capacity']
    free_speed = row['free_speed']
    num_lanes = row['lanes']
    allowed_uses = row['allowed_uses']

    if not network.link(from_node, to_node):
        # Create the link without num_lanes or type (set those after creation)
        link = network.create_link(i_node=from_node, j_node=to_node, length=length)

        # Set additional link attributes
        link.capacity = capacity
        link.free_speed = free_speed
        link.num_lanes = num_lanes  # Set num_lanes separately
        
        # Convert link_type string to integer
        link.type = link_type_map.get(link_type, 0)  # Default to 0 if no match

        # Assign allowed uses (modes)
        for mode in allowed_uses.split(','):
            if mode.strip() and network.mode(mode.strip()):
                link.modes |= {network.mode(mode.strip())} """




my_scenario.publish_network(network)
print ("Network succesfully imported!")

