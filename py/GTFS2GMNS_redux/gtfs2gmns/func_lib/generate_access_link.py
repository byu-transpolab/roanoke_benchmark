# -*- coding:utf-8 -*-
##############################################################
# Created Date: Sunday, February 18th 2024
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################


import pandas as pd
import numpy as np
from shapely.geometry import Point, LineString
from scipy.spatial import cKDTree
import pyufunc as uf
from pyufunc import gmns_geo

def generate_access_link(hwy_node_path: str, tran_node_path: str) -> pd.DataFrame:
    # Load highway and transit node data
    df_hwy_node = pd.read_csv(hwy_node_path, usecols=['node_id', 'x_coord', 'y_coord'])
    df_tran_node = pd.read_csv(tran_node_path, usecols=['node_id', 'x_coord', 'y_coord', 'directed_service_id', 'node_type'])

    # Filter real transit nodes (remove those with directed_service_id) & keep only "bus_service_node"
    df_tran_node_real = df_tran_node[
        
        (df_tran_node['node_type'] == "bus_service_node")
    ].copy()

    # Convert coordinates to float for safety
    df_hwy_node[['x_coord', 'y_coord']] = df_hwy_node[['x_coord', 'y_coord']].astype(float)
    df_tran_node_real[['x_coord', 'y_coord']] = df_tran_node_real[['x_coord', 'y_coord']].astype(float)

    # Convert to NumPy arrays for fast computation
    hwy_coords = df_hwy_node[['x_coord', 'y_coord']].to_numpy()
    tran_coords = df_tran_node_real[['x_coord', 'y_coord']].to_numpy()

    # If no bus service nodes are found, return empty DataFrame
    if len(tran_coords) == 0:
        return pd.DataFrame()

    # Build KDTree for highway nodes (fast nearest neighbor search)
    tree = cKDTree(hwy_coords)

    # Query each transit node to find the nearest highway node
    distances, indices = tree.query(tran_coords, distance_upper_bound=10000)

    access_links = []

    # Process each transit node (find its nearest highway node)
    for i, tran_node_id in enumerate(df_tran_node_real['node_id']):
        hwy_index = indices[i]

        # Ignore if no valid highway node was found within the radius
        if hwy_index == len(hwy_coords):
            continue

        # Get corresponding highway node data
        hwy_node_id = df_hwy_node.iloc[hwy_index]['node_id']
        tran_point = Point(tran_coords[i])
        hwy_point = Point(hwy_coords[hwy_index])

        # Calculate geodesic distance
        distance = uf.calc_distance_on_unit_sphere(tran_point, hwy_point, "mile")

        # Create access link
        access_links.append(
            gmns_geo.Link(
                id = f"{tran_node_id}", 
                name = "bus_access_link",
                from_node_id=tran_node_id,
                to_node_id=int (hwy_node_id),
                length=distance,
                lanes=1,
                dir_flag = 0,
                free_speed= 2.72727, #4 *3600 / 5280
                capacity= 0,
                allowed_uses='t',
                geometry=LineString([tran_point, hwy_point])
            )
        )

    # Convert to DataFrame
    return pd.DataFrame([link.__dict__ for link in access_links]) if access_links else pd.DataFrame()