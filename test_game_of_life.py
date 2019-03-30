from unittest import TestCase
import game_of_life as GOF
import numpy as np
import unittest
import sys

def func_name():
    import traceback
    return traceback.extract_stack(None, 2)[0][2]

class TestGameOfLife(TestCase):
    def sanityTest(self):
        '''
        program[width][height][infect - after][max - generations][seed]
        '''

        args = {
            'width' : 2,
            'height': 3,
            'infect-after': 3,
            'max-generations': 6,
            'seed': "1 0 0 1 1 1",
        }
        width, height, infect_after, max_gen, seed = 2, 3, 3, 6, [1,0, 0, 1, 1, 1]
        obj = GOF.GameOfLife(width, height, infect_after, max_gen)
        obj.playStage()

    #def setUp(self):
    #    pass

    def test_GameOfLifeOnly(self):
        print("-------------------------------")
        print(func_name())
        width, height, infect_after, max_generations, seed = 2, 3, 6, 6, [1, 0, 0, 1, 1, 1]
        GOF.GameIntiation(width, height, infect_after, max_generations, seed)

    def test_infection_only(self):
        print("-------------------------------")
        print(func_name())
        width, height, infect_after, max_generations, seed = 2, 3, 0, 6, [1, 0, 0, 1, 1, 1]
        GOF.GameIntiation(width, height, infect_after, max_generations, seed)

    def test_bad_dimensions_input(self):
        print("-------------------------------")
        print(func_name())
        width, height, infect_after, max_generations, seed = 3, 3, 6, 6, [0, 0, 0, 1, 0, 0, 1, 0]
        GOF.GameIntiation(width, height, infect_after, max_generations, seed)

    def test_reference_input(self):
        print("-------------------------------")
        print(func_name())
        width, height, infect_after, max_generations, seed = 3, 3, 6, 6, [0, 0, 0, 1, 0, 0, 1, 0, 1]
        GOF.GameIntiation(width, height, infect_after, max_generations, seed)


    def test_many_generations(self):
        print("-------------------------------")
        print(func_name())
        width, height, infect_after, max_generations, seed = 3, 3, 6, 1000, [0,0,0,1,0,0,1,0,1]
        GOF.GameIntiation(width, height, infect_after, max_generations, seed)


    def test_big_world(self):
        print("-------------------------------")
        print(func_name())
        width, height,infect_after, max_generations = 50, 50, 6, 6
        seed = np.random.choice([0, 1], size=(width*height), p=[1. / 3, 2. / 3])
        GOF.GameIntiation(width, height, infect_after, max_generations, seed)

if __name__ == '__main__':
    unittest.main()