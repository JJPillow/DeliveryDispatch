# Jennifer Pillow pillje@hotmail.com

class Location:
    """
    A class used to represent delivery locations as graph vertices.

    Attributes
    ----------
    name : str
        the name of the location
    address : str
        the street address of the location
    zipcode : str
        the zipcode of the location
    distance: float
        the distance to the start location (for use with shortest path algorithm)
    pred_loc : Location
        a pointer to previous location (for graph travelling algorithm)

    Methods
    --------
    __repr__()
        Returns a formatted string showing the street address of the location.
    """

    def __init__(self, name, address, zipcode):
        """
        Constructor for the Location class.

        :param name: the name of the location
        :type name: str
        :param address: the street address of the location
        :type address: str
        :param zipcode: the zipcode of the location
        :type zipcode: str
        """
        self.name = name
        self.address = address
        self.zipcode = zipcode
        self.distance = float("inf")    # distance to start location
        self.pred_loc = None

    def __repr__(self):
        """
        Returns a formatted string showing the street address of the location.

        :return: a formatted string showing the street address of the location
        :rtype: str
        """
        return "{}".format(self.address)


# Weighted graph of distances between delivery locations
class Graph:
    """
    A class for representing a weighted graph of distances between delivery locations.

    Attributes
    ----------
    adj_list : dict
        a dictionary to hold the adjacency lists for each location
    distance : dict
        a dictionary that holds the distances for each pair of locations in the adjacency list

    Methods
    ---------
    add_location(new_location)
        Adds a new location to the adjacency list.
    add_distance(location1, location2, distance)
        Adds a weighted, undirected route to the graph
    print_dist()
        Displays a formatted list of all routes in the graph and their distances.
    search_location(address)
        Searches the list of locations by address
    """

    def __init__(self):
        """
        Constructor for the Graph class.
        """
        self.adj_list = {}
        self.distance = {}

    def add_location(self, new_location):
        """
        Adds a new location to the adjacency list

        :param new_location: the location to add to the adjacency list
        :type new_location: Location
        """
        self.adj_list[new_location] = []

    def add_distance(self, location1, location2, distance):
        """
        Adds a weighted, undirected route as an edge to the graph.

        :param location1: the location at one end of the route
        :type location1: Location
        :param location2: the location at the other end of the route
        :type location2: Location
        :param distance: the distance between the two locations
        :type distance: float
        """
        # Add distance from location1 to location2
        self.distance[(location1, location2)] = distance
        self.adj_list[location1].append(location2)

        # Add distance from location2 to location1
        self.distance[(location2, location1)] = distance
        self.adj_list[location2].append(location1)

    def print_dist(self):
        """
        Displays a formatted list of all routes in the graph and their distances.
        """
        for route in self.distance:
            dist = self.distance[(route[0], route[1])]
            print(route[0], '->', route[1], ' distance: ', dist)

    def search_location(self, address):
        """
        Searches the list of locations by address, returns a None-type object if not found

        :param address: the address of the location to search for
        :type address: str
        :return: the location that corresponds to the address or a None-type object if not found
        :rtype: Location
        """
        for location in self.adj_list:
            if location.address == address:
                return location
        return None


def dijkstra_shortest_path(graph, start_loc):
    """
    Applies Dijkstra's shortest path algorithm to the graph, updates distance values
    if shorter path from the start location to a location  is found.

    :param graph: graph of the distances between locations
    :type graph: Graph
    :param start_loc: the location in the graph to start travelling the graph
    :type start_loc: Location
    """
    # put all locations in unvisited queue
    unvisited_queue = []
    for curr_loc in graph.adj_list:
        unvisited_queue.append(curr_loc)

    start_loc.distance = 0  # start location -> start location : 0 distance

    # Visit each location, then remove it from unvisited queue
    while len(unvisited_queue) > 0:
        # visit location at min distance
        sm_index = 0
        for i in range(1, len(unvisited_queue)):
            if unvisited_queue[i].distance < unvisited_queue[sm_index].distance:
                sm_index = i    # update sm_index with index of smallest distance
        curr_loc = unvisited_queue.pop(sm_index)  # travel to shortest dist location

        # check path lengths at new location
        for adj_loc in graph.adj_list[curr_loc]:
            dist = graph.distance[(curr_loc, adj_loc)]
            alt_path_dist = curr_loc.distance + dist

            if alt_path_dist < adj_loc.distance:    # check distance from start location to adjacent location
                # print("Changing path distance: ", start_loc, "->", adj_loc, " to ", alt_path_dist)
                graph.distance[(start_loc, adj_loc)] = alt_path_dist  # update values in distance graph
                graph.distance[(adj_loc, start_loc)] = alt_path_dist  # update reverse values in distance graph
                adj_loc.distance = alt_path_dist    # update distance to adjacent location
                adj_loc.pred_loc = curr_loc         # update predecessor for adjacent location
