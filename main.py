# !usr/bin/python
# -*- coding:utf-8 -*-
import copy

import os

import gc

import method
import fileOprate.dataRetrieve
import fileOprate.saveResult
import RFDC.RFDC
import metrics.metrics

file_name = "data/17-URVemail-edges.net"
graph, total = fileOprate.dataRetrieve.DataRetriever(file_name).getGraph()
vaccination_list = RFDC.RFDC.RandomForest(graph, total / 10, total, 11).getRandForest()
fileOprate.saveResult.ResultSaver("point.txt", vaccination_list).saveData()
fileOprate.saveResult.ResultSaver("hehedaPriority" + ".txt",
                                  metrics.metrics.Metrics(graph, vaccination_list).getInfluence()).saveData()

# relative_path = "data"
# for root, dirs, file_name_list in os.walk(relative_path):
#     pass
# for file_name in file_name_list:
#     result_path = file_name
#     isExists = os.path.exists(result_path)
#     if not isExists:
#         os.makedirs(result_path)
#     try:
#         graph, total = method.getGraph(method.getPath("data/" + file_name))
#         amt_vaccination = graph.number_of_nodes() / 10
#     except Exception, e:
#         print Exception, ":", e
#     for i in range(7):
#         try:
#             new_graph = copy.deepcopy(graph)
#             vaccination_list = method.getRandForsetNew(new_graph, amt_vaccination, total, 2 * i + 1)
#             method.saveData(vaccination_list, result_path + "/forestPoint" + str(2 * i + 1) + ".txt")
#             temp = method.getInfluence(new_graph, vaccination_list)
#             method.saveData(temp, result_path + "/forestPriority" + str(2 * i + 1) + ".txt")
#             print "finish " + str(i) + "th " + file_name
#             del vaccination_list, temp, new_graph
#             gc.collect()
#         except Exception, e:
#             print Exception, ":", e
# method.saveData(vaccination_list, "heheda" + ".txt")
# method.saveData(method.getInfluence(graph, vaccination_list),  "hehedaPriority" + ".txt")
# color_list = ['k', 'b', 'r', 'c', 'g', 'y']
# for i in range(2):
#     new_graph = copy.deepcopy(graph)
#     vaccination_list = method.getRandForset(new_graph, amt_vaccination, total, 10 * i + 1)
#     temp = method.getInfluence(new_graph, vaccination_list)
#     plt.plot(temp, color_list[i])
#     del vaccination_list, temp, new_graph
#     gc.collect()
# plt.show()
