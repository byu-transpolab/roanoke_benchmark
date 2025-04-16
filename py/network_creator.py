import pandas as pd
from simpledbf import Dbf5
import geopandas as gpd
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))) # So that gtfs2gmns can be accessed
from GTFS2GMNSII import gtfs2gmns, generate_access_links

#GLOBAL CONSTANTS
AUTO_FFS_CON = 60 #Miles per Hour
PED_FFS_CON = 4 # Feet per Second
BIKE_FFS_CON = 12 #Miles per Hour
UNKNOWN_FFS_CON = BIKE_FFS_CON 


# Function to read a DBF file and convert it to a DataFrame
def read_dbf(dbf_file):
    dbf = Dbf5(dbf_file)
    return dbf.to_dataframe()


# Function to save the DataFrame to CSV
def save_to_csv(df, csv_file):
    df.to_csv(csv_file, index=False)


# If the values in the facility_type/link_type column are integers, use this function to convert them to strings based on your data.
def factype_to_string(factype_value):
    if isinstance(factype_value, int):
        factype_dict = {
            1: 'interstate_principal_freeway', 
            2: 'minor_freeway', 
            3: 'principal_arterial', 
            4: 'major_arterial', 
            5: 'minor_arterial', 
            6: 'major_collector', 
            7: 'minor_collector', 
            8: 'local', 
            9: 'highspeed_ramp', 
            10: 'lowspeed_ramp', 
            11: 'centroid_connector', 
            12: 'external_station_connector'
        }
        return factype_dict.get(factype_value, f'unknown_type')  #_{factype_value}
    return 'Invalid FACTYPE'


# Function to create 'allowed_uses' column based on conditions 
def create_allowed_uses_column(df):
    allowed_uses = []
    
    for index, row in df.iterrows():
        use_parts = []
        
        # Check for TRAFF_PHB column (if it has 'Y')
        if 'traff_phb' in row and row['traff_phb'] == 'Y':
            use_parts.append('c')
        
        # Check for PED_PHB column (if it has 'Y')
        if 'ped_phb' in row and row['ped_phb'] == 'Y':
            use_parts.append('p')
        
        # Check for BIKE_FAC column (if it has any non-null, non-empty value)
        #if 'bike_facility' in row and pd.notnull(row['bike_facility']) and row['bike_facility'] != '':
        if 'ped_phb' in row and row['ped_phb'] == 'Y':
            use_parts.append('b')
        
        # Join the parts into a string and assign it to the allowed_uses list
        allowed_uses_value = ''.join(use_parts)
        
        # If no uses were added, assign 'cpbt'
        if not allowed_uses_value:
            allowed_uses_value = 'cpbt' #All possible modes of tranport
        
        allowed_uses.append(allowed_uses_value)
    
    # Assign the list as a new 'allowed_uses' column in the DataFrame
    df['allowed_uses'] = allowed_uses
    return df


# Function to create use group file based off the modes given in allowed uses. 
def create_use_group_file(network_link_dir, use_group_csv):
    df = pd.read_csv(network_link_dir)
    
    if 'allowed_uses' not in df.columns:
        print("Error: 'allowed_uses' column not found in the input file.")
        return
    
    # Define valid modes and their descriptions
    mode_info = {
        "c": ("car", "AUTO", AUTO_FFS_CON),
        "p": ("pedestrian", "AUX_TRANSIT", PED_FFS_CON),
        "b": ("bike", "AUX_TRANSIT", BIKE_FFS_CON),
        "t": ("transit", "TRANSIT",  AUTO_FFS_CON)
    }
    
    # Extract unique modes by checking if c, p, or b appears in allowed_uses
    unique_modes = set()
    for uses in df['allowed_uses'].dropna().astype(str):
        for char in uses:  # Iterate over each character
            if char in mode_info:
                unique_modes.add((char, mode_info[char][0], mode_info[char][1], mode_info[char][2]))
            else:
                unique_modes.add((char, "unknown", "AUX_TRANSIT", UNKNOWN_FFS_CON))  # Default values for unknown modes

    # Create a DataFrame with mode, description, type, and free_speed_constant
    use_group_df = pd.DataFrame(unique_modes, columns=['mode', 'description', 'type', 'free_speed_constant'])

    # Save the result to CSV
    use_group_df.to_csv(use_group_csv, index=False)
    print(f"Use group file saved to {use_group_csv}")


# Function to remove duplicate rows based on the 'A' and 'B' column
def remove_duplicate_pairs(df):
    return df.drop_duplicates(subset=['A', 'B'], keep='first')


# Function to rename link ids that have the same number but are unique 
def renumber_unique_duplicate_ids(df):
    if 'ID' not in df.columns:
        print("Error: 'ID' column not found in the DataFrame.")
        return df

    df['ID'] = pd.to_numeric(df['ID'], errors='coerce')
    max_id = df['ID'].max()
    seen_ids = set()
    new_id_map = {}

    for index, row in df.iterrows():
        link_id = row['ID']
        if link_id in seen_ids:
            max_id += 1
            new_id_map[index] = max_id
        else:
            seen_ids.add(link_id)

    df.loc[new_id_map.keys(), 'ID'] = df.loc[new_id_map.keys()].index.map(new_id_map)
    return df

# Function to process and convert DBF links to CSV
def dbflinks_to_csv(dbf_link_file, link_shp_file, output_dbf_link, network_link_dir):
    # Check if the shapefile exists
    if not os.path.exists(link_shp_file):
        print(f"Error: The file {link_shp_file} does not exist.")
        return

    # Read the DBF and shapefile
    df = read_dbf(dbf_link_file)
    shapefile = gpd.read_file(link_shp_file)

    # Read the output_links.dbf file and merge FFSPEED column based on A and B
    output_df = read_dbf(output_dbf_link)[['A', 'B', 'FFSPEED']]
    output_df.rename(columns={'FFSPEED': 'free_speed'}, inplace=True)

    # Merge the free_speed column into df based on A and B
    df = pd.merge(df, output_df, on=['A', 'B'], how='left')

    # Fill missing values with 25
    df['free_speed'] = df['free_speed'].fillna(25)
    df.loc[df['free_speed'] == 0, 'free_speed'] = 25

    # Ensure both shapefile and DBF have the 'ID' column
    if {'A', 'B'}.issubset(shapefile.columns) and {'A', 'B'}.issubset(df.columns):
        # Select only the 'A', 'B', and 'geometry' columns from the shapefile
        shapefile_geometry = shapefile[['A', 'B', 'geometry']]

        # Merge shapefile GeoDataFrame and DBF DataFrame based on 'A' and 'B'
        merged = pd.merge(df, shapefile_geometry, on=['A', 'B'], how='left')

        # Remove duplicates
        merged = remove_duplicate_pairs(merged)
        
        # Renumber duplicate link IDs that are acutally unique
        merged = renumber_unique_duplicate_ids(merged)

        # Log after duplicates are removed
        print(f"After duplicate removal, {len(merged)} rows remain.")

        # Ensure the 'FACTYPE' column is in integer format before applying conversion
        merged['FACTYPE'] = merged['FACTYPE'].astype('Int64', errors='ignore')

        # Apply the factype_to_string function to the 'FACTYPE' column
        merged['FACTYPE'] = merged['FACTYPE'].apply(factype_to_string)

        # Rename columns and reorder them
        merged.rename(columns={
            'ID': 'link_id',
            'RTE_NAME': 'name',
            'A': 'from_node_id',
            'B': 'to_node_id',
            'DIR': 'directed',
            'DISTANCE': 'length',
            'FACTYPE': 'facility_type',
            'CAP_R': 'capacity',
            'LANES': 'lanes',
            'BIKE_FAC': 'bike_facility',
            'TRAFF_PHB': 'traff_phb',  # Keep these temporarily for processing
            'PED_PHB': 'ped_phb'       # Keep these temporarily for processing
        }, inplace=True)

        # Create the 'allowed_uses' column based on the TRAFF_PHB, PED_PHB, and BIKE_FAC columns
        merged = create_allowed_uses_column(merged)

        # Drop the TRAFF_PHB and PED_PHB columns after creating 'allowed_uses'
        merged.drop(columns=['traff_phb', 'ped_phb'], inplace=True)

        # List the columns to keep (those that are renamed)
        columns_to_keep = ['link_id', 'name', 'from_node_id', 'to_node_id', 
                           'directed', 'length', 'facility_type', 'capacity', 
                           'free_speed', 'lanes', 'bike_facility', 'allowed_uses', 'geometry']
        
        # Keep only the relevant columns
        merged = merged[columns_to_keep]

        # Save the merged DataFrame to CSV
        save_to_csv(merged, network_link_dir)
    else:
        print("Error: 'ID' column is missing from either the shapefile or DBF data.")


#Convert output links file to link volume CSV file
def dbfoutputs_to_csv(output_dbf_link, link_vol):
    # Read the DBF file
    dbf = Dbf5(output_dbf_link)
    df = dbf.to_dataframe()

    # Define the columns you want to keep
    new_order = ['ID', 'AAWDT', 'AM_VOL', 'MD_VOL', 'PM_VOL', 'NT_VOL', 'TOTAL_VOL']  # Replace with your desired columns

    # Drop columns that are not in the new order
    df = df[new_order]
    df.rename(columns={'ID': 'link_id', 'AM_VOL': 'mpo_vol_am', 'MD_VOL': 'mpo_vol_md', 'PM_VOL': 'mpo_vol_pm', 'NT_VOL': 'mpo_vol_nt', 'TOTAL_VOL': 'mpo_vol_total'}, inplace=True)

    # Write to CSV file
    df.to_csv(link_vol, index=False)


#Only needed if the zone_id column does not exist in your nodes files
# Function to process and convert DBF nodes to CSV
def dbfnodes_to_csv(dbf_node_file, dbf_node_csv_file):
    df = read_dbf(dbf_node_file)
    
    # Save to CSV
    save_to_csv(df, dbf_node_csv_file)


# This is only if the zone_id column does not exist in your nodes files
# Function to merge zones with nodes data
def merge_zones_with_nodes(dbf_node_csv_file, zones_csv, node_csv):
    nodes_df = pd.read_csv(dbf_node_csv_file)
    zones_df = pd.read_csv(zones_csv)
   
    # Merge based on 'ID' column and save the result
    merged_df = pd.merge(nodes_df, zones_df[['N', 'Z']], on='N', how='left')

    # Add the `is_centroid` column
    merged_df['is_centroid'] = merged_df['Z'].apply(lambda z: 1 if pd.notna(z) and float(z).is_integer() else 0)

    merged_df.rename(columns={'Z': 'zone_id', 'N': 'node_id', 'X': 'x_coord', 'Y': 'y_coord'}, inplace=True)

    # Save the result to CSV
    save_to_csv(merged_df, node_csv)


#Alternative: Use if the zone_id column does exist in you nodes file
#def dbfnodes_to_csv(dbf_file, csv_file):
    # Read the DBF file
    #dbf = Dbf5(dbf_file)
    #df = dbf.to_dataframe()

    # Define the columns you want to keep
    #new_order = [new column order]  # Replace with your desired columns

    # Drop columns that are not in the new order
    #df = df[new_order]
    #df.rename(columns={'Old_column_name': 'New_column_name'}, inplace=True)

    # Write to CSV file
    #df.to_csv(csv_file, index=False)


#Create gmns for transit from gtfs source files uses gtfs2gmns
def process_gtfs_and_access_links(gtfs_input_dir, network_dir, transit_time_period):
    if not os.path.exists(gtfs_input_dir):
        print(f"Error: The file {gtfs_input_dir} does not exist.")
        return
    
    transit_dir = f"{network_dir}/transit"
    
    print("Generating GMNS nodes and links...")
    links = gtfs2gmns.gtfs2gmns(gtfs_input_dir, transit_dir, transit_time_period)
    
    # Generate access links
    print("Generating access links...")
    access_links = generate_access_links.generate_access_link(f"{network_dir}/hwy/node.csv", f"{transit_dir}/node_transit.csv")
    
    # Combine links and access links into a single DataFrame
    combined_links = pd.concat([links, access_links], ignore_index=True)
    
    #rename the columns to match hwy and gmns standard
    combined_links.rename(columns={'id': 'link_id'}, inplace=True)
    combined_links.rename(columns={'dir_flag': 'directed'}, inplace=True)
    combined_links.rename(columns={'name': 'facility_type'}, inplace=True)
    
    # Save combined links to a CSV file
    combined_links.to_csv(f"{transit_dir}/transit_and_access_links.csv", index=False)
    print("Combined Links saved to transit_and_access_links.csv.")
    
    
# Merges the link and node files for transit network, using hyw gmns as basis.
def merge_transit_hwy(transit_dir, transit_link, transit_node, hwy_link, hwy_node):
    print("Merging transit links with network...")

    # Read the files
    transit_link_df = pd.read_csv(transit_link)
    transit_node_df = pd.read_csv(transit_node)
    hwy_link_df = pd.read_csv(hwy_link)
    hwy_node_df = pd.read_csv(hwy_node)

    # Find common columns between the hwy and transit
    link_common_columns = hwy_link_df.columns.intersection(transit_link_df.columns)
    node_common_columns = hwy_node_df.columns.intersection(transit_node_df.columns)

    # Select only the common columns from transit
    transit_link_common_df = transit_link_df[link_common_columns]
    transit_node_common_df = transit_node_df[node_common_columns]

    # Combine the two DataFrames based on the common columns
    combined_link_df = pd.concat([hwy_link_df, transit_link_common_df], ignore_index=True)
    combined_node_df = pd.concat([hwy_node_df, transit_node_common_df], ignore_index=True)

    # Ensure "zone_id" keeps empty values as smpty but converts nonempty values to integers
    if 'zone_id' in combined_node_df.columns:
        combined_node_df['zone_id'] = combined_node_df['zone_id'].apply(lambda x: int(x) if pd.notna(x) and not pd.isna(x) else "")

    # Ensure "is_centroid" is converted to integer, replacing NaN with 0
    if 'is_centroid' in combined_node_df.columns:
        combined_node_df['is_centroid'] = combined_node_df['is_centroid'].fillna(0).astype(int)

    # Save the combined DataFrame to a new CSV file
    combined_link_df.to_csv(f"{transit_dir}/link.csv", index=False)
    combined_node_df.to_csv(f"{transit_dir}/node.csv", index=False)

    print(" ")
    print(f"CSV files have been combined and saved to {transit_dir}.")


"--------------- Main Function ---------------"

def create_network (source, network_dir = 'network/my_network' ):
    """ Creates gmns network from dbf and gtfs files. 

    Args:
        source (str): file containing a 'hwy' file with dbf files for network (links.dbf, nodes.dbf, links_shape.shp, output_links.dbf, nodes_from_cube.dbf )
                        and a 'transit' file containing gtfs standard .txt files
        network_dir (str): directory for saved network, split into two files labled "hwy" and "transit". If none given, creates directory titled 'network'
    """
# hwy and Transit Source Files
    
    # Network directory files
    hwy_src = f"{source}/hwy"
    nt_hwy_dir = f"{network_dir}/hwy"
    tran_src = f"{source}/transit"
    nt_transit_dir = f"{network_dir}/transit"
    
    try:
        # Create network directory is none exists. 
        if not os.path.exists(network_dir):
            print(f"Creating network directory: {network_dir}")
            os.makedirs(os.path.join(network_dir, 'hwy'))
            os.makedirs(os.path.join(network_dir, 'transit'))
            
        # Convert links DBF to CSV
        print(" ")
        dbflinks_to_csv(f"{hwy_src}/links.dbf", f"{hwy_src}/links_shape.shp", f"{hwy_src}/output_links.dbf", f"{nt_hwy_dir}/link.csv")
        print(f"Converted links 'links.dbf' to link.csv successfully.")

        dbfoutputs_to_csv(f"{hwy_src}/output_links.dbf", f"{nt_hwy_dir}/links_vol.csv")
        print("Converted links 'outputs_links.dbf' to 'links_vol.csv' successfully.")
       
        # Convert nodes DBF to CSV
        dbfnodes_to_csv(f"{hwy_src}/nodes_from_cube.dbf", f"{hwy_src}/nodes_from_cube.csv")
        print("Converted nodes 'nodes_from_cube.dbf' to 'nodes_from_cube.csv' successfully.")

        # Create use_group CSV
        create_use_group_file(f"{nt_hwy_dir}/link.csv", f"{network_dir}/use_group.csv") # Duplicate and move into both hwy and transit?
        
        #Only need if zone_id column did not previously exist in your nodes files
        # Merge zones with nodes
        merge_zones_with_nodes(f"{hwy_src}/nodes_from_cube.csv", f"{nt_hwy_dir}/zones.csv", f"{nt_hwy_dir}/node.csv")
        print(f"Merged zones data into 'nodes_from_cube.csv' and saved to node.csv.")
        print(" ")
        
        
        #Create transit link and node files, and add them to the link and node file. 
        process_gtfs_and_access_links(tran_src, 
                                      network_dir, 
                                      transit_time_period = '0000_2359')
        
        merge_transit_hwy(transit_dir = nt_transit_dir,
                          transit_link = f"{nt_transit_dir}/transit_and_access_links.csv" ,
                          transit_node = f"{nt_transit_dir}/node_transit.csv",
                          hwy_link = f"{nt_hwy_dir}/link.csv",
                          hwy_node = f"{nt_hwy_dir}/node.csv" )
        
    except Exception as e:
        print(f"An error occurred: {e}")
    

 
if __name__ == "__main__":
    source = 'src/roanoke'
    #hwy_src = 'hwy/src'
    #tran_src ='transit/src'
    network_dir = 'network/Roanoke'
    
    #Create gmns network using above sources.
    create_network(source,network_dir )
    
    
    
    
    
    

