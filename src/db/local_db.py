import sqlite3
import pandas as pd
from os import listdir
from os.path import isfile, join

from db.Routes import Routes
from db.Stops import Stops

def load_trentinotrasporti_data():
    conn = sqlite3.connect(r'./data/TT_info.db')
    for f in listdir("./TT_info/"):
        if isfile(join("./TT_info/", f)):
            file = f.removesuffix(".csv")
            df = pd.read_csv('./TT_info/'+file+".csv", dtype=str, header=0)
            df.to_sql(file, conn, if_exists='replace', index=False)
    conn.close()


def get_table(table:str) -> list[tuple]:
    conn = sqlite3.connect(r'./data/TT_info.db')
    cur = conn.cursor()

    ret_val = []
    for row in cur.execute(f'SELECT * FROM {table}'):
        ret_val.append(row)
    cur.close()
    conn.close()
    return ret_val

def get_stops_for_trip(route_id:str|None) -> list[Stops]:
    if route_id == None:
        return []
    
    conn = sqlite3.connect(r'./data/TT_info.db')
    cur = conn.cursor()
    # row = cur.execute(f'SELECT route_short_name,route_long_name FROM routes WHERE route_id={route_id}').fetchone()
    row = cur.execute(f'SELECT trip_id FROM trips WHERE route_id={route_id}').fetchone()
    trip_id=row[0]
    row = cur.execute(f'SELECT stop_id FROM stop_times WHERE trip_id="{trip_id}"').fetchall()
    
    stops_info = []
    for stop in row:
        row = cur.execute(f'SELECT stop_id,stop_name,stop_lat,stop_lon FROM stops WHERE stop_id="{stop[0]}"').fetchone()
        s = Stops(int(row[0]), row[1], float(row[2]), float(row[3]))
        stops_info.append(s)
    cur.close()
    conn.close()

    return stops_info


def get_route(route_id:str|None) -> Routes|None:
    if route_id == None:
        return None
    
    conn = sqlite3.connect(r'./data/TT_info.db')
    cur = conn.cursor()
    row = cur.execute(f'SELECT route_short_name,route_long_name,route_color FROM routes WHERE route_id={route_id}').fetchone()
    shortname = row[0]
    longname = row[1]
    colour = row[2]
    stops = get_stops_for_trip(route_id)
    return Routes(shortname, longname, stops, colour)

    


if __name__ == "__main__":
    load_trentinotrasporti_data()
    # stops = get_stops_for_trip("400")
