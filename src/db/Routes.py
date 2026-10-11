from db.Stops import Stops


class Routes:
    shortname: str
    longname: str
    stops: list[Stops]
    color:str


    def __init__(self, shortname:str, longname:str, stops: list[Stops], color:str|None) -> None:
        self.shortname = shortname
        self.longname = longname
        self.stops = stops
        self.color = "#"+color if color != None else "#FD3DB5"