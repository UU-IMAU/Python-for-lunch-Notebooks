# Python for lunch 6 March 2019 IMAU
# See: https://docs.python.org/2/library/profile.html for more info on cProfile

import numpy as np
import matplotlib.pyplot as plt

#import profile modules
import cProfile
import pstats

#import the class parsetting form the directory model and file module1.py
from model.module1 import parsetting as parset1
from model.module2 import parsetting as parset2

# make instance of parsetting class
ps1 = parset1()
ps2 = parset2()

#make it a bit more costly.
ps1.N=800
ps1.nn=2e6
ps2.N=1000
ps2.nn=2e6

#run profiler, output is called 'stats'
cProfile.run('ps1.solve()', 'stats1')
cProfile.run('ps2.solve()', 'stats2')

#make a pstats variable to analyse the stats
p1 = pstats.Stats('stats1')
p2 = pstats.Stats('stats2')

#sort on total time spend in the given function and print the first 10 lines.
p1.sort_stats('tottime').print_stats(10)
p2.sort_stats('tottime').print_stats(10)



#---------------------------------------------------------
# ncalls: for the number of calls.
# tottime: for the total time spent in the given function (and excluding time made in calls to sub-functions)
# percall: is the quotient of tottime divided by ncalls
# cumtime: is the cumulative time spent in this and all subfunctions (from invocation till exit). This figure is accurate even for recursive functions.
# percall: is the quotient of cumtime divided by primitive calls
# filename:lineno(function): provides the respective data of each function

# When there are two numbers in the first column (for example 3/1), it means that the function recursed. 
# The second value is the number of primitive calls and the former is the total number of calls. 
# Note that when the function does not recurse, these two values are the same, and only the single figure is printed.