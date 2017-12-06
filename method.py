# -*- coding:utf-8 -*-
import networkx as nx
from collections import Counter
from numpy import random


def getTreeGraph(graph, total, start_sign=0, diffusion_sign=0):
    """
    :param graph:
    :param total:
    :param start_sign: 生成树起始点的选择，0表示随机选择一个节点作为起始点，1表示的是选择一个度最大的节点作为起始点。  默认式0
    :param diffusion_sign: 使用方法的标志位置,如果是0表示使用的是随机的方式，1表示使用的节点度大的点作为扩散点   默认是0
    :return: new graph
    """
    tree_graph = nx.Graph()
    if start_sign == 0:
        while True:
            current_position = random.randint(0, total)
            if current_position in graph.nodes():
                break
    elif start_sign == 1:
        current_position = sorted((nx.degree(graph)).iteritems(), key=lambda b: b[1], reverse=True)[0][0]
    else:
        exit(0)
    travel_list = []  # 表示已经遍历过的点
    path_list = []  # 标识遍历的路线，当travelList长度等于总的点数的时候表示遍历完成
    path_list.append(current_position)
    travel_list.append(current_position)
    while len(travel_list) < graph.number_of_nodes():  # 将所有点加入树中就是遍历结束的标志
        current_position = path_list[-1]
        next_path_list = graph.neighbors(current_position)
        next_path_list = list(set(next_path_list).difference(set(travel_list)))
        if len(next_path_list) == 0:  # 表示当前点没有邻居，遍历过程进行回退
            del path_list[-1]
        else:
            if diffusion_sign == 0:
                # 所有邻居中随机选择一个作为扩散点
                index = random.uniform(0, 1)
                next_position = next_path_list[int(index * (len(next_path_list) - 1))]
                tree_graph.add_edge(current_position, next_position)
            elif diffusion_sign == 1:
                # 选择度最大的节点作为扩散点
                temp = 0
                next_position = next_path_list[0]
                for index in next_path_list:
                    if len(graph.neighbors(index)) > temp:
                        temp = len(graph.neighbors(index))
                        next_position = index
                tree_graph.add_edge(current_position, next_position)
            else:
                exit(0)
            travel_list.append(next_position)
            path_list.append(next_position)
    return tree_graph


def rankDegree(dic_degree):
    """
    :param dic_degree:节点度的字典
    :return: 节点度的排序
    """
    index = 1
    dic_rank = {}
    for tupe in sorted(dic_degree.iteritems(), key=lambda b: b[1], reverse=True):
        dic_rank[tupe[0]] = index
        index += 1
    return dic_rank


def getRandForsetNew(graph, amt_vaccination, total, tree_num, start_sign=0, diffusion_sign=0):
    """
    :param graph:
    :param amt_vaccination:
    :param total:
    :param start_sign: 生成树起始点的选择，0表示随机选择一个节点作为起始点，1表示的是选择一个度最大的节点作为起始点。  默认式0
    :param diffusion_sign: 使用方法的标志位置,如果是0表示使用的是随机的方式，1表示使用的节点度大的点作为扩散点   默认是0
    :return: 接种点集合
    """
    # 利用多线程生成多课子树
    from RFDC import MyThread
    degree_dic = {}
    threads = []
    index = 0
    for i in range(tree_num):
        t = MyThread.MyThread(getTreeGraph, args=(graph, total, start_sign, diffusion_sign))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
        if index == 0:
            degree_dic = rankDegree(t.get_result().degree())
        else:
            degree_dic = dict(Counter(degree_dic) + Counter(rankDegree(t.get_result().degree())))
        index += 1
    vaccination_list = [sorted(degree_dic.iteritems(), key=lambda b: b[1], reverse=False)[i][0] for i in
                        range(amt_vaccination)]

    return vaccination_list
