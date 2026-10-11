class Stops:
    id:int
    name:str
    lat:float
    lon:float

    def __init__(self, id:int, name:str, lat:float, lon:float) -> None:
        self.id = id
        self.name = name
        self.lat = lat
        self.lon = lon

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "lat": self.lat,
            "lon": self.lon,
        }

