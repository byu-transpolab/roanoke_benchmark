
import path4gmns_skim as pg
import gtfs2gmns_conversion as gtfs


# Source Files
input_dir = "hwy"
tran_input_dir = "transit/gtfs/roanoke"

# Output file and path
output_dir = "hwy"
tran_output_dir = "transit"
output_type = ".csv"  # Choose between ".csv", ".omx", or ".zip"

cost_type = "time" # Set to the cost type for skim.
time_period = '0000_2359'

#File paths for read_network
link_file = 'hwy/link.csv'      
node_file = 'hwy/node.csv'

#gtfs.gtfs2gmns(tran_input_dir,tran_output_dir, time_period)

#nt =pg.read_network(length_unit='mi', speed_unit='mph', input_dir=input_dir)

print(pg.run_skim_network('mi','mph',input_dir, output_dir, cost_type, output_type))



'''
    for i in range(len(agents) - 1):  # -1 removed auto added "auto" type
        print(agents[i].name)
        G.agent_type_name = "all"  # agents[i].name
        mode_type = agents[i].type

    # Create a placeholder list to maintain index positions
        filtered_links = [None] * len(G.links)

    # Iterate through the original links and place valid links in their original index positions
        for j, link in enumerate(G.links):
            if mode_type in link.allowed_uses.lower():
                filtered_links[j] = link  # Maintain index position

    # Remove None values, keeping only the valid links
        G.links = [link for link in filtered_links if link is not None]
    ''' 


'''
     for i in range(len(agents)-1): # -1 removed auto added "auto" type
        print(agents[i].name)
        G.agent_type_name = "all" #agents[i].name
        mode_type = agents[i].type
        filtered_links = [links for links in G.links if mode_type in links.allowed_uses.lower()]
        G.links = filtered_links
    
    print(agents[i].type) #Letter representing mode on link
    print(len(agents)) # Total length of link
    print(agents[i].name) #Name of type of skim
    '''




'''
#Compute skim
#print(nt.find_shortest_path(2, 5472,"all", "node", cost_type))
#print(nt.get_shortest_path(2,5472,cost_type))
#print(nt.get_shortest_path_tree(1, "time"))

def create_settings_yaml(input_dir, file_path="settings.yml"):
    csv_path = os.path.join(input_dir, "use_group.csv")
    
    if os.path.exists(file_path):
        print(f"Settings file '{file_path}' already exists. Skipping creation.")
        return
    
    df = pd.read_csv(csv_path)
    settings = {"agents": []}
    
    for _, row in df.iterrows():
        agent = {
            "type": row["type"],
            "name": row["mode"],
            "description": row["description"],
            "vot": 1.0,  # Default value, can be updated as needed
            "flow_type": "standard",  # Placeholder
            "pce": 1.0,  # Placeholder
            "free_speed": 50.0,  # Placeholder
            "use_link_ffs": True  # Default setting
        }
        settings["agents"].append(agent)
    
    with open(file_path, "w") as file:
        yaml.dump(settings, file, default_flow_style=False)
    
    print(f"Settings file '{file_path}' created successfully.")


create_settings_yaml(input_dir)




#Read link and nodes into network
nt = pg.read_network(length_unit='mi', speed_unit='mph', input_dir=input_dir)
x = 2
y = 5472

print(nt.find_shortest_path_distance(x,y))
print(nt.find_shortest_path(x,y))

''' 
    
   


'''
#for i in range(G.link_size):
     #   print(G.links[i].fftt)
        
    #for i in range(G.node_size):
       #print(G.nodes[i].node_id)
    #node_ids = np.array([G.nodes[i].node_id for i in range(G.node_size)])
    #print(node_ids)


#### To and From nodes ###
from_node = 1101
to_node =3414
# node path value from node 1 to node 2s
#print(nt.find_shortest_path(from_node, to_node))
#nt.find_shortest_path()

 # Load the network
    #network.read_network(length_unit="mi", speed_unit="mph", input_dir=input_dir)


# Define dimensions
rows = len(df_node.node_id)
cols = rows
rowplace = (df_node.node_id)
colplace = (df_node.node_id)

#
def create_numpy_matrix(rows, cols):
    time_start_matrix_all = time.time() #Start Total time stop watch
    time_start = time.time ()           #Initailize step counter timer
    matrix = [[0 for _ in range(cols)] for _ in range(rows)]  # Create a matrix of zeros manually
    matrix = np.array(matrix)                                 # Convert to NumPy array
    for i in range(0, rows):
        time_end = time.time()
        print('Time to preform interation ',i, '-' , time_end - time_start, 's') # Time for each step
        time_start = time.time()
        for j in range (0, cols):
          matrix[i,j] = network.find_shortest_path_value(rowplace[i], colplace[j]) #Path4gmns calc for distence between two nodes
    
    return matrix  


time_start_matrix_all = time.time()
matrix = create_numpy_matrix(rows, cols)
time_end_matrix_all = time.time()

#Print out matrix and time for completion
print(matrix)
print('Matrix Creation Time:', time_end_matrix_all - time_start_matrix_all, 's') #Total time
np.savetxt('skim.csv', matrix, delimiter=",", fmt='%d')   # Save to CSV


# 'data/ASU' #
print(colplace[0])

print(rowplace[0])




# link path value from node 1 to node 2
print(network.find_shortest_path_value(from_node, to_node, seq_type='link'))

network = pg.read_network(length_unit='mi', speed_unit='mph', input_dir=network_file)
pg.read_demand(network)

# specify the parameters for traffic assignment
column_gen_num = 10
column_update_num = 10

# path-based UE only
pg.find_ue(network, column_gen_num, column_update_num,)

# if you do not want to include geometry info in the output file,
# use pg.output_columns(network, False)

# output column information to route_assignment.csv
pg.output_columns(network)
# output link performance to link_performance.csv
pg.output_link_performance(network)




import path4gmns_skim as pg
import numpy as np
import pandas as pd
import time

## Source File ##
network_file = 'hwy'        # Source folder for link/node files
link_file = 'hwy/link.csv'  # Link File for calculations
node_file = 'hwy/node.csv'  # Node file for calculations

# Read link and node files
df_link = pd.read_csv(link_file)
df_node = pd.read_csv(node_file)

###### Find Shortest Path Network ########
# Read link and nodes into network
network = pg.read_network(length_unit='mi', speed_unit='mph', input_dir=network_file)

# Define dimensions
nodes = df_node.node_id.to_numpy()  # Convert to NumPy array for faster operations
num_nodes = len(nodes)

# Matrix initialization
def create_numpy_matrix(num_nodes, nodes):
    """Creates a distance matrix using shortest path calculations in an optimized manner."""
    time_start_matrix_all = time.time()  # Start total stopwatch

    matrix = np.zeros((num_nodes, num_nodes))  # Initialize matrix with zeros

    # Vectorized approach using NumPy
    for i, row_node in enumerate(nodes):
        time_start = time.time()  # Start step timer
        
        shortest_paths = [network.find_shortest_path_value(row_node, col_node) for col_node in nodes]
        matrix[i, :] = shortest_paths  # Assign row in one operation instead of looping

        time_end = time.time()
        print(f'Time for iteration {i}: {time_end - time_start:.4f} s')  # Time for each step

    time_end_matrix_all = time.time()
    print(f'Matrix Creation Time: {time_end_matrix_all:.2f} s')  # Total time

    return matrix

# Create the matrix
matrix = create_numpy_matrix(num_nodes, nodes)

# Convert matrix to DataFrame for better formatting in CSV
df_matrix = pd.DataFrame(matrix, index=nodes, columns=nodes)

# Save the matrix as a CSV file
output_file = "hwy/src/shortest_path_matrix.csv"
df_matrix.to_csv(output_file, index=True, header=True)

print(f"Matrix saved to {output_file}")





import path4gmns_skim as pg
import numpy as np
import pandas as pd
import time                     #Tracking total time of process
from joblib import Parallel, delayed  # Parallel processing
from tqdm import tqdm           # Progress bar
import zipfile
import io                       # For in-memory file handling
import openmatrix as omx


### Source Files ###
network_file = 'hwy'            # Source folder for link/node files
link_file = 'hwy/link.csv'      # Link File for calculations
node_file = 'hwy/node.csv'      # Node file for calculations

###Output file and path ###
output_filepath = "hwy"                  #Folder location for output
output_filename = "old_shortest_path_matrix" #Output name (no extensions needed)
output_type = ".csv"                     #Desired Extesnion (".csv", ".omx", ".zip")

def find_shortest_path_network (network_file, link_file, node_file, output_filepath, output_filename, output_type):
    # Read link and node files
    df_link = pd.read_csv(link_file)
    df_node = pd.read_csv(node_file) 
    
    ### Convert lengths of road into travel time at FFSpeed ###
    df_link.length = (df_link.length / df_link.free_speed) * 60  # Convert travel time to minutes
    df_link.to_csv(link_file, index=False)
    
    ### Find Shortest Path Network ####
    network = pg.read_network(length_unit='mi', speed_unit='mph', input_dir=network_file)
    
    # Convert node IDs to NumPy array for efficiency
    nodes = df_node.node_id.to_numpy()
    num_nodes = len(nodes)
    
    # Function to compute shortest paths for a single row
    def compute_row_distances(row_node, nodes):
        return [network.find_shortest_path_distance(row_node, col_node) for col_node in nodes]

    # Parallel computation of skim_matrix rows with progress bar
    def create_numpy_matrix_parallel(num_nodes, nodes):
        time_start_matrix_all = time.time()  # Start stopwatch

    # Use joblib with tqdm progress bar
        skim_matrix = Parallel(n_jobs=-1)(
            delayed(compute_row_distances)(row_node, nodes) 
            for row_node in tqdm(nodes, desc="Computing shortest paths")
    )

        time_end_matrix_all = time.time()
        print(f'Matrix Creation Time: {time_end_matrix_all - time_start_matrix_all:.2f} s')

        return np.array(skim_matrix)
    
    # Create the skim_matrix with parallel processing and progress bar
    skim_matrix = create_numpy_matrix_parallel(num_nodes, nodes)
    
    # Convert matrix to DataFrame for structured output
    df_skim_matrix = pd.DataFrame(skim_matrix, index=nodes, columns=nodes)

    ### Convert lengths of road back to lengths from travel time ###
    df_link.length = (df_link.length / 60) * df_link.free_speed 
    df_link.to_csv(link_file, index=False)

    # Save as OMX (OpenMatrix Format)
    if output_type == ".omx":
        omx_file = f"{output_filepath}/{output_filename}.omx"
        with omx.open_file(omx_file, 'w') as omx_out:
            omx_out.create_matrix(
                name="shortest_path_matrix",
                obj=skim_matrix,  # Pass the NumPy array directly
                title="Shortest Path Distance Matrix",
                attrs={"Description": "This matrix contains the shortest path distances between nodes"}
            )
            # Create a mapping for node indexing
            omx_out.create_mapping("nodes", nodes)
        print(f"Matrix saved as OMX file: {omx_file}")
    
    # Save the matrix as a CSV file
    if output_type == ".csv":
        output_file = output_filepath + "/" + output_filename + ".csv"
        df_skim_matrix.to_csv(output_file, index=True, header=True, float_format="%.2f")  # Save with 6 decimal precision
        print(f"Matrix saved to {output_file}")
        
    ### If desired output is a zip file ###    
    if output_type == ".zip":
        output_file = output_filepath + "/" + output_filename + ".zip"
        csv_filename = output_filename + ".csv"
        #zip_filename = "hwy/shortest_path_matrix.zip"
        with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            with io.StringIO() as csv_buffer:
                df_skim_matrix.to_csv(csv_buffer, index=True, header=True, float_format="%.2f")  # Save with 6 decimal precision
                zipf.writestr(csv_filename, csv_buffer.getvalue())
        print(f"Matrix Zipfile saved to {output_file}")


    return

find_shortest_path_network (network_file, link_file, node_file, output_filepath, output_filename, output_type)
'''