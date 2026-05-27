import os
import json
import matplotlib.pyplot as plt


file_path = os.path.dirname(__file__)
INPUT_FILE = f"{file_path}/../data/tmp.json"


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

if __name__ == "__main__":
    with open(INPUT_FILE, "r") as f:
        database_data = json.load(f)
        
    for (i, bus) in enumerate(database_data):
        plt.figure(figsize=(8, 4))
        bus = dict(bus)
        delays = bus["delays"]
        data_to_plot = {"xdata":[], "ydata":[]}
        for delay in delays:
            data_to_plot["xdata"].append(delay["lastSequenceDetection"])
            data_to_plot["ydata"].append(delay["delay"])
        data_to_plot = sort_dict(data_to_plot)
        plt.plot(data_to_plot["xdata"], data_to_plot["ydata"], label=f"{bus["routeShortName"]} ({bus["tripid"]})")
        plt.title(f"Delays of bus: {bus['routeShortName']}")
        plt.tight_layout()
        plt.savefig(f"plots/plot_{bus["tripid"]}.png")

    # plt.show()

