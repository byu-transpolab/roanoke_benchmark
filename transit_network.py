from gtfs2gmns import GTFS2GMNS

if __name__ == "__main__":
    gtfs_input_dir = r"gtfs"
    print(f"Reading gtfs file from '{gtfs_input_dir}'")
    # Explain: GMNS2GMNS is capable of reading multiple GTFS data sets
    """
	--root folder
	    -- subfolder (GTFS data of agency 1)
	    -- subfolder (GTFS data of agency 2)
	    -- subfolder (GTFS data of agency 3)
	    -- ...
	then, assign gtfs_input_foler = root folder
    """

    time_period = "00:00:00_23:59:59"
    date_period = ["2024-10-16"]

    gg = GTFS2GMNS(gtfs_input_dir, time_period, date_period, gtfs_output_dir="transit/", isSaveToCSV=True)