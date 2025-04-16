import sys
import os
import openmatrix as omx
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))) # So that path4gmns can be accessed
import path4gmns as pg


def skim_network(length_unit,speed_unit,network_dir, output_dir, output_type, cost_type):
    """ Creates Travel Time Skims based off modes in use_group file. 

    Args:
        length_unit(str): 'mile' or 'km' (km currently not supported)
        speed_unit (str): 'mph' or 'kph' ('kph' currently not supported)
        network_dir (str): File path to gmns network files. ex 'network/roanoke/hwy'
        output_dir (str): File path to desired location for skims
        output_type (str): '.omx' or '.csv'. omx files are saved as one file. csv are saved seperatly.
        cost_type (str): 'time' or 'distance' (distance currently not supported)
    """
# Run_skim_netowrk is found under io.py in path4gmns
    print(pg.run_skim_network(length_unit, speed_unit,network_dir, output_dir, cost_type, output_type))



def read_omx_file (file_path = "skims/shortest_path_matrix_time.omx"):
# Read omx file, give attributes
    # Give saved matrices
    with omx.open_file(file_path, "r") as f:
        print(f"matrices saved in {file_path}")
        print(f.list_matrices())

    
    
#Preview some of the matrix
    with omx.open_file(file_path, "r") as f:
        matrices = {idx: matrix_name for idx, matrix_name in enumerate(f.list_matrices())}
    for idx, matrix_name in matrices.items():
        matrix_data = f[matrix_name][:]  
        print(f"Matrix '{matrix_name}':\n", matrix_data)
  
  
    with omx.open_file(file_path, "r") as f:
        print("Attributes:", f.list_all_attributes())

'''
    with omx.open_file(file_path, "r") as f:
        for matrix_name in f.list_matrices():
            print(f"Matrix: {matrix_name}")

            # Get matrix object
            matrix = f[matrix_name]

            # Retrieve and print attributes
            attributes = {key: matrix.attrs[key] for key in matrix.attrs._f_list()}
            print(f"Attributes for '{matrix_name}':", attributes)
'''

if __name__ == "__main__":
    # Source network
    network_dir = "network"

    # Output file and path
    output_dir = "skims"
    output_type = ".omx"  # Choose between ".csv", ".omx"

    #Cost Type
    cost_type = "time" # Set to the cost type for skim. Either time or distance

    # Unit types
    length_unit = 'mi'
    speed_unit = "mph"
    
    skim_network(length_unit,speed_unit,network_dir, output_dir, output_type, cost_type)