import sys
# print('Hello')


class Graph():
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for column in range(vertices)]
                      for row in range(vertices)]

    def printsol(self, dist):
        print("Distance\n")
        for node in range(self.V):
            print(node, '\t', dist[node])

    def mindis(self, dist, sel):
        min = sys.maxsize
        for v in range(self.V):
            if sel[v] == False and dist[v] < min:
                min = dist[v]
                index = v
        return index

    def dijkstra(self, src):

        dist = [sys.maxsize]*self.V
        sel = [False]*self.V
        dist[src] = 0
        for i in range(self.V):

            u = self.mindis(dist, sel)
            sel[u] = True
            for v in range(self.V):
                if (sel[v] == False) and (self.graph[u][v] > 0) and (dist[u]+self.graph[u][v] < dist[v]):
                    dist[v] = dist[u]+self.graph[u][v]
        self.printsol(dist)


g = Graph(9)
g.graph = [[0, 4, 0, 0, 0, 0, 0, 8, 0],
           [4, 0, 8, 0, 0, 0, 0, 11, 0],
           [0, 8, 0, 7, 0, 4, 0, 0, 2],
           [0, 0, 7, 0, 9, 14, 0, 0, 0],
           [0, 0, 0, 9, 0, 10, 0, 0, 0],
           [0, 0, 4, 14, 10, 0, 2, 0, 0],
           [0, 0, 0, 0, 0, 2, 0, 1, 6],
           [8, 11, 0, 0, 0, 0, 1, 0, 7],
           [0, 0, 2, 0, 0, 0, 6, 7, 0]
           ]
g.dijkstra(0)
