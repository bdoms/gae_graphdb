import importlib
import inspect
import os
import sys

import pydot

try:
    import dev_appserver
except ImportError, e:
    raise ImportError, "App Engine must be in PYTHONPATH."
    sys.exit()

dev_appserver.fix_sys_path()

from google.appengine.ext import db, ndb
from google.appengine.ext.db import polymodel
from google.appengine.ext.ndb import polymodel as npolymodel


def analyzeModels(model_file):
    edges = []
    inheritences = []
    nodes = []

    # import the file given its path
    folder = os.path.dirname(model_file)
    filename = os.path.basename(model_file)
    name, ext = os.path.splitext(filename)
    sys.path.append(folder)
    module = importlib.import_module(name)

    # find all the db classes
    models = []
    for key in dir(module):
        attr = getattr(module, key)
        if (inspect.isclass(attr) and
            (issubclass(attr, db.Model) or
            issubclass(attr, polymodel.PolyModel) or
            issubclass(attr, ndb.Model) or
            issubclass(attr, npolymodel.PolyModel))):

            models.append(attr)
    
    # find references from one to another
    for model in models:
        # include inheritence
        for other_model in models:
            if model != other_model and issubclass(model, other_model):
                inheritences.append((model.__name__, other_model.__name__))

        for prop in dir(model):
            attr = getattr(model, prop)
            # don't need to check self reference property because reference property includes it
            if (isinstance(attr, db.ReferenceProperty) or
                isinstance(attr, ndb.KeyProperty)):

                reference = getattr(attr, "reference_class")
                edges.append((model.__name__, reference.__name__))

    # find nodes that are disconnected sub graphs
    for model in models:
        model_name = model.__name__
        found = False
        for edge in edges:
            if model_name in edge:
                found = True
                break
        if not found:
            for inheritence in inheritences:
                if model_name in inheritence:
                    found = True
                    break
        if not found:
            nodes.append(model_name)

    return edges, inheritences, nodes


def writeGraph(edges, inheritences, nodes, filename, method='dot', parent_childs=None):
    assert method in ['circo', 'dot', 'fdp', 'neato', 'twopi']

    graph = pydot.graph_from_edges(edges, directed=True)

    # add any disconnected subgraphs here
    for node in nodes:
        graph.add_node(pydot.Node(node))

    graph.set_edge_defaults(arrowhead="odot")

    for inheritence in inheritences:
        graph.add_edge(pydot.Edge(inheritence[0], inheritence[1]))

    if parent_childs:
        graph.set_edge_defaults(arrowhead="onormal")

        for pair in parent_childs:
            graph.add_edge(pydot.Edge(pair[0], pair[1]))

    graph.write_png(filename, prog=method)
