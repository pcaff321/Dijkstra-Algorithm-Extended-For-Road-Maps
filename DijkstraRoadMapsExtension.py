class Element:

    def __init__(self, k, v, i):
        self.key = k
        self.value = v
        self.index = i

    def __eq__(self, other):
        return self.key == other.key

    def __lt__(self, other):
        return self.key < other.key

    def __gt__(self, other):
        return self.key > other.key

    def _wipe(self):
        self.key = None
        self.value = None
        self.index = None

    def __str__(self):
        return str(self.value)


class AdaptablePriorityQueue:

    def __init__(self):
        self.APQ = list()

    def empty(self):
        return len(self.APQ) == 0

    def add(self, key, item):
        el = Element(key, item, len(self.APQ))
        self.APQ.append(el)
        self.bubble_up(el)
        return el

    def get_key(self, el):
        if el:
            return el.key
        return None

    def bubble_up(self, el):
        el_pos = el.index
        parent_pos = (el_pos-1) // 2
        if parent_pos < 0:
            parent_pos = 0
        parent = self.APQ[parent_pos]
        if parent.key > el.key:
            parent.index = el_pos
            el.index = parent_pos
            self.APQ[el_pos] = parent
            self.APQ[parent_pos] = el
            self.bubble_up(el)

    def min_child(self, el):
        el_pos = el.index
        left_child_pos = (el_pos * 2) + 1
        right_child_pos = (el_pos * 2) + 2
        if (len(self.APQ) - 1) < left_child_pos:
            return None
        lowest_child = self.APQ[left_child_pos]
        if (len(self.APQ) - 1) >= right_child_pos:
            if self.APQ[right_child_pos] < self.APQ[left_child_pos]:
                lowest_child = self.APQ[right_child_pos]
        return lowest_child

    def bubble_down(self, el):
        el_pos = el.index
        lowest_child = self.min_child(el)
        if lowest_child is not None and lowest_child < el:
            child_pos = lowest_child.index
            lowest_child.index = el_pos
            el.index = child_pos
            self.APQ[el_pos] = lowest_child
            self.APQ[child_pos] = el
            self.bubble_down(el)

    def min(self):
        return self.APQ[0]

    def update_key(self, el, newkey):
        el.key = newkey
        el_pos = el.index
        parent_pos = (el_pos-1) // 2
        if parent_pos < 0:
            parent_pos = 0
        parent = self.APQ[(el_pos-1) // 2]
        if parent > el:
            self.bubble_up(el)
        else:
            self.bubble_down(el)

    def remove_min(self):
        if len(self.APQ) > 0:
            end = self.APQ[-1]
            the_min = self.min()
            end_pos = end.index
            end.index = 0
            self.APQ[0] = end
            self.APQ.pop()  # no need to complete swap as it is being removed anyways
            if len(self.APQ) > 0:
                self.bubble_down(self.APQ[0])
            val, key = the_min.value, the_min.key
            the_min._wipe()
            return val, key

    def __str__(self):
        return str(self.APQ)

    def print_struct(self):
        for i in self.APQ:
            print(i, i.index)


class Vertex:
    """ A Vertex in a graph. """

    def __init__(self, element):
        """ Create a vertex, with a data element.

        Args:
            element - the data or label to be associated with the vertex
        """
        self._element = element

    def __str__(self):
        """ Return a string representation of the vertex. """
        return str(self._element)

    def __lt__(self, v):
        """ Return true if this element is less than v's element.

        Args:
            v - a vertex object
        """
        return self._element < v.element()

    def element(self):
        """ Return the data for the vertex. """
        return self._element

class Edge:
    """ An edge in a graph.

        Implemented with an order, so can be used for directed or undirected
        graphs. Methods are provided for both. It is the job of the Graph class
        to handle them as directed or undirected.
    """

    def __init__(self, v, w, element):
        """ Create an edge between vertices v and w, with a data element.

        Element can be an arbitrarily complex structure.

        Args:
            element - the data or label to be associated with the edge.
        """
        self._vertices = (v, w)
        self._element = element

    def __str__(self):
        """ Return a string representation of this edge. """
        return ('(' + str(self._vertices[0]) + '--'
                + str(self._vertices[1]) + ' : '
                + str(self._element) + ')')

    def vertices(self):
        """ Return an ordered pair of the vertices of this edge. """
        return self._vertices

    def start(self):
        """ Return the first vertex in the ordered pair. """
        return self._vertices[0]

    def end(self):
        """ Return the second vertex in the ordered pair. """
        return self._vertices[1]

    def opposite(self, v):
        """ Return the opposite vertex to v in this edge.

        Args:
            v - a vertex object
        """
        if self._vertices[0] == v:
            return self._vertices[1]
        elif self._vertices[1] == v:
            return self._vertices[0]
        else:
            return None

    def element(self):
        """ Return the data element for this edge. """
        return self._element


class Graph:

    def __init__(self):
        """ Create an initial empty graph. """
        self._structure = dict()

    def __str__(self):
        """ Return a string representation of the graph. """
        hstr = ('|V| = ' + str(self.num_vertices())
                + '; |E| = ' + str(self.num_edges()))
        vstr = '\nVertices: '
        for v in self._structure:
            vstr += str(v) + '-'
        edges = self.edges()
        estr = '\nEdges: '
        for e in edges:
            estr += str(e) + ' '
        return hstr + vstr + estr

    # -----------------------------------------------------------------------#

    # ADT methods to query the graph

    def depthfirstsearch(self, v):
        marked = {v:None}
        self._depthfirstsearch(v, marked)
        return marked

    def _depthfirstsearch(self, v, marked):
        for e in self.get_edges(v):
            w = e.opposite(v)
            if w not in marked:
                marked[w] = e
                self._depthfirstsearch(w, marked)


    def breadthfirstsearch(self, v):
        marked = {v:None}
        levels = [[v]]
        self._breadthfirstsearch(marked, levels, 0)
        return marked

    def _breadthfirstsearch(self, marked, levels, level):
        new_level = level + 1
        new_list = list()
        for v in levels[level]:
            for e in self.get_edges(v):
                w = e.opposite(v)
                if w not in marked:
                    marked[w] = e
                    new_list.append(w)
        if len(new_list) > 0:
            levels.append(new_list)
            self._breadthfirstsearch(marked, levels, new_level)

    def num_vertices(self):
        """ Return the number of vertices in the graph. """
        return len(self._structure)

    def dijkstra(self, s):
        APQ = AdaptablePriorityQueue()  # 'open'
        locs = dict()
        closed = dict()
        preds = {s: None}
        locs[s] = APQ.add(0, s)

        while not APQ.empty():
            v, v_key = APQ.remove_min()
            v_el = locs.pop(v)
            predecessor = preds.pop(v)
            closed[v] = (v_key, predecessor)
            for e in self.get_edges(v):
                w = e.opposite(v)
                if w not in closed:
                    new_cost = v_key + e.element()
                    if w not in locs:
                        preds[w] = v
                        locs[w] = APQ.add(new_cost, w)
                    elif APQ.get_key(locs[w]) > new_cost:
                        preds[w] = v
                        APQ.update_key(locs[w], new_cost)
        return closed

    def print_paths(self, d_dict):
        for i in d_dict.keys():
            vertex = str(i)
            vals = d_dict[i]
            cost = str(vals[0])
            preceding = str(vals[1])
            print("Vertex: " + vertex + "; Cost: " + cost + "; Preceding Vertex: " + preceding)

    def num_edges(self):
        """ Return the number of edges in the graph. """
        num = 0
        for v in self._structure:
            num += len(self._structure[v])  # the dict of edges for v
        return num // 2  # divide by 2, since each edege appears in the
        # vertex list for both of its vertices

    def vertices(self):
        """ Return a list of all vertices in the graph. """
        return [key for key in self._structure]

    def get_vertex_by_label(self, element):
        """ Return the first vertex that matches element. """
        for v in self._structure:
            if v.element() == element:
                return v
        return None

    def edges(self):
        """ Return a list of all edges in the graph. """
        edgelist = []
        for v in self._structure:
            for w in self._structure[v]:
                # to avoid duplicates, only return if v is the first vertex
                if self._structure[v][w].start() == v:
                    edgelist.append(self._structure[v][w])
        return edgelist

    def get_edges(self, v):
        """ Return a list of all edges incident on v.

        Args:
            v - a vertex object
        """
        if v in self._structure:
            edgelist = []
            for w in self._structure[v]:
                edgelist.append(self._structure[v][w])
            return edgelist
        return None

    def get_edge(self, v, w):
        """ Return the edge between v and w, or None.

        Args:
            v - a vertex object
            w - a vertex object
        """
        if (self._structure is not None
                and v in self._structure
                and w in self._structure[v]):
            return self._structure[v][w]
        return None

    def degree(self, v):
        """ Return the degree of vertex v.

        Args:
            v - a vertex object
        """
        return len(self._structure[v])

    # ----------------------------------------------------------------------#

    # ADT methods to modify the graph

    def add_vertex(self, element):
        """ Add a new vertex with data element.

        If there is already a vertex with the same data element,
        this will create another vertex instance.
        """
        v = Vertex(element)
        self._structure[v] = dict()
        return v

    def add_vertex_if_new(self, element):
        """ Add and return a vertex with element, if not already in graph.

        Checks for equality between the elements. If there is special
        meaning to parts of the element (e.g. element is a tuple, with an
        'id' in cell 0), then this method may create multiple vertices with
        the same 'id' if any other parts of element are different.

        To ensure vertices are unique for individual parts of element,
        separate methods need to be written.

        """
        for v in self._structure:
            if v.element() == element:
                return v
        return self.add_vertex(element)

    def add_edge(self, v, w, element):
        """ Add and return an edge between two vertices v and w, with  element.

        If either v or w are not vertices in the graph, does not add, and
        returns None.

        If an edge already exists between v and w, this will
        replace the previous edge.

        Args:
            v - a vertex object
            w - a vertex object
            element - a label
        """
        if v not in self._structure or w not in self._structure:
            return None
        e = Edge(v, w, element)
        self._structure[v][w] = e
        self._structure[w][v] = e
        return e

    def add_edge_pairs(self, elist):
        """ add all vertex pairs in elist as edges with empty elements.

        Args:
            elist - a list of pairs of vertex objects
        """
        for (v, w) in elist:
            self.add_edge(v, w, None)

    # ---------------------------------------------------------------------#

    # Additional methods to explore the graph

    def highestdegreevertex(self):
        """ Return the vertex with highest degree. """
        hd = -1
        hdv = None
        for v in self._structure:
            if self.degree(v) > hd:
                hd = self.degree(v)
                hdv = v
        return hdv

    def BFS_logged(self, v):
        marked = {v: None}
        levels = [[v]]
        self._BFS_logged(marked, levels, 0)
        return marked

    def _BFS_logged(self, marked, levels, level):
        new_level = level + 1
        new_list = list()
        for v in levels[level]:
            for e in self.get_edges(v):
                w = e.opposite(v)
                if w not in marked:
                    marked[w] = [e, new_level]
                    new_list.append(w)
        if len(new_list) > 0:
            levels.append(new_list)
            self._BFS_logged(marked, levels, new_level)

    def total_steps(self, v):
        log = self.BFS_logged(v)
        steps = 0
        for i in log.items():
            if i[1] is not None:
                steps += i[1][1]
        return steps

    def furthest_v(self, v):
        log = self.BFS_logged(v)
        furthest = None
        dist = -1
        for i in log.items():
            v1 = i[0]
            if i[1] is not None:
                if furthest is None or i[1][1] > dist:
                    furthest = v1
                    dist = i[1][1]
        return furthest, dist

    def path_length(self, v1, v2):
        marked = {v1: None}
        levels = [[v1]]
        found, length = self._path_length(marked, levels, 0, v2)
        return found, length

    def _path_length(self, marked, levels, level, v2):
        new_level = level + 1
        new_list = list()
        found, length = False, 0
        for v in levels[level]:
            if v == v2:
                return True, level
            for e in self.get_edges(v):
                w = e.opposite(v)
                if w not in marked:
                    marked[w] = e
                    new_list.append(w)
        if len(new_list) > 0 and found is False:
            levels.append(new_list)
            found, length = self._path_length(marked, levels, new_level, v2)
        return found, length

    def central_vertex(self):
        fewest = 0  # fewest steps
        v = None  # list of vertices that have shortest paths to furthest vertex
        for i in self._structure:
            furthest = self.furthest_v(i)
            steps = furthest[1]
            if v is None or steps < fewest:
                fewest = steps
                v = [i]
            elif steps == fewest:
                v.append(i)
        return fewest, v


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



def routereader(filename):
    """ Read and return the route map in filename. """
    graph = RouteMap()
    file = open(filename, 'r')
    entry = file.readline() #either 'Node' or 'Edge'
    num = 0
    while entry == 'Node\n':
        num += 1
        nodeid = int(file.readline().split()[1])
        next_line = file.readline().split()
        lat = float(next_line[1])
        long = float(next_line[2])
        vertex = graph.add_vertex(nodeid, lat, long)
        entry = file.readline() #either 'Node' or 'Edge'
    print('Read', num, 'vertices and added into the graph')
    num = 0
    while entry == 'Edge\n':
        num += 1
        source = int(file.readline().split()[1])
        sv = graph.get_vertex_by_label(source)
        target = int(file.readline().split()[1])
        tv = graph.get_vertex_by_label(target)
        length = float(file.readline().split()[1])
        time = float(file.readline().split()[1])
        edge = graph.add_edge(sv, tv, time)
        file.readline() #read the one-way data
        entry = file.readline() #either 'Node' or 'Edge'
    print('Read', num, 'edges and added into the graph')
    print(graph)
    return graph

def graphreader(filename):
    """ Read and return the route map in filename. """
    graph = Graph()
    file = open(filename, 'r')
    entry = file.readline() #either 'Node' or 'Edge'
    num = 0
    while entry == 'Node\n':
        num += 1
        nodeid = int(file.readline().split()[1])
        vertex = graph.add_vertex(nodeid)
        entry = file.readline() #either 'Node' or 'Edge'
    print('Read', num, 'vertices and added into the graph')
    num = 0
    while entry == 'Edge\n':
        num += 1
        source = int(file.readline().split()[1])
        sv = graph.get_vertex_by_label(source)
        target = int(file.readline().split()[1])
        tv = graph.get_vertex_by_label(target)
        length = float(file.readline().split()[1])
        edge = graph.add_edge(sv, tv, length)
        file.readline() #read the one-way data
        entry = file.readline() #either 'Node' or 'Edge'
    print('Read', num, 'edges and added into the graph')
    print(graph)
    return graph


def simpletest():
    graph = Graph()
    a = graph.add_vertex('a')
    b = graph.add_vertex('b')
    c = graph.add_vertex('c')
    d = graph.add_vertex('d')
    e = graph.add_vertex('e')
    eab = graph.add_edge(a, b, 2)
    ebc = graph.add_edge(b, c, 9)
    ecd = graph.add_edge(c, d, 7)
    ede = graph.add_edge(d, e, 4)
    eae = graph.add_edge(a, e, 14)

    ans = graph.dijkstra(a, e)
    graph.print_paths(ans)


def simpletest_routes():
    graph = RouteMap()
    a = graph.add_vertex('a', 69, 69)
    b = graph.add_vertex('b', 69, 69)
    c = graph.add_vertex('c', 69, 69)
    d = graph.add_vertex('d', 69, 69)
    e = graph.add_vertex('e', 69, 69)
    eab = graph.add_edge(a, b, 2)
    ebc = graph.add_edge(b, c, 9)
    ecd = graph.add_edge(c, d, 7)
    ede = graph.add_edge(d, e, 4)
    eae = graph.add_edge(a, e, 25)

    ans = graph.sp(a, e)



def corkCityRead():
    routemap = routereader('corkCityData.txt')
    # start = routemap.get_vertex_by_label(1669466540)
    # target = routemap.get_vertex_by_label(1147697924)
    # routemap.sp(start, target)

    ids = {}
    ids['wgb'] = 1669466540
    ids['turnerscross'] = 348809726
    ids['neptune'] = 1147697924
    ids['cuh'] = 860206013
    ids['oldoak'] = 358357
    ids['gaol'] = 3777201945
    ids['mahonpoint'] = 330068634
    sourcestr = 'neptune'
    deststr = 'wgb'
    source = routemap.get_vertex_by_label(ids[sourcestr])
    dest = routemap.get_vertex_by_label(ids[deststr])
    dijkstra_dict = routemap.dijkstra(source)
    routemap.print_paths(dijkstra_dict)  # Delete to reduce output lines
    routemap.sp(source, dest, dijkstra_dict)



corkCityRead()


# PLEASE NOTE: The method to print the shortests paths returned from the dijkstra method is print_paths(dict).
# (Example: graph.print_paths(Returned_Dict_From_Dijkstra))
# For big graphs such as the CorkCity map, you can delete this line to prevent it printing out so many lines

#  An additional third argument can be given to sp if the dijsktra dict has already been generated also, but it's okay
#  if this isn't supplied

