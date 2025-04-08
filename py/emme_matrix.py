#Create an empty EMME network

import pandas as pd
import inro.emme.desktop.app as _app
import inro.modeller as _m

# Define paths
emme_project = r"C:\Users\kmsquire\source\EMME networks\Roanoke\Roanoke.emp"
nodes_file = r"C:\Users\kmsquire\source\repos\roanoke_benchmark\network\node.csv"
links_file = r"C:\Users\kmsquire\source\repos\roanoke_benchmark\network\link.csv"
use_group_file = r"C:\Users\kmsquire\source\repos\roanoke_benchmark\network\use_group.csv"

# Start EMME session
my_desktop = _app.start_dedicated(project=emme_project, visible=True, user_initials="KMS")
my_modeller = _m.Modeller(my_desktop)

# Load CSV data
nodes_df = pd.read_csv(nodes_file)
links_df = pd.read_csv(links_file)
modes_df = pd.read_csv(use_group_file)


# Get active scenario and network
my_scenario = my_modeller.scenario
network = my_scenario.get_network()

#Delete any existing links, nodes, and modes.
for i, row in nodes_df.iterrows():
    if network.node(row['node_id']):  # Check if the node exists
        network.delete_node(id=row['node_id'], cascade=True)

for i, row in modes_df.iterrows():
    if network.mode(row['mode']):  # Check if the mode exists
        network.delete_mode(id=row['mode'], cascade=True)

for i, row in links_df.iterrows():
    if network.link(row['from_node_id'], row['to_node_id']):  # Check if the link exists
        network.delete_link(i_node_id=row['from_node_id'], j_node_id=row['to_node_id'], cascade=True)


#Create Modes table
for _, row in modes_df.iterrows():
    mode = network.create_mode(id=row['mode'], type=row['type'])
    mode['description'] = row['description']  # Set description separately


#Create Nodes
for i, row in nodes_df.iterrows():
    node = network.create_node(id=row['node_id'],  is_centroid= row['is_centroid']) 
    node['x'] = row['x_coord']
    node['y'] = row['y_coord']
    node['data1'] = row['zone_id']


#Turn NaN values into a string
links_df['facility_type'] = links_df['facility_type'].fillna('').astype(str).str.strip()

#Map the link_type if it is in a string in the link.csv file
link_type_map = {
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
    'external_station_connector': 12,
    'unknown_type': 13,
    'bus': 14,
    '': 15}

#Create Links
for _, row in links_df.iterrows():
    link = network.create_link(i_node_id=row['from_node_id'],j_node_id=row['to_node_id'],modes=row['allowed_uses'])
    link['num_lanes']=row['lanes']
    link['length']=row['length']
    link['type'] = link_type_map.get(row['facility_type'])


#Publish the network
my_scenario.publish_network(network)
print ("Network succesfully imported!")


# ==== CREATE TRAVEL TIME MATRIX ====

import inro.emme.matrix as matrix

emmebank = my_modeller.emmebank

def create_matrix(matrix_id):
    # Get the list of zones
    #scenario = emmebank.scenario(3001)
    zones = my_scenario.zone_numbers

# Create index for matrix
    indices = [zones,zones]

# Create matrix with 0s
    new_mat = matrix.MatrixData (indices, default_value=0, type='f')

#print("New matrix indices=%s" % str(new_mat.indices))
    print("\n")
    print("The new matrix value at O-D=(5,6) is %s " % str(new_mat.get(5,6)))

    existing_matrix = emmebank.matrix(matrix_id)
    if existing_matrix is not None:
        print(f"Matrix with ID '{matrix_id}' already exists.")
    else:
        matrix_new = emmebank.create_matrix(matrix_id, 0)
        matrix_new.name = "Custom_matrix"
        print(f"Matrix with ID '{matrix_id}' created.")
        matrix_new.set_data(new_mat)

matrix_id = "mf3"

matrix_current = emmebank.matrix(matrix_id)
if matrix_current is not None:
    value = matrix_current.get_data(my_scenario).get(5,7)
    print(value)
#Kaleigh, I've gotten it to create a matrix. Message me and I can explain what I can about the above code. 
# Connor

