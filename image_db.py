import numpy as np
import pandas as pd
import sqlite3

#save image into sqlite
def save_img_data(values_dataframe):
    try:
        conn = sqlite3.connect("img.db")
        with conn:
            values_dataframe.to_sql('img_data', conn, if_exists='replace', index=False)
        
        conn.close()
    except Exception as e:
        return "Issue in Image store in Database"

def fetch_img_data(depth_min,depth_max):
    try:
        conn = sqlite3.connect("img.db")
        with conn:
            query = f"SELECT * FROM img_data WHERE d BETWEEN ? AND ?"
            params = (depth_min, depth_max)
            # Retrieve the data using Pandas
            filtered_df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return filtered_df
    except Exception as e:
        print("Issue with reading info from DataBase")
        return "Issue with reading info from DataBase"
    
    
def fetch_min_max_depth():
    try:
        conn = sqlite3.connect("img.db")
        with conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT MIN(d), MAX(d) FROM img_data")
            min_depth, max_depth = cursor.fetchone()

        conn.close()

        return {"min_depth": min_depth, "max_depth": max_depth}
    except Exception as e:
        return {"error": str(e)}
    