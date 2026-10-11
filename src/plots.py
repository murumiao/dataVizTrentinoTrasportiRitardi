import os
import json
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd


file_path = os.path.dirname(__file__)
INPUT_FILE = f"{file_path}/../data/data.json"
STOP_ID_FILE = f"{file_path}/../TT_info/stops.csv"


def load_stop_id(path:str) -> pd.DataFrame:
    df = pd.read_csv(path, header=0)
    return df

def load_data(path:str) -> dict:
    if path.endswith(".json"):
        with open(path, "r") as f:
            return json.load(f)
    return {"Error": "File is not a JSON"}

def sort_dict(dict_to_sort:dict) -> dict:
    tmp = []
    for (x,y) in zip(dict_to_sort["xdata"], dict_to_sort["ydata"]):
        tmp.append((x,y))
    
    tmp = sorted(tmp, key=lambda x: x[0])
    unique_stops = list(set(dict_to_sort["xdata"]))
    unique_stops.sort()

    sums = [0 for _ in range(len(unique_stops))]
    length = [0 for _ in range(len(unique_stops))]
    averages = {"xdata":[], "ydata":[]}

    for (x,y) in tmp:
        index = unique_stops.index(x)
        sums[index] += y
        length[index] += 1

    for (i, sum) in enumerate(sums):
        averages["xdata"].append(i)
        averages["ydata"].append(sum/length[i])

    return averages

def map_id_to_stopname(stop_id:int) -> str:
    global stop_id_mapping
    correct_stop = stop_id_mapping["stop_id"] == stop_id
    stop_name = stop_id_mapping.loc[correct_stop]["stop_name"]
    if stop_name.empty:
        return "???"
    return stop_name.values[0]


def prepare_image(fig: Figure, ax:Axes, x: list, y:list, name:str):
    plt.plot(x, y, figure=fig)
    plt.title(f"Delays of bus: {name}", figure=fig)
    st.text(x)
    x_labels = [map_id_to_stopname(stop_id) for stop_id in x]
    ax.set_xticks(x)
    ax.set_xticklabels(x_labels, rotation=90, fontsize=8)
    plt.tight_layout()

if __name__ == "__main__":
    data = load_data(INPUT_FILE)
    stop_id_mapping = load_stop_id(STOP_ID_FILE)
    for (i, bus) in enumerate(data[:10]):
        fig, ax  = plt.subplots(figsize=(8, 4))
        bus = dict(bus)
        delays = bus["delays"]
        data_to_plot = {"xdata":[], "ydata":[], "x_ticks":[]}
        for delay in delays:
            data_to_plot["xdata"].append(delay["lastSequenceDetection"])
            data_to_plot["ydata"].append(delay["delay"])
        data_to_plot = sort_dict(data_to_plot)
        prepare_image(fig, ax, data_to_plot["xdata"], data_to_plot["ydata"], bus['routeShortName'])
        st.pyplot(fig)
        plt.clf()


