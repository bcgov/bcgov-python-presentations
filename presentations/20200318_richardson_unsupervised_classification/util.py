# some deps, and parfor function for using all cores!
import os  # operating system
import sys  # system functions
import copy  # copy an object
import math  # basic math
import pickle # pickle library, to save results
from vpython import *  # python vis
import colorsys  # color transformations
import multiprocessing as mp  # multithreading
from random import random as random  # random number generator
args = sys.argv  # command line arguments

def err(msg):
    print('Error: ' + str(msg))
    sys.exit(1)

def parfor(my_function, my_inputs):  # evaluate function in parallel
    return mp.Pool(mp.cpu_count()).map(my_function, my_inputs)
