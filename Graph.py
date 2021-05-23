from Vertex import *
from Edge import *
from AdaptablePriorityQueue import *

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
