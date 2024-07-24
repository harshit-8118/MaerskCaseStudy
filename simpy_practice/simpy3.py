import simpy
import random
import sys
from datetime import datetime, timedelta

sys.stdout = open('output.txt', 'w')

class Car:
    def __init__(self, env, gas_station, name):
        self.env = env
        self.gas_station = gas_station
        self.name = name        

    def refuel(self):
        yield self.env.timeout(5)

    def action(self):
        with self.gas_station.request() as req:
            yield req
            current_time = start_time + timedelta(minutes=self.env.now)
            print(f'{current_time.strftime("%Y-%m-%d %H:%M")} - {self.name}: Arrived')
            yield from self.refuel()
            current_time = start_time + timedelta(minutes=self.env.now)
            print(f'{current_time.strftime("%Y-%m-%d %H:%M")} - {self.name}: Refueled')

def car_generator(env, gas_station):
    i = 0
    while True:
        t = random.randint(1, 10)
        yield env.timeout(t)
        car = Car(env, gas_station, f"Car {i}")
        env.process(car.action())
        i += 1

start_time = datetime(2024, 7, 23, 0, 0) 
env = simpy.Environment()
gas_station = simpy.Resource(env, 2)
env.process(car_generator(env, gas_station))
env.run(until=5000) 
