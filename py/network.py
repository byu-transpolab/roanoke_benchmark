import pandas as pd
from simpledbf import Dbf5
import geopandas as gpd
import os
 
 #Convert Links DBF file to CSV and merge the geometry column from the links SHP file
# Function to read a DBF file and convert it to a DataFrame
def read_dbf(dbf_file):
    dbf = Dbf5(dbf_file)
    return dbf.to_dataframe()
 
# Function to save the DataFrame to CSV
def save_to_csv(df, csv_file):
    df.to_csv(csv_file, index=False)
 
# Function to process and convert DBF links to CSV
def dbflinks_to_csv(dbf_file, shp_file, csv_file):
     # Check if the shapefile exists
    if not os.path.exists(shp_file):
        print(f"Error: The file {shp_file} does not exist.")
        return
    # Read the DBF and shapefile
    df = read_dbf(dbf_file)
    shapefile = gpd.read_file(shp_file)
 

    # Ensure both shapefile and DBF have the 'ID' column
    if 'ID' in shapefile.columns and 'ID' in df.columns:
        # Select only the 'ID' and 'geometry' columns from the shapefile
        shapefile_geometry = shapefile[['ID', 'geometry']]

        # Merge shapefile GeoDataFrame and DBF DataFrame based on 'ID'
        merged = pd.merge(df, shapefile_geometry, on='ID', how='left')

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
            'FFSPEED_R': 'free_speed',
            'LANES': 'lanes',
            'BIKE_FAC': 'bike_facility'
        }, inplace=True)
 
         # List the columns to keep (those that are renamed)
        columns_to_keep = ['link_id', 'name', 'from_node_id', 'to_node_id', 
                           'directed', 'length', 'facility_type', 'capacity', 
                           'free_speed', 'lanes', 'bike_facility', 'geometry']
        
        # Drop columns that are not in the 'columns_to_keep' list
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
    df.rename(columns={'N': 'ID', 'X': 'x_coord', 'Y': 'y_coord'}, inplace=True)
   
    # Save to CSV
    save_to_csv(df, csv_file)


# This is only if the zone_id column does not exist in your nodes files
# Function to merge zones with nodes data
def merge_zones_with_nodes(nodes_csv, zones_csv, output_csv):
    nodes_df = pd.read_csv(nodes_csv)
    zones_df = pd.read_csv(zones_csv)
   
    # Merge based on 'ID' column and save the result
    merged_df = pd.merge(nodes_df, zones_df[['ID', 'Z']], on='ID', how='left')
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
        dbflinks_to_csv('hwy/src/links.dbf', 'hwy/src/links_shape.shp', 'hwy/links.csv')
        print("Converted links 'links.dbf' to 'links.csv' successfully.")

        dbfoutputs_to_csv('hwy/src/output_links.dbf', 'hwy/links_vol.csv')
        print("Converted links 'outputs_links.dbf' to 'links_vol.csv' successfully.")
       
        # Convert nodes DBF to CSV
        dbfnodes_to_csv('hwy/src/nodes_from_cube.dbf', 'hwy/src/nodes_from_cube.csv')
        print("Converted nodes 'nodes_from_cube.dbf' to 'nodes_from_cube.csv' successfully.")
 
        #Only need if zone_id column did not previously exist in your nodes files
        # Merge zones with nodes
        merge_zones_with_nodes('hwy/src/nodes_from_cube.csv', 'se/zones.csv', 'hwy/nodes.csv')
        print("Merged zones data into 'nodes_from_cube.csv' and saved to 'nodes.csv'.")
   
    except Exception as e:
        print(f"An error occurred: {e}")





