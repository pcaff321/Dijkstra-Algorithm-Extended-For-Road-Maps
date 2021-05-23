from AdaptablePriorityQueue import *
from RouteMap import *


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

