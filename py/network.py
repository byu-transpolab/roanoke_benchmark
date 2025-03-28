import pandas as pd
from simpledbf import Dbf5
import geopandas as gpd
import os

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
        if 'ped_phb' in row and row['ped_phb'] == 'Y':
            use_parts.append('b')
        
        # Join the parts into a string and assign it to the allowed_uses list
        allowed_uses_value = ''.join(use_parts)
        
        # If no uses were added, assign 'cwbt'
        if not allowed_uses_value:
            allowed_uses_value = 'cpb' #We don't need t to be a part. That is handled separately.
        
        allowed_uses.append(allowed_uses_value)
    
    # Assign the list as a new 'allowed_uses' column in the DataFrame
    df['allowed_uses'] = allowed_uses
    return df

# Function to create use group file based off the modes given in allowed uses. 
def create_use_group_file(csv_file, output_csv):
    df = pd.read_csv(csv_file)
    
    if 'allowed_uses' not in df.columns:
        print("Error: 'allowed_uses' column not found in the input file.")
        return
    
    # Extract unique allowed uses
    unique_uses = df['allowed_uses'].unique()
    
    # Define valid modes and their descriptions
    mode_info = {
        "c": ("car", "AUTO"),
        "p": ("pedestrian", "AUX_TRANSIT"),
        "b": ("bike", "AUX_TRANSIT"),
        #"t": ("transit", "TRANSIT") Unneeded? Transit link and nodes are seperate. 
    }
    
    # Extract unique modes by checking if c, p, b, or t appears in allowed_uses
    unique_modes = set()
    for uses in df['allowed_uses'].dropna().astype(str):
        for char in uses:  # Iterate over each character
            if char in mode_info:
                unique_modes.add((char, mode_info[char][0], mode_info[char][1]))
            else:
                unique_modes.add((char, "unknown type", "aux. transit"))

    # Create a DataFrame with mode, description, and type
    use_group_df = pd.DataFrame(unique_modes, columns=['mode', 'description', 'type'])

    # Save the result to CSV
    use_group_df.to_csv(output_csv, index=False)
    print(f"Use group file saved to {output_csv}")


# Function to remove duplicate rows based on the 'A' and 'B' column
def remove_duplicate_pairs(df):
    return df.drop_duplicates(subset=['A', 'B'], keep='first')

# Function to rename link ids that have the same number but are unique 
def renumber_duplicate_ids(df):
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
def dbflinks_to_csv(dbf_file, shp_file, output_dbf_file, csv_file):
    # Check if the shapefile exists
    if not os.path.exists(shp_file):
        print(f"Error: The file {shp_file} does not exist.")
        return

    # Read the DBF and shapefile
    df = read_dbf(dbf_file)
    shapefile = gpd.read_file(shp_file)

    # Read the output_links.dbf file and merge FFSPEED column based on A and B
    output_df = read_dbf(output_dbf_file)[['A', 'B', 'FFSPEED']]
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
            'FACTYPE': 'link_type_name',
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
                           'directed', 'length', 'link_type_name', 'capacity', 
                           'free_speed', 'lanes', 'bike_facility', 'allowed_uses', 'geometry']
        
        # Keep only the relevant columns
        merged = merged[columns_to_keep]

        # Save the merged DataFrame to CSV
        save_to_csv(merged, csv_file)
    else:
        print("Error: 'ID' column is missing from either the shapefile or DBF data.")


#Convert output links file to link volume CSV file
def dbfoutputs_to_csv(dbf_file, csv_file):
    # Read the DBF file
    dbf = Dbf5(dbf_file)
    df = dbf.to_dataframe()

    # Define the columns you want to keep
    new_order = ['ID', 'AAWDT', 'AM_VOL', 'MD_VOL', 'PM_VOL', 'NT_VOL', 'TOTAL_VOL']  # Replace with your desired columns

    # Drop columns that are not in the new order
    df = df[new_order]
    df.rename(columns={'ID': 'link_id', 'AM_VOL': 'mpo_vol_am', 'MD_VOL': 'mpo_vol_md', 'PM_VOL': 'mpo_vol_pm', 'NT_VOL': 'mpo_vol_nt', 'TOTAL_VOL': 'mpo_vol_total'}, inplace=True)


    # Write to CSV file
    df.to_csv(csv_file, index=False)



#Only needed if the zone_id column does not exist in your nodes files
# Function to process and convert DBF nodes to CSV
def dbfnodes_to_csv(dbf_file, csv_file):
    df = read_dbf(dbf_file)
    # Rename columns for clarity
   
    # Save to CSV
    save_to_csv(df, csv_file)


# This is only if the zone_id column does not exist in your nodes files
# Function to merge zones with nodes data
def merge_zones_with_nodes(nodes_csv, zones_csv, output_csv):
    nodes_df = pd.read_csv(nodes_csv)
    zones_df = pd.read_csv(zones_csv)
   
    # Merge based on 'ID' column and save the result
    merged_df = pd.merge(nodes_df, zones_df[['N', 'Z']], on='N', how='left')

    # Add the `is_centroid` column
    merged_df['is_centroid'] = merged_df['Z'].apply(lambda z: 1 if pd.notna(z) and float(z).is_integer() else 0)

    merged_df.rename(columns={'Z': 'zone_id', 'N': 'node_id', 'X': 'x_coord', 'Y': 'y_coord'}, inplace=True)

    # Save the result to CSV
    save_to_csv(merged_df, output_csv)

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

 
if __name__ == "__main__":
    try:
        # Convert links DBF to CSV
        dbflinks_to_csv('hwy/src/links.dbf', 'hwy/src/links_shape.shp', 'hwy/src/output_links.dbf', 'hwy/link.csv')
        print("Converted links 'links.dbf' to 'link.csv' successfully.")

        dbfoutputs_to_csv('hwy/src/output_links.dbf', 'hwy/links_vol.csv')
        print("Converted links 'outputs_links.dbf' to 'links_vol.csv' successfully.")
       
        # Convert nodes DBF to CSV
        dbfnodes_to_csv('hwy/src/nodes_from_cube.dbf', 'hwy/src/nodes_from_cube.csv')
        print("Converted nodes 'nodes_from_cube.dbf' to 'nodes_from_cube.csv' successfully.")

        # Create use_group CSV
        create_use_group_file('hwy/link.csv', 'hwy/use_group.csv')
        
        #Only need if zone_id column did not previously exist in your nodes files
        # Merge zones with nodes
        merge_zones_with_nodes('hwy/src/nodes_from_cube.csv', 'hwy/zones.csv', 'hwy/node.csv')
        print("Merged zones data into 'nodes_from_cube.csv' and saved to 'nodes.csv'.")
   
    except Exception as e:
        print(f"An error occurred: {e}")

