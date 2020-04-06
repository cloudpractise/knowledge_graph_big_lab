#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from __future__  import print_function  # Python 2/3 compatibility

from gremlin_python import statics
from gremlin_python.structure.graph import Graph
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.strategies import *
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
statics.load_statics(globals())
graph = Graph()
remoteConn = DriverRemoteConnection('ws://52.73.109.206:8182/gremlin','g')
g = graph.traversal().withRemote(remoteConn)
g.addV('person').property(id,'600').property('age','18-24')
list = g.V()
print(list)