import networkx as nx
import numpy as np
from bson import ObjectId
from pylab import rcParams
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import itertools
from collections import defaultdict

from pymongo import MongoClient
from p1c2newcomers import findNewComers

cluster = MongoClient("mongodb://localhost:27017")
db = cluster["smartshark"]
issue_comment = db["issue_comment"]

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

def create_and_get_social_collaboration_dict(project_name):
    issue_new_comer = defaultdict(set)
    new_comers = findNewComers(project_name)
    for new_comer in new_comers:
        issue_ids = issue_comment.find({"author_id": new_comer}, {"issue_id":1})
        for issue_id in issue_ids:
            issue_new_comer[issue_id["issue_id"]].add(new_comer)
    return issue_new_comer