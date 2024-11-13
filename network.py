import pandas as pd
from simpledbf import Dbf5
import geopandas as gpd

# read the link dbf to a csv and export
def dbflinks_to_csv(dbf_file, csv_file):
    # Read the DBF file
    dbf = Dbf5(dbf_file)
    df = dbf.to_dataframe()

    # Load the existing CSV file
    csv_path = 'links.csv'
    existing_df = pd.read_csv(csv_path)

    # Load the shapefile
    shapefile_path = 'links shape.shp'
    gdf = gpd.read_file(shapefile_path)

    # Select the column you want to export (replace 'your_column' with the actual column name)
    new_column = gdf[['geometry']]

    # Concatenate the new column to the existing DataFrame
    combined_df = pd.concat([existing_df, new_column], axis=1)

    # Save the combined DataFrame back to the CSV file
    combined_df.to_csv(csv_path, index=False)
    #process link information
    #process link information

    # Define the columns you want to keep
    new_order = ['ID', 'RTE_NAME', 'A', 'B', 'geometry', 'DIR', 'DISTANCE', 'FACTYPE', 'CAP_R', 'FFSPEED_R', 'LANES']  # Replace with your desired columns
    
    # Drop columns that are not in the new order
    df = df[new_order]
    df.rename(columns={'ID': 'link_id', 'RTE_NAME': 'name', 'A': 'from_node_id', 'B': 'to_node_id', 'DIR': 'directed', 'DISTANCE': 'length', 'FACTYPE': 'facility_type', 'CAP_R': 'capacity', 'FFSPEED_R': 'free_speed', 'LANES': 'lanes'}, inplace=True)
    # Save the modified DataFrame back to the same CSV file
    # Write to CSV file
    df.to_csv(csv_file, index=False)


def dbfnodes_to_csv(dbf_file, csv_file):
    # Read the DBF file
    dbf = Dbf5(dbf_file)
    df = dbf.to_dataframe()

    # Load the source and destination CSV files
    source_file = 'zones.csv'
    destination_file = 'nodes.csv'

    # Read the CSV files into DataFrames
    source_df = pd.read_csv(source_file)
    destination_df = pd.read_csv(destination_file)

    # Specify the column you want to move
    column_to_move = 'Z'  # replace with your column name

    # Check if the column exists in the source DataFrame
    if column_to_move in source_df.columns:
    # Extract the column
     column_data = source_df[column_to_move]

    # Add the column to the destination DataFrame
    destination_df[column_to_move] = column_data

    # Save the updated destination DataFrame back to CSV
    destination_df.to_csv(destination_file, index=False)
    # Step 1: Read the CSV file

    # Define the columns you want to keep
    new_order = ['N', 'X', 'Y', 'Z']  # Replace with your desired columns
    
    # Drop columns that are not in the new order
    df = df[new_order]

    # Step 2: Rename the columns
    # For example, if you want to rename 'old_name1' to 'new_name1' and 'old_name2' to 'new_name2':
    df.rename(columns={'N': 'node_id', 'X': 'x_coord', 'Y': 'y_coord', 'Z': 'zone_id'}, inplace=True)

    # Step 3: Save the modified DataFrame back to a CSV file
    df.to_csv('nodes.csv', index=False)





if __name__ == "__main__":
    
    # read in highway network and write out csv file
    input_dbf = 'highway.dbf'   # Replace with your DBF file path
    output_csv = 'links.csv'    # Replace with your desired CSV file path

    dbflinks_to_csv(input_dbf, output_csv)
    print(f"Converted links '{input_dbf}' to '{output_csv}' successfully.")


    # read in nodes and write out CSV file
    inputn_dbf = 'nodes.dbf'    # Replace with your DBF file path
    outputn_csv = 'nodes.csv'   # Replace with your desired CSV file path

    dbfnodes_to_csv(inputn_dbf, outputn_csv)
    print(f"Converted nodes '{inputn_dbf}' to '{outputn_csv}' successfully.")






