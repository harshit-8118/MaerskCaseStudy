import simpy
import random

SIMULATION_TIME = 1 * 24 * 60  # simulation time (in mins)
VESSEL_AVG_ARRIVAL_INTERVAL = 5 * 60  # vessels average arrival time (in mins)
CONTAINERS_PER_VESSEL = 150  # no of containers per vessel
AVAIL_BERTHS = 2  # no of berths
AVAIL_CRANES = 2  # no of cranes in service
AVAIL_TRUCKS = 3  # no of trucks in service
MOVE_CONTAINER_TIME = 3  # time elapsed by crane to move container to the truck (in mins)
TRUCK_TRIP_ROUND_TIME = 6  # time taken by trucks to move container to the yard (in mins)
RANDOM_SEED = 11

class ContainerSimulation:
    
    def __init__(self, env, berths, cranes, trucks):
        self.env = env
        self.berths = simpy.Resource(env, berths) 
        self.cranes = simpy.Resource(env, cranes)
        self.trucks = simpy.Resource(env, trucks)

    def now(self):
        return self.env.now
    
    def process_for_unloading_containers(self, vessel_id):
        '''
        unloading containers process request to berth, once it berth 
        then all of its 150 containers parallely unloaded by the 2 cranes and load onto the trucks
        '''
        
        arrival = self.now()
        print(f"Vessel {vessel_id} arriving at time {arrival:.2f}")
        
        berth_request = self.berths.request()  
        ''' vessel requesting to berth '''
        yield berth_request

        t = self.now()
        vessel_waiting_time = t - arrival
        print(f'Vessel {vessel_id} waited to berth for {vessel_waiting_time:.2f}')  # amount of time passed to berth the vessel at terminal
        print(f"Vessel {vessel_id} berthing at time {t:.2f}")
        
        for container_no in range(1, CONTAINERS_PER_VESSEL+1):
                crane_req = self.cranes.request()
                ''' container requesting for crane '''
                yield crane_req
                yield self.env.process(self.Process_for_loading_container_on_truck(vessel_id, container_no))
                ''' crane released '''
                self.cranes.release(crane_req)

        ''' berth released '''
        self.berths.release(berth_request)

        t = self.now()
        vessel_turn_around_time = t - arrival
        print(f"Vessel {vessel_id} leaving at time {t:.2f}")
        print(f"Vessel {vessel_id} turn_around time is {vessel_turn_around_time:.2f}")

    def Process_for_loading_container_on_truck(self, vessel_id, container_no):
        trucks_req = self.trucks.request()
        ''' crane requesting for truck '''
        yield trucks_req
    
        print(f"Quay crane moving container {container_no} from vessel {vessel_id} at time {self.now():.2f}")
        yield self.env.timeout(MOVE_CONTAINER_TIME)  # crane moving container from the vessel
        
        print(f"Truck transporting container {container_no} from vessel {vessel_id} at time {self.now():.2f}")
        yield self.env.timeout(TRUCK_TRIP_ROUND_TIME)  # truck leaving the container to yard block
        
        print(f"Truck returned after transporting container {container_no} from vessel {vessel_id} at time {self.now():.2f}")
        ''' truck released '''
        self.trucks.release(trucks_req)
    
def vessel_generator(env):
    vessel = ContainerSimulation(env, AVAIL_BERTHS, AVAIL_CRANES, AVAIL_TRUCKS)
    
    vessel_id = 0
    while(True):
        ''' 1/avg, wait for average interval between vessel arrival '''
        yield env.timeout(random.expovariate(1 / VESSEL_AVG_ARRIVAL_INTERVAL))  
        vessel_id += 1
        env.process(vessel.process_for_unloading_containers(vessel_id))  # start process for berthing & unloading containers

if __name__ == '__main__':
    random.seed(RANDOM_SEED)

    # Create an environment and start the vessel generation
    env = simpy.Environment()
    env.process(vessel_generator(env))

    # Execute!
    env.run(SIMULATION_TIME)
