import simpy

import sys
sys.stdout = open('output.txt', 'w')

def traffic(env):
    while(True):
        print('Turn GRN light on' + str(env.now))
        yield env.timeout(30)
        print('Turn YLW light on' + str(env.now))
        yield env.timeout(5)
        print('Turn RED light on' + str(env.now))
        yield env.timeout(20)
    
env = simpy.Environment()
env.process(traffic(env))
env.run(until=120)