
import hashlib
import math
import matplotlib.pyplot as graph
from matplotlib import cm


def plot_solution(x, y_n):
    extents = _get_extents(y_n)
    unique_extents = list(set(extents))
    graph_rows = len(unique_extents)
    colours = _get_colours(len(extents))
    created_subplots = []
    for index, result in enumerate(y_n):
        extent = extents[index]
        graph_row = unique_extents.index(extent) + 1
        graph.subplot(graph_rows, 1, graph_row)
        graph.plot(x, result, label='state {0}'.format(index), color=colours[index])
        graph.legend()
        if graph_row not in created_subplots:
            if graph_row == len(unique_extents):
                graph.xlabel("(Probably) Time (msecs)")
            graph.ylabel("Y-axis")
            if graph_row == 1:
                graph.title("A test graph")

            created_subplots.append(graph_row)
    graph.show()


def _get_colours(num_colours):
    colours = []
    colour_map = cm.get_cmap('hsv')
    for i in range(num_colours):
        colour = colour_map(1. * i / num_colours)  # color will now be an RGBA tuple
        colours.append(colour)

    return colours


def _get_extents(data_in):
    extents = []
    for data in data_in:
        extents.append('{0} {1}'.format(math.floor(math.log10(abs(max(data)))),
                                                    math.floor(math.log10(abs(min(data))))))

    return extents
