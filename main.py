import matplotlib.pyplot as plt
import numpy as np


class Extractor(object):
    def __init__(self, file_name):
        self.q = {'true': 0, 'array': [], 'len': 0}
        self.m = {'true': 0, 'array': [], 'len': 0}

        with open(file_name) as f:
            self.q['true'], self.q['array'] = self.extract_parameters(f.readline())
            self.q['len'] = len(self.q['array'])
            self.m['true'], self.m['array'] = self.extract_parameters(f.readline())
            self.m['len'] = len(self.m['array'])

            self.entry_matrix = np.zeros((self.q['len'], self.m['len']))
            for i in range(self.q['len']):
                for j, value in enumerate(f.readline().strip().split(" ")):
                    self.entry_matrix[i][j] = int(value)
                    assert j < self.m['len'], 'Wrong parameters'

    @staticmethod
    def extract_parameters(_str):
        _line = _str.strip().split(";")
        p0 = float(_line[0])
        _line = _line[1].split(":")
        p_n = int(_line[0])
        p_range = (float(_line[2])-float(_line[1]))
        i = 0
        p = []
        p_current = float(_line[1])
        while True:
            p.append(p_current)
            i += 1
            if i == p_n:
                break
            else:
                p_current += p_range/(p_n-1)
        return p0, np.array(p)


if __name__ == '__main__':
    ext = Extractor("result_matrix.dat")

    n = 9
    print(np.sum(ext.entry_matrix[n]))
    plt.plot(ext.m['array'], ext.entry_matrix[n])
    plt.axvline(ext.m['true'])
    plt.show()
