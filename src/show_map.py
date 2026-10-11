
import folium
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

from db.Stops import Stops
from db.local_db import get_route, get_table


def find_center_map(stops:list[Stops]) -> tuple[float, float]:
    return (np.average([s.lat for s in stops]),np.average([s.lon for s in stops]))

def add_stop_markers(map: folium.Map, stops:list[Stops], colour:str):
    for s in stops:        
        folium.Marker(
            location=[s.lat, s.lon],
            popup=f"{s.name} ({s.id})",
            icon = folium.Icon(icon='bus', color="gray",prefix= 'fa',icon_color=colour),
        ).add_to(map)

        
    for (s1,s2) in zip(stops, stops[1:]):
        folium.PolyLine(
                locations=[(s1.lat, s1.lon), 
                        (s2.lat, s2.lon)],
                weight=6
            ).add_to(map)


def map_component(stops: list[Stops], colour:str):
    center_map = find_center_map(stops)

    with st.container(border=True):
        map = folium.Map(location=center_map, zoom_start=15)

        # folium.Marker(
        #     location=center_map,
        #         popup=f"center of stops",
        #     icon = folium.Icon(color="red",icon='',prefix= 'fa',icon_color='white'),
        # ).add_to(map)

        add_stop_markers(map, stops, colour)  

        # Display map
        st_folium(map, width=1500)

def get_options_bus() -> list[str]:
    routes = get_table("routes")
    ret_val = []
    for route in routes:
        ret_val.append(f"{route[2]} - {route[3]} ({route[0]})")

    ret_val.sort()
    return ret_val


if __name__ == "__main__":
    st.set_page_config(page_title="Trentino Trasporti", layout="wide")

    
    trip_id = st.selectbox("Trip to look:", get_options_bus())
    routes = get_route(trip_id[-4:-1])
    if routes != None:
        stops = routes.stops

        map_component(stops, routes.color)
        

