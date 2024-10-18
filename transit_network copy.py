from gtfs2gmns import GTFS2GMNS


gtfs_input_dir = 'gtfs'
print(f"Reading gtfs file from '{gtfs_input_dir}'")
time_period = "00:00:00_23:59:59"
print(time_period)
date_period= ("2024-10-10")
print(date_period)
gtfs_output_dir = '89780'
print(f"Reading exporting files to '{gtfs_output_dir}'")



GTFS2GMNS(gtfs_input_dir, time_period,date_period,gtfs_output_dir,isSaveToCSV = True)




