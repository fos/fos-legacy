import networkx as nx

def network_measures(offset, parents):
    # create a network for each neuron
    for i in range(len(offset)-1):
        # extract the connectivity
        con = parents[offset[i]:offset[i+1]]
        g = nx.Graph()
        # skipt the first node (root node)
        for j in range(1,len(con)-1):
            g.add_edge(con[j], con[j+1])
        
        print "Graph statistics, neuron ", i
        print "# nodes", g.number_of_nodes()
        print "# edges", g.number_of_edges()
        print "average shortest path length", nx.average_shortest_path_length(g)
        print "average clustering coefficient", nx.average_clustering(g)
        
f = h5py.File('neurons.hdf5', 'r')
offset = f['neurons/offset'].value
parents = f['neurons/parents'].value
f.close()

ac = network_measures(parents, offset)
