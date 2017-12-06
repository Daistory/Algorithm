# --*coding:utf-8*--
import copy

import gc

import betweenness.Betweenness
import degree.Degree
import metrics.metrics
import fileOprate.saveResult
import randomWalk.randomWalk


def getResultByAllWay(graph, amt_vaccination, relative_path, total):
    """
    :param graph: 无向图
    :param amt_vaccination: 需要隔离点的总数
    :param relative_path: 需要存储的相对位置
    :param total: 原来网络的大小
    :return: none
    """
    try:
        new_graph = copy.deepcopy(graph)
        vaccination_list = degree.Degree.Degree(new_graph, amt_vaccination).getDegreePoint()
        fileOprate.saveResult.ResultSaver(vaccination_list, relative_path + "degreePoint" + ".txt").saveData()
        fileOprate.saveResult.ResultSaver(metrics.metrics.Metrics(new_graph, vaccination_list).getInfluence(),
                                          relative_path + "degreePriority" + ".txt").saveData()
        del new_graph
        gc.collect()
    except Exception, e:
        print "error in the way named getDegree"
        print Exception, ":", e
    try:
        new_graph = copy.deepcopy(graph)
        vaccination_list = betweenness.Betweenness.betweenness(new_graph, amt_vaccination).getBetweennessCenterPoint()
        fileOprate.saveResult.ResultSaver(vaccination_list, relative_path + "betweennessPoint" + ".txt").saveData()
        fileOprate.saveResult.ResultSaver(metrics.metrics.Metrics(new_graph, vaccination_list).getInfluence(),
                                          relative_path + "betweennessPriority" + ".txt").saveData()
        del new_graph
        gc.collect()
    except Exception, e:
        print "error in the way named getCentrality"
        print Exception, ":", e
    try:
        new_graph = copy.deepcopy(graph)
        vaccination_list = randomWalk.randomWalk.RandomWalker(new_graph, amt_vaccination, total).getrandWalkPoint()
        fileOprate.saveResult.ResultSaver(vaccination_list, relative_path + "randWalkPoint" + ".txt").saveData()
        fileOprate.saveResult.ResultSaver(metrics.metrics.Metrics(new_graph, vaccination_list).getInfluence(),
                                          relative_path + "randWalkPriority" + ".txt").saveData()
        del new_graph
        gc.collect()
    except Exception, e:
        print "error in the way named getRandNei"
        print Exception, ":", e
    try:
        new_graph = copy.deepcopy(graph)
        vaccination_list = randomWalk.randomWalk.RandomWalker(new_graph, amt_vaccination, total).getRandNeiPoint()
        fileOprate.saveResult.ResultSaver(vaccination_list, relative_path + "randNeiPoint" + ".txt").saveData()
        fileOprate.saveResult.ResultSaver(metrics.metrics.Metrics(new_graph, vaccination_list).getInfluence(),
                                          relative_path + "randNeiPriority" + ".txt").saveData()
        del new_graph
        gc.collect()
    except Exception, e:
        print "error in the way named getRandWalk"
        print Exception, ":", e
    try:
        new_graph = copy.deepcopy(graph)
        vaccination_list = method.getRandSpanTree(new_graph, amt_vaccination, total, 1, 1)
        method.saveData(vaccination_list, relative_path + "similarAntPoint11" + ".txt")
        method.saveData(method.getInfluence(new_graph, vaccination_list),
                        relative_path + "similarAntPriority11" + ".txt")
        del new_graph
        gc.collect()
    except Exception, e:
        print "error in the way named getSimilarAnt"
        print Exception, ":", e
