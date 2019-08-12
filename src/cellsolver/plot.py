
import math
import matplotlib.pyplot as graph
from matplotlib import cm


def plot_solution(x, y_n, x_info, y_n_info, title):
    extents = _get_extents(y_n, y_n_info)
    unique_extents = list(set(extents))
    ordered_unique_extents = sorted(unique_extents)
    graph_rows = len(ordered_unique_extents)
    colours = _get_colours(len(extents))
    created_subplots = []
    for index, result in enumerate(y_n):
        extent = extents[index]
        graph_row = ordered_unique_extents.index(extent) + 1
        graph.subplot(graph_rows, 1, graph_row)
        graph.plot(x, result, label=y_n_info[index]['name'], color=colours[index])
        graph.legend()
        if graph_row not in created_subplots:
            if graph_row == len(ordered_unique_extents):
                graph.xlabel("{0} ({1})".format(x_info['name'], x_info['units']))
            graph.ylabel("{0}".format(y_n_info[index]['units']))
            if graph_row == 1:
                graph.title(title)

            created_subplots.append(graph_row)
    graph.show()


def _get_colours(num_colours):
    colours = []
    colour_map = cm.get_cmap('hsv')
    for i in range(num_colours):
        colour = colour_map(1. * i / num_colours)  # color will now be an RGBA tuple
        colours.append(colour)

    return colours


def _get_extents(data_in, data_info):
    extents = []
    for index, data in enumerate(data_in):
        extents.append('{0} {1} {2}'.format(math.floor(math.log10(abs(max(data)))),
                                            math.floor(math.log10(abs(min(data)))),
                                            data_info[index]['units']))

    return extents
