from lattice_planner import graph_utils
import numpy as np


class LatticeGraph:

    def __init__(self):
        self._graph = graph_utils.Graph()

        self._nrows = None
        self._n_cols = None
        self._lattice_cell_size = None
        self._arc_primitives = {}

    def configure(self, n_rows=10, n_cols=10, lattice_cell_size=10, lattice_type='square_grid'):

        self._nrows = n_rows
        self._n_cols = n_cols
        self._lattice_cell_size = lattice_cell_size

        if lattice_type == 'square_grid':
            self._configure_square_grid_lattice(n_rows, n_cols)
        elif lattice_type == 'arc_grid':
            self._configure_arc_grid_lattice(n_rows, n_cols, lattice_cell_size)
        self._graph.configure()

    def update_obstacles(self, obs):

        for edge_key, edge_val in self._graph._edge_dict.items():
            is_valid = obs.is_edge_valid(edge_key, edge_val, self._lattice_cell_size, self._arc_primitives)

            if not is_valid:
                self._graph._edge_dict[edge_key] = np.inf

        self._graph._set_adjacency_matrix()

    def solve(self, s, g, method):
        path = self._graph.solve(s, g, method)
        return path

    def _configure_square_grid_lattice(self, n_rows, n_cols):

        for row in range(n_rows):
            for col in range(n_cols):
                v = (row, col)
                self._graph.add_vertex(v)

        for row in range(n_rows):
            for col in range(n_cols):

                v = (row, col)

                if (row-1) >= 0:
                    v_top = (row-1, col)
                    self._graph.set_edge(v, v_top, 1)

                if (row+1) < n_rows:
                    v_buttom = (row+1, col)
                    self._graph.set_edge(v, v_buttom, 1)

                if (col-1) >= 0:
                    v_left = (row, col-1)
                    self._graph.set_edge(v, v_left, 1)

                if (col+1) < n_cols:
                    v_right = (row, col+1)
                    self._graph.set_edge(v, v_right, 1)

    def _configure_arc_grid_lattice(self, n_rows, n_cols, lattice_cell_size):

        for row in range(n_rows):
            for col in range(n_cols):
                for angle in [0, 90, 180, 270]:
                    v = (row, col, angle)
                    self._graph.add_vertex(v)

        for row in range(n_rows):
            for col in range(n_cols):
                for angle in [0, 90, 180, 270]:

                    v = (row, col, angle)

                    # top row
                    if (row - 1) >= 0 and angle == 90:
                        v_top = (row - 1, col, 90)

                    if (col - 1) >= 0 and (row - 1) >= 0 and angle == 90:
                        v_top_left = (row - 1, col - 1, 180)
                        self._graph.set_edge(v, v_top_left, 2)

                    if (col + 1) < n_cols and (row - 1) >= 0 and angle == 90:
                        v_top_right = (row - 1, col + 1, 0)
                        self._graph.set_edge(v, v_top_right, 2)

                    # buttom row
                    if (row + 1) < n_rows and angle == 270:
                        v_buttom = (row + 1, col, 270)
                        self._graph.set_edge(v, v_buttom, 1)

                    if (col - 1) >= 0 and (row + 1) < n_rows and angle == 270:
                        v_buttom_left = (row + 1, col - 1, 180)
                        self._graph.set_edge(v, v_buttom_left, 2)

                    if (col + 1) < n_cols and (row + 1) < n_rows and angle == 270:
                        v_buttom_right = (row + 1, col + 1, 0)
                        self._graph.set_edge(v, v_buttom_right, 2)

                    # left col
                    if (col - 1) >= 0 and angle == 180:
                        v_left = (row, col - 1, 180)
                        self._graph.set_edge(v, v_left, 1)

                    if (col - 1) >= 0 and (row - 1) >= 0 and angle == 180:
                        v_left_up = (row - 1, col - 1, 90)
                        self._graph.set_edge(v, v_left_up, 2)

                    if (col - 1) >= 0 and (row + 1) < n_rows and angle == 180:
                        v_left_down = (row + 1, col - 1, 270)
                        self._graph.set_edge(v, v_left_down, 2)

                    # right col
                    if (col + 1) < n_cols and angle == 0:
                        v_right = (row, col + 1, 0)
                        self._graph.set_edge(v, v_right, 1)

                    if (col + 1) < n_cols and (row - 1) >= 0 and angle == 0:
                        v_right_up = (row - 1, col + 1, 90)
                        self._graph.set_edge(v, v_right_up, 2)

                    if (col + 1) < n_cols and (row + 1) < n_rows and angle == 0:
                        v_right_down = (row + 1, col + 1, 270)
                        self._graph.set_edge(v, v_right_down, 2)

        # arcs
        npoints = int(lattice_cell_size * np.pi / 2) + 1
        pts_0_to_90 = np.zeros((2, npoints))
        for i in range(npoints):
            x = np.cos(float(i) / float(npoints - 1) * np.pi / 2) * lattice_cell_size - lattice_cell_size
            y = np.sin(float(i) / float(npoints - 1) * np.pi / 2) * lattice_cell_size
            pts_0_to_90[0, i] = x
            pts_0_to_90[1, i] = y

        self._arc_primitives[(0, 90)] = pts_0_to_90

        pts_0_to_270 = np.zeros((2, npoints))
        pts_0_to_270[0, :] = -1*pts_0_to_90[0, :]
        pts_0_to_270[1, :] = pts_0_to_90[1, :]
        self._arc_primitives[(0, 270)] = pts_0_to_270

        pts_270_to_180 = np.zeros((2, npoints))
        pts_270_to_180[0, :] = np.flip(pts_0_to_90[0, :]) + lattice_cell_size
        pts_270_to_180[1, :] = np.flip(pts_0_to_90[1, :]) - lattice_cell_size
        self._arc_primitives[(270, 180)] = pts_270_to_180

        pts_90_to_180 = np.zeros((2, npoints))
        pts_90_to_180[0, :] = np.flip(pts_0_to_270[0, :]) - lattice_cell_size
        pts_90_to_180[1, :] = np.flip(pts_0_to_270[1, :]) - lattice_cell_size
        self._arc_primitives[(90, 180)] = pts_90_to_180

        pts_90_to_0 = np.zeros((2, npoints))
        pts_90_to_0[0, :] = pts_90_to_180[0, :]
        pts_90_to_0[1, :] = -1*pts_90_to_180[1, :]
        self._arc_primitives[(90, 0)] = pts_90_to_0

        pts_180_to_270 = np.zeros((2, npoints))
        pts_180_to_270[0, :] = np.flip(pts_90_to_0[0, :]) + lattice_cell_size
        pts_180_to_270[1, :] = np.flip(pts_90_to_0[1, :]) - lattice_cell_size
        self._arc_primitives[(180, 270)] = pts_180_to_270

        pts_270_to_0 = np.zeros((2, npoints))
        pts_270_to_0[0, :] = -1*np.flip(pts_180_to_270[0, :]) + lattice_cell_size
        pts_270_to_0[1, :] = np.flip(pts_180_to_270[1, :]) + lattice_cell_size
        self._arc_primitives[(270, 0)] = pts_270_to_0

        pts_180_to_90 = np.zeros((2, npoints))
        pts_180_to_90[0, :] = np.flip(pts_270_to_0[0, :]) - lattice_cell_size
        pts_180_to_90[1, :] = np.flip(pts_270_to_0[1, :]) - lattice_cell_size
        self._arc_primitives[(180, 90)] = pts_180_to_90

        DEBUG = 0
        if DEBUG:
            import matplotlib.pyplot as plt

            plt.figure()
            plt.plot(pts_0_to_90[1, :], pts_0_to_90[0, :], 'o--')
            plt.plot(pts_0_to_90[1, 0], pts_0_to_90[0, 0], 'x')
            plt.gca().invert_yaxis()
            plt.title("pts_0_to_90")
            plt.show()

            plt.figure()
            plt.plot(pts_0_to_270[1, :], pts_0_to_270[0, :], 'o--')
            plt.plot(pts_0_to_270[1, 0], pts_0_to_270[0, 0], 'x')
            plt.gca().invert_yaxis()
            plt.title("pts_0_to_270")
            plt.show()

            plt.figure()
            plt.plot(pts_270_to_180[1, :], pts_270_to_180[0, :], 'o--')
            plt.plot(pts_270_to_180[1, 0], pts_270_to_180[0, 0], 'x')
            plt.gca().invert_yaxis()
            plt.title("pts_270_to_180")
            plt.show()

            plt.figure()
            plt.plot(pts_90_to_180[1, :], pts_90_to_180[0, :], 'o--')
            plt.plot(pts_90_to_180[1, 0], pts_90_to_180[0, 0], 'x')
            plt.gca().invert_yaxis()
            plt.title("pts_90_to_180")
            plt.show()

            plt.figure()
            plt.plot(pts_90_to_0[1, :], pts_90_to_0[0, :], 'o--')
            plt.plot(pts_90_to_0[1, 0], pts_90_to_0[0, 0], 'x')
            plt.gca().invert_yaxis()
            plt.title("pts_90_to_0")
            plt.show()

            plt.figure()
            plt.plot(pts_180_to_270[1, :], pts_180_to_270[0, :], 'o--')
            plt.plot(pts_180_to_270[1, 0], pts_180_to_270[0, 0], 'x')
            plt.gca().invert_yaxis()
            plt.title("pts_180_to_270")
            plt.show()

            plt.figure()
            plt.plot(pts_270_to_0[1, :], pts_270_to_0[0, :], 'o--')
            plt.plot(pts_270_to_0[1, 0], pts_270_to_0[0, 0], 'x')
            plt.gca().invert_yaxis()
            plt.title("pts_270_to_0")
            plt.show()

            plt.figure()
            plt.plot(pts_180_to_90[1, :], pts_180_to_90[0, :], 'o--')
            plt.plot(pts_180_to_90[1, 0], pts_180_to_90[0, 0], 'x')
            plt.gca().invert_yaxis()
            plt.title("pts_180_to_90")
            plt.show()


class ObstaclesGrid:
    def __init__(self, map_size):

        self.map = np.zeros(map_size, dtype=np.bool)
        self.map_size = map_size

    def is_edge_valid(self, edge_key, edge_val, lattice_cell_size, arc_primitives):

        pt1 = edge_key[0]
        pt2 = edge_key[1]

        if edge_val == 1:  # line
            pts = self._get_pts_from_line(pt1, pt2, lattice_cell_size)
        elif edge_val == 2:  # arc
            pts = self._get_pts_from_arc(pt1, pt2, lattice_cell_size, arc_primitives)
        else:
            pts = [(-99, -99)]

        for pt in pts:
            if not self._is_point_valid(pt):
                return False

        return True

    def _get_pts_from_line(self, pt1, pt2, lattice_cell_size):

        pts = []
        dir_row = pt2[0] - pt1[0]
        dir_col = pt2[1] - pt1[1]

        for i in range(lattice_cell_size):
            row = pt1[0]*lattice_cell_size + i*dir_row
            col = pt1[1]*lattice_cell_size + i*dir_col
            pts.append((row, col))

        return pts

    def _get_pts_from_arc(self, pt1, pt2, lattice_cell_size, arc_primitives):

        if pt1[2] == pt2[2]:
            pts = self._get_pts_from_line(pt1, pt2, lattice_cell_size)
        else:
            arc = arc_primitives[(pt1[2], pt2[2])]
            arc = np.array(pt1[:2]).reshape((2, 1)) * lattice_cell_size + arc

            pts = []
            for i in range(arc.shape[1]):
                pts.append((int(arc[0, i]), int(arc[1, i])))

        return pts

    def _is_point_valid(self, point):

        if point[0] >= self.map_size[0] or point[1] >= self.map_size[1] or point[0] < 0 or point[1] <0:
            return False

        return not self.map[point[0], point[1]]