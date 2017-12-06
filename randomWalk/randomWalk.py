# -*- coding:utf-8 -*-
import random


class RandomWalker(object):
    """
        使用random的方法，在整个网络中随机选择一个节点，寻找一条路径
        :param graph: 无向图
        :param amt_vaccination: 需要寻找的节点数目
        :param total: 原来网络中总的节点数（实验的网络是寻找的整个网络中最大连通子图，这样才能得到所有节点的标签）
        :return: 接种点集合
        """

    def __init__(self, graph, amt_vaccination, total):
        self.graph = graph
        self.amt_vaccination = amt_vaccination
        self.total = total

    def getrandWalkPoint(self):
        vaccination_list = []
        while True:
            current_position = random.randint(0, self.total)
            if current_position not in vaccination_list and current_position in self.graph.nodes():
                vaccination_list.append(current_position)
                if len(vaccination_list) == self.amt_vaccination:
                    break
                next_path_list = (self.graph.neighbors(current_position))
                next_path_list = list(set(next_path_list).difference(set(vaccination_list)))
                if len(next_path_list) <= 0:
                    continue
                index = random.uniform(0, 1)
                current_position = next_path_list[int(index * (len(next_path_list) - 1))]
                vaccination_list.append(current_position)
                if len(vaccination_list) == self.amt_vaccination:
                    break
        return vaccination_list

    def getRandNeiOfNeiPoint(self):
        vaccination_list = []
        index_list = []
        while (len(vaccination_list) < self.amt_vaccination):
            nei_list = []  # 邻居的邻居
            index = random.randint(0, self.total)
            if index not in index_list:
                index_list.append(index)
                for i in self.graph.neighbors(index):  # 遍历随机点的邻居
                    nei_list = nei_list + self.graph.neighbors(i)
                nei_list = list(set(nei_list))  # 去除重复的元素
                max_degree = 1  # 最大的邻居数量
                subscript = 0  # 保留度最大的点
                for j in nei_list:
                    count_nei = len(self.graph.neighbors(j))
                    if count_nei >= max_degree:
                        max_degree = count_nei
                        subscript = j
                if subscript not in vaccination_list:
                    vaccination_list.append(subscript)
        return vaccination_list

    def getRandNeiPoint(self):
        vaccination_list = []
        index_list = []
        while len(vaccination_list) < self.amt_vaccination:
            index = random.randint(0, self.total)
            if index not in index_list and index in self.graph.nodes():
                index_list.append(index)
                max_degree = 0  # 最大的度
                subscript = 0  # 度最大的节点的下标
                for i in self.graph.neighbors(index):
                    count_nei = len(self.graph.neighbors(i))
                    if count_nei >= max_degree:
                        max_degree = count_nei
                        subscript = i
                vaccination_list.append(subscript)
        return vaccination_list

    def getRandRadiusPoint(self):

        radius = 3

        vaccination_list = []
        index_list = []
        while len(vaccination_list) < self.amt_vaccination:
            index = random.randint(0, self.total)
            all_point = []  # 存放在半径范围内的所有的点
            if index not in index_list:
                index_list.append(index)
                all_point.append(index)
                for i in range(radius):
                    for j in all_point:
                        all_point = all_point + self.graph.neighbors(j)
                all_point = list(set(all_point))
                subscript = 0
                max_degree = 1  # 最大的邻居数量
                for i in all_point:
                    count_nei = self.graph.neighbors(i)
                    if count_nei >= max_degree:
                        max_degree = count_nei
                        subscript = i
                if subscript not in vaccination_list:
                    vaccination_list.append(subscript)
        return vaccination_list
