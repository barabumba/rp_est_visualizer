from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from collections import namedtuple


class TestResults(object):
    def __init__(self, q, m, matrix):
        self.q = q
        self.m = m
        self.entry_matrix = matrix

    def __hash__(self):
        return hash(str(self.q.true)+str(self.q.array)+str(self.m.true)+str(self.m.array))


class Extractor(object):
    def __init__(self, *args):
        self.uploaded_data_dict = {}
        self.q = {'true': 0, 'array': [], 'len': 0}
        self.m = {'true': 0, 'array': [], 'len': 0}

        cnt = 0
        for file_name in args:
            try:
                if file_name.strip().split(".")[1] != "dat":
                    print("File {0}: unidentified suffix".format(file_name))
                    continue
                else:
                    cnt += 1
            except SyntaxError:
                print("Unrecognized file {0}".format(file_name))
                continue

            with open(file_name) as f:
                q_true, q_array = self._extract_parameters(f.readline())
                m_true, m_array = self._extract_parameters(f.readline())
                entry_matrix = np.zeros((len(q_array), len(m_array)))
                for i in range(len(q_array)):
                    for j, value in enumerate(f.readline().strip().split(" ")):
                        entry_matrix[i][j] = int(value)
                        assert j < len(m_array), 'Wrong parameters'

                parameter = namedtuple("parameter", ["true", "array", "len"])
                test_res = TestResults(parameter(q_true, q_array, len(q_array)),
                                       parameter(m_true, m_array, len(m_array)),
                                       entry_matrix)
                self.uploaded_data_dict.setdefault("{0}".format(cnt), test_res)
        else:
            print("Total files uploaded: {0}".format(cnt))

        self._combine_results()

    @staticmethod
    def _extract_parameters(_str):
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

    def _combine_results(self):
        total_entry_matrix = []
        if self._check_test_conformity():
            q = self.uploaded_data_dict["1"].q
            m = self.uploaded_data_dict["1"].m
            for test_res in self.uploaded_data_dict.values():
                total_entry_matrix.append(test_res.entry_matrix)
            total_entry_matrix = sum(total_entry_matrix)
            self.uploaded_data_dict.setdefault("combined_results", TestResults(q, m, total_entry_matrix))

    def _check_test_conformity(self):
        hashes = []
        for test_res in self.uploaded_data_dict.values():
            hashes.append(hash(test_res))
        return not(len(set(hashes))-1)


if __name__ == '__main__':
    ext = Extractor("result_matrix.dat", "result_matrix2.dat")
    n = 8
    test = ext.uploaded_data_dict["combined_results"]
    X = test.m.array
    Y = test.entry_matrix[n]
    print(np.sum(Y))
    plt.plot(X, Y/np.sum(Y))
    plt.show()

    # X = np.array(test.m.array)
    # Y = np.array(test.q.array)
    # X, Y = np.meshgrid(X, Y)
    # Z = test.entry_matrix
    # Z /= np.sum(Z)
    #
    # ax = plt.axes()
    # ax.contourf(X, Y, Z, levels=50, cmap='gist_heat')
    # ax.axhline(test.q.true, color='g')
    # ax.axvline(test.m.true, color='g')
    # plt.show()
