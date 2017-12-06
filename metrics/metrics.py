# -*- coding:utf-8 -*-
import networkx as nx
from wheel.signatures.djbec import double


class Metrics(object):
    def __init__(self, graph, vaccination_list):
        self.graph = graph
        self.vaccination_list = vaccination_list

    def getInfluence(self):
        """
        获取对应接种接种点之后的影响范围
        :param graph: 原图
        :param vaccination_list: 接种节点的集合
        :return: 删除对应节点之后的一个鲁帮性结果
        """
        influence_list = []
        for i in self.vaccination_list:
            self.graph.remove_edges_from(self.graph.edges(i))
            g = nx.connected_components(self.graph)  # 得到断开该点之后的连接情况
            count_graph = self.graph.number_of_nodes()
            influence_point = 0.0
            for j in g:
                count_sub_graph = len(j)  # 得到局部网络的人数
                influence_point = influence_point + float(count_sub_graph * count_sub_graph) / float(count_graph)
            influence_list.append(float(influence_point) / count_graph)
        return influence_list

    def getRelativeSize(self):
        """
        获得最大簇的相对大小
        :param graph:
        :param vaccination_list: 待接种的点的集合
        :return: relative_size (= (最大簇的节点数量)/(网络总的节点数目))
        """
        count_nodes = self.graph.number_of_nodes()
        relative_size_list = []
        for i in self.vaccination_list:
            temp = 0
            self.graph.remove_edges_from(self.graph.edges(i))
            nx.connected_component_subgraphs(self.graph)
            for j in nx.connected_component_subgraphs(self.graph):
                if j.number_of_nodes() > temp:
                    temp = j.number_of_nodes()
                    new_graph = j
            relative_size_list.append(double(new_graph.number_of_nodes()) / count_nodes)
        return relative_size_list