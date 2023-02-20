import networkx as nx
import graphviz as gv
import matplotlib.pyplot as plt

class Grafo(object):
    def __init__(self, nodos):
        self.nodos = nodos
        self.grafo_graphviz()

    # def dibujar_grafo(self):
    #     G = nx.Graph()
    #     for nodo in self.nodos:
    #         G.add_node(nodo.conteo)
    #         for key, value in nodo.transicion.items():
    #             print(nodo.conteo, key.conteo)
    #             G.add_edge(nodo.conteo, key.conteo, title=value)
    #     edge_labels = nx.get_edge_attributes(G, 'title')
    #     # label = nx.nodes(G)
    #     pos = nx.spring_layout(G)
    #     nx.draw(G, pos, with_labels=True)
    #     nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    #     plt.show()
    

    def grafo_graphviz(self):
        G = gv.Digraph(format='png', graph_attr={'rankdir':'LR'})
        for nodo in self.nodos:
            if nodo.inicial:
                G.node('inicio', shape='none', label='')
                G.node(str(nodo.conteo))
                G.edge('inicio', str(nodo.conteo))
            elif nodo.final:
                G.node(str(nodo.conteo), peripheries = '2')
            else:
                G.node(str(nodo.conteo))

            for key in nodo.transicion.keys():
                for values in nodo.transicion[key]:
                    G.edge(str(nodo.conteo), str(key.conteo), label= str(values))  
                
        G.render('test-output/round-table.gv', view=True)