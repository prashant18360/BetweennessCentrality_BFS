#!/usr/bin/env python3

import re
import itertools

ROLLNUM_REGEX = "201[0-9]{4}"

class Graph(object):
    name = "Prashant"
    email = "prashant18360@iiitd.ac.in"
    roll_num = "2018360"

    def __init__ (self, vertices, edges):
        """
        Initializes object for the class Graph

        Args:
            vertices: List of integers specifying vertices in graph
            edges: List of 2-tuples specifying edges in graph
        """

        self.vertices = vertices
        
        ordered_edges = list(map(lambda x: (min(x), max(x)), edges))
        
        self.edges    = ordered_edges

        edges2   =  [(y, x) for x, y in self.edges]
        edges3 = edges + edges2
        #print(edges2,edges3)
        graph={}
        for a,b in edges3:
            try:
                graph[a].append(b)
            except KeyError:
                graph[a] = [b]
        self.graph=graph
        
        self.validate()
        

    def validate(self):
        """
        Validates if Graph if valid or not

        Raises:
            Exception if:
                - Name is empty or not a string
                - Email is empty or not a string
                - Roll Number is not in correct format
                - vertices contains duplicates
                - edges contain duplicates
                - any endpoint of an edge is not in vertices
        """

        if (not isinstance(self.name, str)) or self.name == "":
            raise Exception("Name can't be empty")

        if (not isinstance(self.email, str)) or self.email == "":
            raise Exception("Email can't be empty")

        if (not isinstance(self.roll_num, str)) or (not re.match(ROLLNUM_REGEX, self.roll_num)):
            raise Exception("Invalid roll number, roll number must be a string of form 201XXXX. Provided roll number: {}".format(self.roll_num))

        if not all([isinstance(node, int) for node in self.vertices]):
            raise Exception("All vertices should be integers")

        elif len(self.vertices) != len(set(self.vertices)):
            duplicate_vertices = set([node for node in self.vertices if self.vertices.count(node) > 1])

            raise Exception("Vertices contain duplicates.\nVertices: {}\nDuplicate vertices: {}".format(vertices, duplicate_vertices))

        edge_vertices = list(set(itertools.chain(*self.edges)))

        if not all([node in self.vertices for node in edge_vertices]):
            raise Exception("All endpoints of edges must belong in vertices")

        if len(self.edges) != len(set(self.edges)):
            duplicate_edges = set([edge for edge in self.edges if self.edges.count(edge) > 1])

            raise Exception("Edges contain duplicates.\nEdges: {}\nDuplicate vertices: {}".format(edges, duplicate_edges))




    
    
    def bfs_paths(self,start_node, end_node):
        q = [(start_node, [start_node])]
        while q:
            (v, p) = q.pop(0)
            for next in set(self.graph[v]) - set(p):
                if next == end_node:
                    yield p + [next]
                else:
                    q.append((next, p + [next]))
        return q
        '''bfs algo to find visited list'''

    def one_shortest_paths(self,start_node, end_node):
        try:
            return next(self.bfs_paths(start_node,end_node))
        except StopIteration:
            return None
        """
        Finds one shortest paths between start_node and end_node

        Args:
            start_node: Starting node for paths
            end_node: Destination node for paths

        Returns:
            A list one path, where each path is a list of integers.
        """

        #raise NotImplementedError
        
    def min_dist(self,start_node, end_node):
        dist= len(self.one_shortest_paths(start_node,end_node))
        return dist
        
        '''
        Finds minimum distance between start_node and end_node

        Args:
            start_node: Vertex to find distance from
            end_node: Vertex to find distance to

        Returns:
            An integer denoting minimum distance between start_node
            and end_node
        '''

        raise NotImplementedError


    def all_paths(self,start_node,end_node):
        dist=self.min_dist(start_node,end_node)
        paths=self.all_path1(start_node,end_node)
        path=[]
        for i in paths:
            if len(i)==dist:
                path.append(i)
        return path
        """
        Finds all paths from node to destination with length = dist

        Args:
            node: Node to find path from
            destination: Node to reach
            dist: Allowed distance of path
            path: path already traversed

        Returns:
            List of path, where each path is list ending on destination

            Returns None if there no paths
        """
        raise NotImplementedError
        
                

    def all_path1(self,start_node, end_node,path=[]):
        
        graph = self.graph
        path = path + [start_node]
        if start_node == end_node:
            return [path]
        if start_node not in graph:
            return []
        paths = []
        for node in graph[start_node]:
            if node not in path:
                ext_paths = self.all_path1(node,end_node,path)
                for p in ext_paths: 
                    paths.append(p)
        
        return paths
        ''' it give all path between two node i.e. start_node, end_node'''

        raise NotImplementedError

    def betweenness_centrality(self, node):
        graph=self.graph
        vertices=self.vertices
        u=vertices.index(node)
        f=vertices[:u]
        o=vertices[u+1:]
        c=f+o
        z=tuple(itertools.combinations(c, 2))
        x=[]
        for i in z:
            d=i[0]
            e=i[1]
            p=self.all_paths(d,e)
            #print(p)
            f=len(p)
            x.append(f)
        
        y=[]
        for i in z:
            t=i[0]
            u=i[1]
            r=self.all_paths(t,u)
            i=[]
            for h in r:
                if node in h:
                    i.append(1)
                else:
                    i.append(0)
            y.append(sum(i))

        tosum=[int(y) / int(x) for y,x in zip(y, x)]
        between=sum(tosum)
        
          

        return between
        """
        Find betweenness centrality of the given node

        Args:
            node: Node to find betweenness centrality of.

        Returns:
            Single floating point number, denoting betweenness centrality
            of the given node
        """

        raise NotImplementedError

    def top_k_betweenness_centrality(self,k):
        graph=self.graph
        vert=self.vertices
        l=[]
        for i in range(len(vert)):
            j=self.betweenness_centrality(vert[i])
            l.append(j)

        N=len(self.vertices)
        D=[((N-1)*(N-2))/2]*N
        L=[int(a)/int(b) for a,b in zip(l,D)]

        L.sort(reverse=True)
        v=[]
        for i in range(k):
            v.append(L[i])
            
        return v
        """
        Find top k nodes based on highest equal betweenness centrality.

        
        Returns:
            List a integer, denoting top k nodes based on betweenness
            centrality.
        """

        raise NotImplementedError

    

if __name__ == "__main__":
    vertices = [1, 2, 3, 4, 5, 6]
    edges    = [(1, 2), (1,5),(2, 3), (2,5),(3, 4),(3,6), (4,5), (4,6)]
    g = Graph(vertices, edges)
    #gp=g.graph(edges)
    #print(gp)
    #print(g.graph(edges))
    #print(g.graph(1,4))
    #print(graph)
    #print(g.min_dist(1,6))
    #print(g.all_paths(1,10))
    #print(g.betweenness_centrality(1))
    #print(g.one_shortest_paths(2,4))
    #print(g.bfs_paths(1,4))
    print(g.top_k_betweenness_centrality(5))
