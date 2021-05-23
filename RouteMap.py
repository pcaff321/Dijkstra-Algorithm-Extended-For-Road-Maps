from Graph import *


class RouteMap(Graph):
    def __init__(self):
        super().__init__()
        self.coords = dict()
        self.vertex_objects = dict()

    def add_vertex(self, element, lat, long):
        v = super().add_vertex(element)
        self.coords[v] = (lat, long)
        self.vertex_objects[element] = v
        return v

    def add_vertex_if_new(self, element, lat, long):
        for v in self._structure:
            if v.element() == element:
                return v
        return self.add_vertex(element, lat, long)

    def coordinates(self, v):
        if v in self.coords:
            return self.coords[v]
        else:
            print("ERROR: Vertex not in RouteMap")
            return None

    def __str__(self):
        if self.num_vertices() < 100 and self.num_edges() < 100:
            return super().__str__()
        else:
            return 'Too many vertices/edges, not printing'

    def get_vertex_by_label(self, element):
        """ Return the first vertex that matches element. """
        if element in self.vertex_objects:
            return self.vertex_objects[element]
        return None

    # Added in an extra argument 'dijkstra_dict' to prevent unnecessarily running dijkstra twice.
    # If the dijsktra_dict is supplied, it won't run again, if it isn't supplied, it will run
    def sp(self, v, w, dijsktra_dict=None):
        paths = dijsktra_dict
        if paths is None:
            paths = self.dijkstra(v)
        pathing = list()
        found = False
        curr = w
        while not found:
            a = curr  # point A (starting point)
            b = paths[a][1]  # point B ( preceding A )
            curr = b
            pathing.append(a)
            if b == v:  # if point B is the starting point
                pathing.append(b)
                found = True
        pathing.reverse()
        self.print_paths_for_GPS(paths, pathing)
        return pathing

    def print_paths_for_GPS(self, d, sp):
        print("type\tlatitude\tlongitude\telement\tcost")
        for i in sp:
            coords = self.coordinates(i)
            lat = str(coords[0])
            long = str(coords[1])
            el = str(i.element())
            cost = str(d[i][0])

            print("W\t" + lat + "\t" + long + "\t" + el + "\t" + cost)
