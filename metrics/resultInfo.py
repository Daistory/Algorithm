import networkx as nx
from wheel.signatures.djbec import double


class ResultInfo(object):
    def __init__(self, graph, vaccination_list):
        self.graph = graph
        self.vaccination_list = vaccination_list

    def getInfo(self):
        info_list = []
        count_nodes = self.graph.number_of_nodes()
        count_degree = 0
        for i in nx.degree(self.graph).values():
            count_degree += i
        info_list.append(double(count_degree) / double(count_nodes))
        count_degree = 0
        count_clustering = 0.0
        for i in self.vaccination_list:
            count_degree += nx.degree(self.graph, i)
            count_clustering += nx.clustering(self.graph, i)
        info_list.append(double(count_degree) / double(len(self.vaccination_list)))
        info_list.append(nx.average_clustering(self.graph))
        info_list.append(double(count_clustering) / double(len(self.vaccination_list)))
        total = 0
        index = 0
        shell = 1
        while True:
            if 0 == nx.k_shell(self.graph, shell).number_of_nodes():
                break
            total += nx.k_shell(self.graph, shell).number_of_nodes() * shell
            for j in self.vaccination_list:
                if j in nx.k_shell(self.graph, shell):
                    index += shell
            shell += 1
        info_list.append(double(total) / double(count_nodes))
        info_list.append(double(index) / double(len(self.vaccination_list)))
        return info_list
