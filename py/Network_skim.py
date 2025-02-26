import path4gmns_skim as pg
import numpy as np
import pandas as pd
import time
from joblib import Parallel, delayed
from tqdm import tqdm
import zipfile
import io
import openmatrix as omx
import os


network_file = "hwy"
link_file = os.path.join(network_file, "link.csv")
node_file = os.path.join(network_file, "node.csv")

# Output file and path
output_dir = "hwy"
output_filename = "shortest_path_matrix"
output_type = ".omx"  # Choose between ".csv", ".omx", or ".zip"


def compute_row_distances(row_node, nodes, network):
    """
    Computes the shortest path distances from a single node to all other nodes.

    Parameters:
        row_node (int): The source node ID.
        nodes (np.ndarray): Array of all node IDs.
        network: The loaded network object.

    Returns:
        list: List of shortest path distances.
    """
    return [network.find_shortest_path_distance(row_node, col_node) for col_node in nodes]


def create_numpy_matrix_parallel(nodes, network):
    """
    Creates a shortest path distance matrix using parallel processing.

    Parameters:
        nodes (np.ndarray): Array of all node IDs.
        network: The loaded network object.

    Returns:
        np.ndarray: The shortest path distance matrix.
    """
    start_time = time.time()

    # Use joblib with tqdm for parallel computation
    skim_matrix = Parallel(n_jobs=-1)(
        delayed(compute_row_distances)(row_node, nodes, network)
        for row_node in tqdm(nodes, desc="Computing shortest paths")
    )

    elapsed_time = time.time() - start_time
    print(f"Matrix Creation Time: {elapsed_time:.2f} s")

    return np.array(skim_matrix)


def save_as_omx(matrix, nodes, output_path):
    """
    Saves the shortest path matrix as an OMX file.

    Parameters:
        matrix (np.ndarray): The shortest path matrix.
        nodes (np.ndarray): Array of node IDs.
        output_path (str): Path to save the OMX file.
    """
    with omx.open_file(output_path, "w") as omx_out:
        omx_out.create_matrix(
            name="shortest_path_matrix",
            obj=matrix,
            title="Shortest Path Distance Matrix",
            attrs={"Description": "This matrix contains the shortest path distances between nodes"},
        )
        omx_out.create_mapping("nodes", nodes)

    print(f"Matrix saved as OMX file: {output_path}")


def save_as_csv(df_matrix, output_path):
    """
    Saves the shortest path matrix as a CSV file.

    Parameters:
        df_matrix (pd.DataFrame): DataFrame containing the shortest path matrix.
        output_path (str): Path to save the CSV file.
    """
    df_matrix.to_csv(output_path, index=True, header=True, float_format="%.2f")
    print(f"Matrix saved to {output_path}")


def save_as_zip(df_matrix, output_path, csv_filename):
    """
    Saves the shortest path matrix as a zipped CSV file.

    Parameters:
        df_matrix (pd.DataFrame): DataFrame containing the shortest path matrix.
        output_path (str): Path to save the zip file.
        csv_filename (str): Name of the CSV file inside the zip archive.
    """
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        with io.StringIO() as csv_buffer:
            df_matrix.to_csv(csv_buffer, index=True, header=True, float_format="%.2f")
            zipf.writestr(csv_filename, csv_buffer.getvalue())

    print(f"Matrix Zipfile saved to {output_path}")


def find_shortest_path_network(network_file, link_file, node_file, output_filepath, output_filename, output_type):
    """
    Reads network files, computes the shortest path distance matrix, and saves it in the desired format.

    Parameters:
        network_file (str): Path to the network directory.
        link_file (str): Path to the link file.
        node_file (str): Path to the node file.
        output_filepath (str): Directory to save the output files.
        output_filename (str): Base name of the output file (without extension).
        output_type (str): Desired output format (".csv", ".omx", ".zip").
    """
    # Load link and node data
    df_link = pd.read_csv(link_file)
    df_node = pd.read_csv(node_file)

    # Convert link lengths to travel time at free-flow speed
    df_link["length"] = (df_link["length"] / df_link["free_speed"]) * 60
    df_link.to_csv(link_file, index=False)

    # Load the network
    network = pg.read_network(length_unit="mi", speed_unit="mph", input_dir=network_file)

    # Convert node IDs to a NumPy array
    nodes = df_node["node_id"].to_numpy()

    # Compute shortest path matrix in parallel
    skim_matrix = create_numpy_matrix_parallel(nodes, network)

    # Convert matrix to DataFrame
    df_skim_matrix = pd.DataFrame(skim_matrix, index=nodes, columns=nodes)

    # Convert travel time back to length
    df_link["length"] = (df_link["length"] / 60) * df_link["free_speed"]
    df_link.to_csv(link_file, index=False)

    # Create output directory if it doesn't exist
    os.makedirs(output_filepath, exist_ok=True)

    # Save the matrix in the requested format
    output_path = os.path.join(output_filepath, f"{output_filename}{output_type}")

    if output_type == ".omx":
        save_as_omx(skim_matrix, nodes, output_path)

    elif output_type == ".csv":
        save_as_csv(df_skim_matrix, output_path)

    elif output_type == ".zip":
        csv_filename = f"{output_filename}.csv"
        save_as_zip(df_skim_matrix, output_path, csv_filename)



if __name__ == "__main__":
    find_shortest_path_network(network_file, link_file, node_file, output_dir, output_filename, output_type)