import networkx as nx
import numpy as np
from bson import ObjectId
from pylab import rcParams
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import itertools

from socialColabGraph import createAndGetCollaborationDict
from techColabGraph import create_and_get_social_collaboration_dict


def beautiful_graph(parentGraph):
    rcParams['figure.figsize'] = 14, 10
    pos = nx.spring_layout(parentGraph, scale=20, k=3 / np.sqrt(parentGraph.order()))
    d = dict(parentGraph.degree)
    nx.draw(parentGraph, pos,
            with_labels=True,
            nodelist=d,
            node_size=[d[k] * 100 for k in d])
    plt.show()


def create_and_get_collaboration_graph(G):
    parent_graph = nx.Graph()
    for fileName, devs in G.items():
        temp_graph = nx.Graph()
        for dev in devs:
            temp_graph.add_node(dev)
        temp_graph.add_edges_from(itertools.combinations(list(devs), 2))
        parent_graph = nx.compose(parent_graph, temp_graph)
    return parent_graph

beautiful_graph(create_and_get_collaboration_graph(create_and_get_social_collaboration_dict("kafka")))
beautiful_graph(create_and_get_collaboration_graph(createAndGetCollaborationDict("kafka")))