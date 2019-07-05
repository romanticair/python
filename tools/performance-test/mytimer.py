"""
version 2

timer(spam, 1, 2, a=3, b=4, _reps=1000) calls and times spam(1, 2, a=3)
_reps times, and returns total time for all runs, with final result;

best(spam, 1, 2, a=3, b=4, _reps=50) runs best-of-N timer to filter out
any system load variation, and returns best time among _reps tests
"""
import time, sys

# timefunc = time.clock if sys.platform[:3] == 'win' else time.time
if sys.platform[:3] == 'win':
    timefunc = time.clock
else:
    timefunc = time.time


def trace(*args):
    print(args)


def timer(func, *pargs, **kargs):
    _reps = kargs.pop('_reps', 1000)  # Passed-in of default reps
    trace(func, pargs, kargs, _reps)
    repslist = range(_reps)  # Hoist range out for 2.6 lists
    start = timefunc()
    for i in repslist:
        ret = func(*pargs, **kargs)
    elapsed = timefunc() - start
    return elapsed, ret


def best(func, *pargs, **kargs):
    _reps = kargs.pop('_reps', 50)
    best = 2 ** 32
    for i in range(_reps):
        (time, ret) = timer(func, *pargs, _reps=1, **kargs)
        if time < best:
            best = time
    return best, ret
    

"""
reps = 1000
resplist = range(reps)

def timer(func, *paras, **kargs):
    start = time.clock()
    for i in resplist:
        ret = func(*paras, **kargs)
    elapsed = time.clock() - start
    return (elapsed, ret)
"""
