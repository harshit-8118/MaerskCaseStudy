import simpy

import sys
sys.stdout = open('output.txt', 'w')

def alarm(env):
    while(True):
        yield env.timeout(10)
        print( "Time to wake up!" )


def alarm_2(env):
    while(True):
        yield env.timeout(200)
        print( "Time to wake up again!" )


env = simpy.Environment()
env.process(alarm(env ))
env.process(alarm_2(env))
env.run(until=1001)