import matplotlib.pyplot as plt
import numpy as np


def plot_scene(obs, graph, arc_length):

    fig, ax = plt.subplots()
    obs_plot = 0.6*obs.map.astype(np.float)
    plt.imshow(obs_plot, vmin=0.0, vmax=1.0, cmap='Greys')#, cmap='gray', Greys, Oranges ,Greens, Reds, cividis
    plt.grid(True)

    return ax


def plot_graph(ax, graph, arc_length):

    for edge in list(graph._graph._edge_dict):

            if len(edge[0]) == 2:

                v1 = edge[0]
                v2 = edge[1]
                ax.plot(v1[1] * arc_length, v1[0] * arc_length, 'bs', markersize=1)
                ax.plot([v1[1] * arc_length, v2[1] * arc_length], [v1[0] * arc_length, v2[0] * arc_length], color=(0.31, 0.1, 0.6), linewidth=0.5)

            else:

                if edge[0][2] == edge[1][2]:
                    v1 = edge[0]
                    v2 = edge[1]
                    ax.plot(v1[1] * arc_length, v1[0] * arc_length, 'bs', markersize=1)
                    ax.plot([v1[1] * arc_length, v2[1] * arc_length], [v1[0] * arc_length, v2[0] * arc_length], color=(0.31, 0.1, 0.6), linewidth=0.5)
                    #plt.pause(0.01)

                else:
                    v1 = edge[0]
                    v2 = edge[1]
                    arc = graph._arc_primitives[(v1[2], v2[2])]
                    arc = np.array(v1[:2]).reshape((2, 1)) * arc_length + arc
                    ax.plot(arc[1, :], arc[0, :], color=(0.31, 0.1, 0.6), linewidth=0.5)
                    #plt.pause(0.01)
    plt.pause(0.01)


def plot_solution(ax, s, g, path, graph, arc_length):

    ax.plot(s[1]*arc_length, s[0]*arc_length, 'go', markersize=8)
    ax.plot(g[1]*arc_length, g[0]*arc_length, 'ro', markersize=8)

    for i in range(len(path)-1):

        if len(path[0]) == 2:

            v1 = path[i]
            v2 = path[i+1]
            ax.plot([v1[1] * arc_length, v2[1] * arc_length], [v1[0] * arc_length, v2[0] * arc_length], color=(0.41, 0.3, 0.7), linewidth=3)

        else:

            if path[i][2] == path[i+1][2]:
                v1 = path[i]
                v2 = path[i+1]
                ax.plot([v1[1] * arc_length, v2[1] * arc_length], [v1[0] * arc_length, v2[0] * arc_length], color=(0.41, 0.3, 0.7), linewidth=3)
                #plt.pause(0.01)
            else:
                v1 = path[i]
                v2 = path[i+1]
                arc = graph._arc_primitives[(v1[2], v2[2])]
                arc = np.array(v1[:2]).reshape((2, 1)) * arc_length + arc
                ax.plot(arc[1, :], arc[0, :], color=(0.41, 0.3, 0.7), linewidth=3)
                #plt.pause(0.01)

    plt.pause(0.01)




