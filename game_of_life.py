import argparse
import numpy as np
import types
import game_of_life_rules as GOF_rules


class GameOfLife:
    """
    This class contains the logic for Conways version with extension of the game infection
    The generations are run as iterators, and the result of the iterator is the flat printout of the current world state
    The rules (original, infection) are picked on as strategy based on infect_after
    """
    def __init__(s, width, height, infect_after, max_generations, seed):
        """
        c'tor. initialize the parameters and invokes factory call for the Rules objects that are to be used in a strategy patttern
        :param width: The width of the world
        :param height: The height of the world
        :param infect_after: The number of generations after which the infection stage will start
        :param max_generations: The maximum number of generations that can be created. Including all phases of the game
        :param seed: initial state of the world
        """
        #if isinstance(seed, types.)
        if width * height != len(seed):
            raise ValueError('width * height({}) not equal to size of seed({})'.format(width * height, len(seed)))
        if type(seed) == type([]): #is a list
            seed = np.asarray(seed)
        seed = seed.reshape(height, width)
        s.width = width
        s.height = height
        s.data = seed
        s.stage = 0
        s.max_gen = max_generations
        s.infect_after = infect_after
        s.rules = {
            'original' : GOF_rules.OriginalRules(),
            'infection' :  GOF_rules.InfectionRules()
        }
        s.curr_rule = s.rules['original']

    def __iter__(s):
        return s

    def __next__(s):
        if s.stage >= s.max_gen:
            raise StopIteration

        if s.stage > 0:
            s.curr_rule = s.rules['infection'] if s.stage >= s.infect_after else s.rules['original']
            s.playStage()

        s.stage +=1

        return s.data.ravel() #1D flattened view


    def playStage(s):
        s.data = s.curr_rule.apply(s.data)



def func_name():
    import traceback
    return traceback.extract_stack(None, 2)[0][2]

def GameIntiation(width, height, infect_after, max_generations, seed):
    try:
        game_inst = GameOfLife(width, height, infect_after, max_generations, seed)
        for step in game_inst:
            print(step)
    except Exception as ex:
        print("exception: {}".format(ex))

def StartSession(args):
    if len(args) != 5:
        print ('Error in usage - needs to supply 5 arguments, only {} supplied'.format(len(args)))
        sys.exit(2)
    width, height, infect_after, max_generations, seed = int(args[0]) , int(args[1]), int(args[2]), int(args[3]), args[4]
    seed = seed.split()
    seed = [int(i) for i in seed]

    print ("seed is " + str(seed))
    print ("seed type is " + str(type(seed[0])))
    game_inst = GameOfLife(width, height, infect_after, max_generations, seed)
    try:
        for step in game_inst:
            print(step)
    except Exception as ex:
        print("exception: {}".format(ex))


def test_game_of_life():
    print("-------------------------------")
    print(func_name())
    width, height, infect_after, max_generations, seed = 2 ,3 ,3, 6, [1, 0, 0, 1, 1, 1]
    GameIntiation(width, height, infect_after, max_generations, seed)

def test_reference_input():
    print("-------------------------------")
    print(func_name())
    width, height, infect_after, max_generations, seed = 3, 3, 3, 6, [0,0,0,1,0,0,1,0,1]
    GameIntiation(width, height, infect_after, max_generations, seed)

def main(args):
    StartSession(args)
    #test_reference_input()
    #test_game_of_life()



import sys
if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
