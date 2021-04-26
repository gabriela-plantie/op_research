from graphviz import Source
from abc import ABC, abstractmethod
import numpy as np

class AbstractGraph(ABC):
    
    def __init__(self):
        self._nodes = set()
        self._distances = {}
    
    def add_node(self, node):
        self._nodes.add(node)
    
    def _check_node(self, node):      
        if not self.contains_node(node):
            raise "Nodes should be added first"
        return None

    def contains_node(self, node):
        return node in self._nodes       
    
    @abstractmethod
    def add_distance(self, node_1, node_2, distance):
        pass
    @abstractmethod
    def get_distance(self, node_1, node_2):
        pass
    @abstractmethod
    def get_adjacents_nodes(self, node):
        pass
        
    @abstractmethod
    def render(self, engine):
        pass 

    
    
class UndirectedGraph(AbstractGraph):
    def __init__(self):
        self._nodes = set()
        self._distances = {}
     
    def _order_nodes(self, node_1, node_2):
        if node_1 > node_2:
            temp = node_2
            node_2 = node_1
            node_1 = temp
        return  [node_1, node_2]
    
    def add_distance(self, node_1, node_2, distance):
        self._check_node(node_1)
        self._check_node(node_2)
        [node_1, node_2] = self._order_nodes(node_1, node_2)  
        if node_1 not in self._distances:
            self._distances[node_1] = {}
        
        self._distances[node_1][node_2] = distance
        
        
    def get_distance(self, node_1, node_2):
        self._check_node(node_1)
        self._check_node(node_2)
        [node_1, node_2] = self._order_nodes(node_1, node_2)
        if node_1 not in self._distances:
            return None
        if node_2 not in self._distances[node_1]:
            return None     
        return self._distances[node_1][node_2]
 


    def get_adjacents_nodes(self, node):
        self._check_node(node)
        
        adjacents = []
        
        keys = self._distances.keys()
        keys = filter(lambda x: x < node, keys)
        
        for key in keys:
            if node in self._distances[key]:
                adjacents += [key]
        
        if node in self._distances:
            adjacent_distances = self._distances[node]
            adjacents += list(adjacent_distances.keys())
               
        return list(set(adjacents))
 

    def render(self, engine = None):
        nodes = '\n'.join(map(str, self._nodes))
        render_edge = lambda x: f"{str(x[0])} -- {str(x[1])} [label=\"{str(x[2])}\"]"
        edges = [(n1, n2, dist) for (n1, adjacents) in self._distances.items() for (n2, dist) in adjacents.items()]
        edges = '\n'.join(map(render_edge, edges))
        temp = "graph G{\n" + nodes + "\n" + edges + "\n}"
        
        return Source(temp, engine = engine)
    
    
    
    
    
    
    
class DiGraph(AbstractGraph):
    def __init__(self):
        self._nodes = set()
        self._distances = {}
            
    def add_distance(self, node_1, node_2, distance):
        self._check_node(node_1)
        self._check_node(node_2)

        if node_1 not in self._distances:
            self._distances[node_1] = {}
        
        self._distances[node_1][node_2] = distance
              
    def get_distance(self, node_1, node_2):
        self._check_node(node_1)
        self._check_node(node_2)
        
        if node_1 not in self._distances:
            return None
        if node_2 not in self._distances[node_1]:
            return None     
        return self._distances[node_1][node_2]


    def get_adjacents_nodes(self, node):
        self._check_node(node)
        adjacents = []
        if node in self._distances:
            adjacent_distances = self._distances[node]
            adjacents += list(adjacent_distances.keys())
        return list(set(adjacents))
        
    def render(self, engine = None):
        nodes = '\n'.join(map(str, self._nodes))
        render_edge = lambda x: f"{str(x[0])} -> {str(x[1])} [label=\"{str(x[2])}\"]"
        edges = [(n1, n2, dist) for (n1, adjacents) in self._distances.items() for (n2, dist) in adjacents.items()]
        edges = '\n'.join(map(render_edge, edges))
        temp = "digraph G{\n" + nodes + "\n" + edges + "\n}"
        
        return Source(temp, engine = engine)

    
    
    
    
def _update_distances(graph, adjacents, visited, distance_to_visiting, distances, previous):
    for adjacent in adjacents:
        dist = graph.get_distance(visited, adjacent) + distance_to_visiting
        if adjacent not in distances:
            distances[adjacent] = np.Inf
        if dist < distances[adjacent]:
            distances[adjacent] = dist
            previous[adjacent] = visited  
    return [distances, previous]   
    



def dijkstra(graph, origin, destiny):    
    visited = origin
    already_visited =[]
    distances = {}
    counter = 0
    distance_to_visiting = 0
    previous = {}
    

    if not graph.contains_node(origin) or not  graph.contains_node(destiny):
        return "destiny or origin don't exist"


    while (visited != destiny) and (visited != None) :
        already_visited.append(visited)
        
        #print('visited: '+ str(visited))
        adjacents = set(graph.get_adjacents_nodes(visited)).difference(already_visited)
     
        #print('adjacents: ' + str(adjacents))
        
        #update distances
        if len(adjacents) != 0:
            [distances, previous] = _update_distances(graph, adjacents, visited, distance_to_visiting, distances, previous)
            #print('distances: ' + str(distances))
            
             
        #choose next step
        min_dist = np.Inf
        visited = None
        for node in distances:
            if (distances[node] < min_dist) and (node not in already_visited):
                #print('already_visited; ' +str(already_visited))
                min_dist = distances[node]
                visited = node
                distance_to_visiting = distances[visited] ### agregue
    
    next_step = destiny
    res = [destiny]
    prev = next_step
    
    if destiny not in previous:
        return 'origin and destiny not connected'

    #gets the minimun path starting destiny
    while prev != origin:
        prev = previous[next_step]
        res.append(prev)
        next_step = prev

    sol = [ res[len(res)-i-1]  for i in range(len(res))] #reorder res
   

    return [sol, distances]

   
    
    
    