# -*- coding:utf-8 -*-
import gc
import networkx as nx;


class DataRetriever(object):
    def __init__(self, file_name):
        self.file_name = file_name

    def _getPath(self):
        """
        :param file_name: 文件的路径名加上名字
        :return: 装有所有点的list，第一个点和第二个点成一条边，同理3,4..........
        """
        file_handle = file(self.file_name, 'r')
        temp_str = ""
        index = 0
        for temp_line in file_handle.readlines():
            temp_str = temp_str + temp_line
            temp_str = temp_str.replace('\n', ' ')
            temp_str = temp_str.replace('\t', ' ')
            index += 1  # 计数器,方便后面对是否有权重的删除每行最后哦偶一个元素
        path_list = temp_str.split(' ')
        del path_list[-1]
        if len(path_list) / index == 3:
            for i in range(len(path_list) / 3):
                del path_list[2 * (i + 1)]
        path_list = map(int, path_list)
        file_handle.close()
        del temp_str, file_handle
        gc.collect()
        return path_list

    def getGraph(self):
        """
        :param path_list: 相对的图文件路径
        :return: target_graph,最大的连同分支
                 total，原网络中的节点数目
        """
        path_list = self._getPath()
        graph = nx.Graph()
        temp = 0
        for i in range(len(path_list) / 2):
            j = i * 2
            graph.add_edge(path_list[j], path_list[j + 1])
        total = graph.number_of_nodes()
        for connected_graph in nx.connected_component_subgraphs(graph):
            if connected_graph.number_of_nodes() > temp:
                temp = connected_graph.number_of_nodes()
                target_graph = connected_graph
        del path_list, graph, temp
        gc.collect()
        return target_graph, total
