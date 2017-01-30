import time
from multiprocessing import Pool
import sys
import random

if(len(sys.argv) != 3):
    raise IndexError("Two arguments needed: num_threads num_funcs")
num_threads = int(sys.argv[1])
num_funcs = int(sys.argv[2])

def slow_func(time):
    total = 0
    for i in range(time * 10**9):
        total += i

    return total


if __name__ == "__main__":
    pool = Pool(num_threads)

    print "Threads: ", num_threads, " Function runs: ", num_funcs

    start_time = time.time()
    # result = pool.apply_async(slow_func, (1,))
    # print result.get(timeout=15)


    print pool.map(slow_func, [2]*num_funcs)

    print "Time: ", time.time() - start_time
