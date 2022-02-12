from queue import Queue, PriorityQueue
import numpy as np


class Graph:

    def __init__(self):

        self._vert_list = []
        self._edge_dict = {}
        self._adjacency_matrix_initialized = False

    def add_vertex(self, v):
        self._vert_list.append(v)

    def set_edge(self, v1, v2, e):
        self._edge_dict[(v1, v2)] = e

    def configure(self):
        self._set_adjacency_matrix()

    def solve(self, start, goal, method="dijkstra"):

        if method == "bfs":
            path = self._solve_bfs(start, goal)
        elif method == "dijkstra":
            path = self._solve_dijkstra(start, goal)
        elif method == "A*":
            path = self._solve_astar(start, goal)
        else:
            path = None

        return path

    def _solve_bfs(self, s, g):

        open_Q = Queue()
        closed = set()
        predecessors = dict()

        open_Q.put(s)

        while not open_Q.empty():

            u = open_Q.get()

            if u == g:
                path = self._extract_path(s, g, predecessors)
                return path
            for v in self._get_adjacent(u):
                if (v in closed) or (v in open_Q.queue):
                    continue
                open_Q.put(v)
                predecessors[v] = u

            closed.add(u)

        return []

    def _solve_dijkstra(self, s, g):

        open_Heap = PriorityQueue()

        closed = set()
        predecessors = dict()
        distances = dict()

        open_Heap.put((0, s))

        while not open_Heap.empty():

            u_cost, u = open_Heap.get()

            if u == g:
                path = self._extract_path(s, g, predecessors)
                return path

            for v in self._get_adjacent(u):

                if v in closed:
                    continue

                uv_cost = self._get_cost(u, v)

                if v in open_Heap.queue:

                    old_cost = distances[v]
                    new_cost = u_cost + uv_cost

                    if new_cost < old_cost:
                        distances[v] = new_cost
                        predecessors[v] = u

                else:
                    open_Heap.put((u_cost + uv_cost, v))
                    distances[v] = u_cost + uv_cost
                    predecessors[v] = u

            closed.add(u)

        return []

    def _solve_astar(self, s, g):
        pass

    def _set_adjacency_matrix(self):

        if not self._adjacency_matrix_initialized:
            self._adjacency_matrix = np.zeros((len(self._vert_list), len(self._vert_list)))
            self._adjacency_matrix_initialized = True

        for i, v in enumerate(self._vert_list):
            for j, u in enumerate(self._vert_list):

                key = (u, v)

                if key in self._edge_dict:
                    self._adjacency_matrix[j, i] = self._edge_dict[key]

    def _extract_path(self, s, g, predecessors):

        path = [g]
        next_v = g
        while True:
            for v in predecessors:

                if s == next_v:
                    path.reverse()
                    return path

                if v == next_v:
                    if predecessors[v] not in path:
                        path.append(predecessors[v])
                        next_v = predecessors[v]

    def _get_adjacent(self, u):

        row = self._vert_list.index(u)
        is_adj = (self._adjacency_matrix[row, :] < np.inf) & (self._adjacency_matrix[row, :] > 0)

        adj_list = []
        for i, v in enumerate(self._vert_list):
            if is_adj[i]:
                adj_list.append(v)

        return adj_list

    def _get_cost(self, v1, v2):
        if (v1, v2) in self._edge_dict:
            return self._edge_dict[(v1, v2)]
        else:
            return np.inf
