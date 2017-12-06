class Degree(object):
    def __init__(self, graph, amt_vaccination):
        self.graph = graph
        self.amt_vaccination = amt_vaccination

    def getDegreePoint(self):
        point_dic = self.graph.degree()
        vaccination_list = []
        newpointDic = sorted(point_dic.iteritems(), key=lambda asd: asd[1], reverse=True)
        for i in newpointDic:
            vaccination_list.append(i[0])
            if len(vaccination_list) == self.amt_vaccination:
                break
        return vaccination_list
