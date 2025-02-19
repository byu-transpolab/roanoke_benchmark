import path4gmns_skim as pg
import numpy as np
import pandas as pd
import time      #Tracking total time of process
from joblib import Parallel, delayed  # Parallel processing
from tqdm import tqdm  # Progress bar
import zipfile
import io  # For in-memory file handling


### Source Files ###
network_file = 'hwy'            # Source folder for link/node files
link_file = 'hwy/link.csv'      # Link File for calculations
node_file = 'hwy/node.csv'      # Node file for calculations

###Output file and path ###
output_filepath = "hwy"                  #Folder location for output
output_filename = "shortest_path_matrix" #Output name (no extensions needed)


# Read link and node files
df_link = pd.read_csv(link_file)
df_node = pd.read_csv(node_file)

### Convert lengths of road into travel time at FFSpeed ###
df_link.length = (df_link.length / df_link.free_speed) * 3600  # Convert travel time to seconds

### Find Shortest Path Network ####
network = pg.read_network(length_unit='mi', speed_unit='mph', input_dir=network_file)

# Convert node IDs to NumPy array for efficiency
nodes = df_node.node_id.to_numpy()
num_nodes = len(nodes)

# Function to compute shortest paths for a single row
def compute_row_distances(row_node, nodes):
    return [network.find_shortest_path_distance(row_node, col_node) for col_node in nodes]

# Parallel computation of matrix rows with progress bar
def create_numpy_matrix_parallel(num_nodes, nodes):
    time_start_matrix_all = time.time()  # Start stopwatch

    # Use joblib with tqdm progress bar
    matrix = Parallel(n_jobs=-1)(
        delayed(compute_row_distances)(row_node, nodes) for row_node in tqdm(nodes, desc="Computing shortest paths")
    )

    time_end_matrix_all = time.time()
    print(f'Matrix Creation Time: {time_end_matrix_all - time_start_matrix_all:.2f} s')

    return np.array(matrix)

# Create the matrix with parallel processing and progress bar
matrix = create_numpy_matrix_parallel(num_nodes, nodes)
print(matrix)

# Convert matrix to DataFrame for structured output
df_matrix = pd.DataFrame(matrix, index=nodes, columns=nodes)
extension = 0  #ignore this

'''
### If the desired output is a csv file ###
# Save the matrix as a CSV file
extension = ".csv"
output_file = output_filepath + "/" + output_filename + extension
df_matrix.to_csv(output_file, index=True, header=True, float_format="%.6f")  # Save with 6 decimal precision
print(f"Matrix saved to {output_file}")
'''

### If desired output is a zip file ###
#'''
extension = ".zip"
output_file = output_filepath + "/" + output_filename + extension
csv_filename = output_filename + ".csv"
#zip_filename = "hwy/shortest_path_matrix.zip"
with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
    with io.StringIO() as csv_buffer:
        df_matrix.to_csv(csv_buffer, index=True, header=True, float_format="%.6f")  # Save with 6 decimal precision
        zipf.writestr(csv_filename, csv_buffer.getvalue())
print(f"Matrix Zipfile saved to {output_file}")
#'''
