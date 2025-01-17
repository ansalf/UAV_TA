import pandas as pd
import math

# Class definition for node to be added to graph
class AdjacentNode:
    
    def __init__(self, vertex):
        self.vertex = vertex
        self.next = None

# BidirectionalSearch implementation
class BidirectionalSearch:
    
    def __init__(self, vertices):
        self.vertices = vertices
        self.graph = [None] * self.vertices
        self.src_queue = list()
        self.dest_queue = list()
        self.src_visited = [False] * self.vertices
        self.dest_visited = [False] * self.vertices
        self.src_parent = [None] * self.vertices
        self.dest_parent = [None] * self.vertices
    
    # Function for adding undirected edge
    def add_edge(self, src, dest):
        node = AdjacentNode(dest)
        node.next = self.graph[src]
        self.graph[src] = node
        node = AdjacentNode(src)
        node.next = self.graph[dest]
        self.graph[dest] = node
    
    # Function for Breadth First Search
    def bfs(self, direction='forward'):
        if direction == 'forward':
            current = self.src_queue.pop(0)
            connected_node = self.graph[current]
            while connected_node:
                vertex = connected_node.vertex
                if not self.src_visited[vertex]:
                    self.src_queue.append(vertex)
                    self.src_visited[vertex] = True
                    self.src_parent[vertex] = current
                connected_node = connected_node.next
        else:
            current = self.dest_queue.pop(0)
            connected_node = self.graph[current]
            while connected_node:
                vertex = connected_node.vertex
                if not self.dest_visited[vertex]:
                    self.dest_queue.append(vertex)
                    self.dest_visited[vertex] = True
                    self.dest_parent[vertex] = current
                connected_node = connected_node.next
    
    # Check for intersecting vertex
    def is_intersecting(self):
        for i in range(self.vertices):
            if (self.src_visited[i] and
                self.dest_visited[i]):
                return i
        return -1
    
    # Print the path from source to target
    def print_path(self, intersecting_node,
                   src, dest):
        path = list()
        path.append(intersecting_node)
        i = intersecting_node
        while i != src:
            path.append(self.src_parent[i])
            i = self.src_parent[i]
        path = path[::-1]
        i = intersecting_node
        while i != dest:
            path.append(self.dest_parent[i])
            i = self.dest_parent[i]
        print("*****Path*****")
        path = list(map(str, path))
        print(' '.join(path))
    
    # Function for bidirectional searching
    def bidirectional_search(self, src, dest):
        self.src_queue.append(src)
        self.src_visited[src] = True
        self.src_parent[src] = -1
        self.dest_queue.append(dest)
        self.dest_visited[dest] = True
        self.dest_parent[dest] = -1
        while self.src_queue and self.dest_queue:
            self.bfs(direction='forward')
            self.bfs(direction='backward')
            intersecting_node = self.is_intersecting()
            if intersecting_node != -1:
                print(f"Path exists between {src} and {dest}")
                print(f"Intersection at : {intersecting_node}")
                self.print_path(intersecting_node,
                                src, dest)
                exit(0)
        return -1

# Load dataset
df = pd.read_csv('fire_archive_M6_96619_5data.csv')

# Initialize graph
n = len(df)
graph = BidirectionalSearch(n)

# Add edges to the graph
for index, row in df.iterrows():
    node = (row['latitude'], row['longitude'])
    for idx, r in df.iterrows():
        if (r['latitude'], r['longitude']) != node:
            graph.add_edge(node, (r['latitude'], r['longitude']))

# Add starting point to the graph with a connection to the first point in the dataset
graph.add_edge((0.0, 0.0), (df.iloc[0]['latitude'], df.iloc[0]['longitude']))

# Set start and destination points
src = (0.0, 0.0)
dest = df.iloc[-1]['latitude'], df.iloc[-1]['longitude']

# Perform bidirectional search
graph.bidirectional_search(src, dest)
