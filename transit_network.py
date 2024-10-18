from gtfs2gmns import GTFS2GMNS

if __name__ == '__main__':
    gtfs_input_dir = '/Users/willicon/Desktop/roanoke_benchmark/gtfs'  # Update this path
    gtfs_output_dir = '/Users/willicon/Desktop/roanoke_benchmark/transit'  # Update this path
    time_period = "00:00:00_23:59:59"  # Adjust as needed
    date_period = ("2024-10-10")  # Adjust as needed

    # Create an instance of GTFS2GMNS
    gg = GTFS2GMNS(gtfs_input_dir, time_period, date_period, gtfs_output_dir="", isSaveToCSV=True)
    print(gg)
    print(f"Reading gtfs file from '{gtfs_input_dir}'")
    
    
    

