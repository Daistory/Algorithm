class ResultSaver(object):
    def __init__(self, file_name, result_list):
        self.file_name = file_name
        self.result_list = result_list

    def saveData(self):
        f = file(self.file_name, 'w+')
        for i in self.result_list:
            f.write(str(i))
            f.write('\n')
        f.close()
