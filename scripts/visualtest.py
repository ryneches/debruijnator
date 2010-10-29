#!/usr/bin/env python

import debruijnator 
import xmlrpclib
import os

os.system( 'ubigraph_server &' )

os.system( 'sleep 1' )

# Create a server object.
server_url = 'http://127.0.0.1:20738/RPC2'
server = xmlrpclib.Server(server_url)
G = server.ubigraph


db = debruijnator.deBruijnGraph( 4 )
db.consume_seq( 'gattgcctagctagggctagcgtttaagttcga' )

for key in db.graph.keys() :
    G.new_vertex_w_id( db.graph.keys().index( key ) )
    G.set_vertex_attribute( db.graph.keys().index(key), 'label', key )

for key1 in db.graph.keys() :
    for key2 in map( db.graph.keys().index, db.graph[key1]['down'].keys() ) :
        G.new_edge( db.graph.keys().index(key1), key2 )

