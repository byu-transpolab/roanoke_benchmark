from gtfs_2_gmns import GTFS2GMNS
import pandas as pd

# Input and Output Directories
gtfs_input_dir = 'transit/src'
gtfs_output_dir = 'network'

hwy_node_path = 'network/node.csv'                      
tran_node_path = f"{gtfs_output_dir}/node_transit.csv"  

# Time and Date Configuration
time_period = "00:00:00_23:59:00"
  

# Create an instance of the GTFS2GMNS class
gtfs2gmns_converter = GTFS2GMNS(
    gtfs_input_dir=gtfs_input_dir,
    gtfs_output_dir=gtfs_output_dir,
    time_period=time_period,
    isSaveToCSV = True
    )


# Load GTFS data
print("Loading GTFS data...")
gtfs2gmns_converter.load_gtfs()


# Generate GMNS nodes and links
print("Generating GMNS nodes and links...")
nodes, links = gtfs2gmns_converter.gen_gmns_nodes_links()                      


# Generate and print access links
print("Generating access links...")
access_links = gtfs2gmns_converter.generate_access_link(hwy_node_path, tran_node_path)


# Combine links and access links into a single DataFrame
combined_links = pd.concat([links, access_links], ignore_index=True)

# Save combined links to a CSV file
combined_links.to_csv(f"{gtfs_output_dir}/transit_and_access_links.csv", index=False)
print("Combined Links saved to combined_links.csv.")

'''
# Save access links to a CSV file
access_links.to_csv(f"{gtfs_output_dir}/access_links.csv", index=False)
print("Access Links saved to access_links.csv.")
'''
