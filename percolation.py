# --*coding:utf-8*--
import random

import method
import networkx as nx


def getExplosivePoint(graph):
    vaccination_list = []
    vaccination_suppose_list = graph.nodes()  # 假定所有的节点初始状态是已经免疫了的，即是候选节点
    new_graph = nx.Graph()
    new_graph.add_nodes_from(vaccination_suppose_list)
    for i in range(len(vaccination_suppose_list)):
        index = getNodeByScore_second(graph, new_graph, vaccination_suppose_list)
        vaccination_suppose_list.remove(index)
        vaccination_list.insert(0, index)
        for j in graph.neighbors(index):
            if j not in vaccination_suppose_list:
                new_graph.add_edge(index, j)
    return vaccination_list


def getNodeByScore_second(graph, new_graph, vaccination_suppose_list):
    ##################################################
    # 参数：
    #       graph.原拓扑
    #       new_graph,每次更新之后的拓扑
    #       vaccination_suppose_list, 候选节点
    #  返回：
    #       node,得到阻碍能力最差的节点的下标
    ##################################################
    total = graph.number_of_nodes()
    index = 1  # 下标位置
    if len(vaccination_suppose_list) >= 1000:
        vaccination_suppose_list = random.sample(vaccination_suppose_list, 1000)
    list = []
    for node in vaccination_suppose_list:
        temp = total + 1
        max_sub_graph_nodes_number = 0  # 最大簇的节点数目
        sub_graph_list = []  # 与节点相连的子图的集合
        for sub_graph in nx.connected_component_subgraphs(new_graph):
            # print sub_graph.nodes()
            if sub_graph.number_of_nodes() > max_sub_graph_nodes_number:
                max_sub_graph_nodes_number = sub_graph.number_of_nodes()
            for i in sub_graph.nodes():
                if i in graph.neighbors(node):
                    sub_graph_list.append(sub_graph.number_of_nodes())
                    break
        sub_graph_list = map(float, sorted(sub_graph_list))
        # print sub_graph_list
        # print sub_graph_list
        if sub_graph_list[-1] != max_sub_graph_nodes_number:
            score = total
            list.append(score)
        elif len(sub_graph_list) == 1:
            score = sub_graph_list[0]
            list.append(score)
        else:
            if sub_graph_list[0] != sub_graph_list[1]:
                score = sub_graph_list[0]
                list.append(score)
            else:
                score = sub_graph_list[0] + float(1) / (total * 100) * sub_graph_list[-2]
                list.append(score)
        if score < temp:
            temp = score
            index = node
    return index
