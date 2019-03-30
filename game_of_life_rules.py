import scipy
import scipy.signal
import numpy as np

import abc
"""
Game of Life Rules are applied as logical operators on convolution on the world matrix 
"""
class AbstractRules:
    cnt_kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
    @abc.abstractmethod
    def apply(s, live):
        pass

    @staticmethod
    def get_cnt_kernel():
        return AbstractRules.cnt_kernel

    @staticmethod
    def calc_cnt(live, cnt_kernel):
        """Calculate count neigbours using 2d convolution
        :param live: the curr world in binary mode
        :param cnt_kernel: which kernel to use for counting (e.g all 8 nighbours, or only horizontal and vertical)
        :return:
        """
        return scipy.signal.convolve2d(live, cnt_kernel,
                                      mode='same', boundary='fill', fillvalue=0)

class OriginalRules(AbstractRules):
    #tried to use lambdas but inside a clas it expects the class object as an extra parameter
    l_under_pop = lambda live, cnt: ~(cnt < 2) & live #Any live cell with fewer than two live neighbors dies (under population)
    l_surv      = lambda live, cnt: np.isin (cnt, [2,3]) & live  #Any live cell with two or three live neighbors lives on to the next generation.
    l_overpop   = lambda live, cnt: ~(cnt > 3) & live  #Any live cell with more than three live neighbors dies
    l_repro     = lambda live, cnt: (cnt == 3) & ~live  #Any dead cell with exactly three live neighbors becomes a live cell

    def apply(s, live):
        cnt = s.calc_cnt(live, super().cnt_kernel)
        new_live = ()
        try:
            r1, r2, r3, r4 = s.under_pop(live, cnt), s.survival(live, cnt), s.overpop(live, cnt), s.repro(live, cnt)
            new_live = (r1 & r2 & r3 ) | r4
        except Exception as ex:
            print ("Exception: {}".format(ex))
        return new_live


    @staticmethod
    def under_pop(live, cnt): #Any live cell with fewer than two live neighbors dies (under population)
         res = ~(cnt < 2) & live
         return res

    @staticmethod
    def survival(live, cnt): #Any live cell with two or three live neighbors lives on to the next generation.
         valid = [2, 3]
         res = np.isin (cnt, valid) & live
         return res

    @staticmethod
    def overpop(live, cnt): #Any live cell with more than three live neighbors dies
         res = ~(cnt > 3) & live
         return res

    @staticmethod
    def repro(live, cnt): #Any dead cell with exactly three live neighbors becomes a live cell
         res = ((cnt == 3) & ~live)
         return res

class InfectionRules(AbstractRules):
    l1_cnt_kernel = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    l_repro    = lambda live, cnt: (cnt == 1) & ~live #Any dead cell with a single live neighbor lives on to the next generation.
    l_underpop = lambda live, cnt: ~(cnt < 2) & live  #Any live cell with no horizontal or vertical live neighbors dies.

    def apply(s, live):
        cnt = s.calc_cnt(live, super().cnt_kernel)
        l1_cnt = s.calc_cnt(live, s.l1_cnt_kernel)
        try:
            #new_live = s.l_repro (live, cnt) or s.l_underpop (live, l1_cnt)
            new_live = s.repro(live, cnt) | s.under_pop(live, l1_cnt)
        except Exception as ex:
            print(ex)
        return new_live

    @staticmethod
    def repro(live, cnt):# Any dead cell with a single live neighbor lives on to the next generation
         res = (cnt == 1) & ~live
         return res

    @staticmethod
    def under_pop(live, l1_cnt): #Any live cell with no horizontal or vertical live neighbors dies
         res = ~(l1_cnt < 2) & live
         return res


