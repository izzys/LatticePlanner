from lattice_planner.lattice_graph import LatticeGraph, ObstaclesGrid
from lattice_planner import drawing_utils
import matplotlib.pyplot as plt


def main():

    graph = LatticeGraph()
    n_rows = 10
    n_cols = 10
    lattice_cell_size = 10
    lattice_type = 'arc_grid' # square_grid, arc_grid

    graph.configure(n_rows=n_rows, n_cols=n_cols, lattice_cell_size=lattice_cell_size, lattice_type=lattice_type)

    # square grid , dim=2: (row, col)
    if lattice_type == 'square_grid':
        s = (1, 1)
        g = (6, 9)

    # arc grid , dim=3: (row, col, theta) [theta = 0 is horizontal to the right, ccw]
    if lattice_type == 'arc_grid':
        s = (1, 1, 270)
        g = (4, 8, 90)

    obs = ObstaclesGrid(map_size=(n_rows*lattice_cell_size, n_cols*lattice_cell_size))

    obs.map[25:35, 45:56] = True
    obs.map[67:89, 57:76] = True
    obs.map[50:55, 80:99] = True
    obs.map[20:60, 25:35] = True

    graph.update_obstacles(obs)

    fig = drawing_utils.plot_scene(obs, graph, lattice_cell_size)
    drawing_utils.plot_graph(fig, graph, lattice_cell_size)

    path = graph.solve(s, g, 'dijkstra') # bfs, dijkstra,

    print("path length = ", len(path))

    drawing_utils.plot_solution(fig, s, g, path, graph, lattice_cell_size)

    plt.show()


if __name__ == '__main__':
    main()
