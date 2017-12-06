# -*- coding:utf-8 -*-

import random

import MyThread
import networkx as nx


class RandomForest(object):
    def __init__(self, graph, amt_vaccination, total, tree_num, start_sign=0, diffusion_sign=0):
        self.graph = graph
        self.amt_vaccination = amt_vaccination
        self.total = total
        self.tree_num = tree_num
        self.start_sign = start_sign
        self.diffusion_sign = diffusion_sign

    def _getTreeGraph(self, graph, total, start_sign=0, diffusion_sign=0):
        """
            :param graph:
            :param total:
            :param start_sign: 生成树起始点的选择，0表示随机选择一个节点作为起始点，1表示的是选择一个度最大的节点作为起始点。  默认式0
            :param diffusion_sign: 使用方法的标志位置,如果是0表示使用的是随机的方式，1表示使用的节点度大的点作为扩散点   默认是0
            :return: new graph
            """
        tree_graph = nx.Graph()
        current_position = 0
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

    def _autoNorm(self, data_list):
        min_value = min(data_list)
        max_value = max(data_list)
        return [float(i - min_value) / float(max_value - min_value) for i in data_list]

    def getRandForest(self):
        """
        :param graph:
        :param amt_vaccination:
        :param total:
        :param start_sign: 生成树起始点的选择，0表示随机选择一个节点作为起始点，1表示的是选择一个度最大的节点作为起始点。  默认式0
        :param diffusion_sign: 使用方法的标志位置,如果是0表示使用的是随机的方式，1表示使用的节点度大的点作为扩散点   默认是0
        :return: 接种点集合
        """
        # 利用多线程生成多课子树
        degree_dic = {}
        threads = []
        index = 0
        for i in range(self.tree_num):
            t = MyThread.MyThread(self._getTreeGraph,
                                  args=(self.graph, self.total, self.start_sign, self.diffusion_sign))
            threads.append(t)
            t.start()
        point_number_list = []
        result_list = []
        index = 0
        max_list = []
        min_list = []
        for t in threads:
            t.join()
            if index == 0:
                point_number_list = t.get_result().degree().keys()
                index = 1
            result_list.append(t.get_result().degree().values())
            max_list.append(max(t.get_result().degree().values()))
            min_list.append(min(t.get_result().degree().values()))
        temp_list = []
        for i in range(len(point_number_list)):
            distance_best = 0.0
            distance_worst = 0.0
            for j in range(self.tree_num):
                distance_best = (max_list[j] - result_list[j][i]) ** 2 + distance_best
                distance_worst = (min_list[j] - result_list[j][i]) ** 2 + distance_worst
            distance_best = distance_best ** (0.5)
            distance_worst = distance_worst ** (0.5)
            temp_list.append(distance_best / (distance_best + distance_worst))
        for i in range(len(point_number_list)):
            degree_dic[point_number_list[i]] = temp_list[i]
        vaccination_list = [sorted(degree_dic.iteritems(), key=lambda b: b[1], reverse=True)[i][0] for i in
                            range(self.amt_vaccination)]

        return vaccination_list
