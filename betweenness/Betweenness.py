# -*- coding:utf-8 -*-
import gc
import networkx as nx


class betweenness(object):
    def __init__(self, graph, amt_vaccination):
        self.graph = graph
        self.amt_vaccination = amt_vaccination

    def getBetweennessCenterPoint(self):
        all_centrality_dic = nx.betweenness_centrality(self.graph)
        all_centrality_dic = sorted(all_centrality_dic.iteritems(), key=lambda asd: asd[1], reverse=True)
        vaccination_list = []
        for i in all_centrality_dic:
            vaccination_list.append(i[0])
            if len(vaccination_list) == self.amt_vaccination:
                break
        del all_centrality_dic
        gc.collect()
        return vaccination_list
