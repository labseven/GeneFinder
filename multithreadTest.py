import time
from multiprocessing import Pool

def slow_func(time):
    total = 0
    for i in range(time * 10**10):
        total += total

    return 1

if __name__ == "__main__":
    slow_func(1)
    print time.clock()
