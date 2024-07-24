### Case Study - Simulating a container
***


    Process: { move_containers_from_vessels, move_container_to_yard }
    Resources: { Berths[2], Trucks[3], Cranes[2] }
    Event: { crane_request, truck_request, berth_request }
    Environment: { ContainerSimulation }
    
    Container terminal has limited number of resources {berths, cranes, and trucks} to operate the containers in parallel.
    
***
1.  Scenario of Vessels and Berths: 
***
            vessels are coming in an interval, i.e. exponentially distributed with an average time of [u = 5hrs] = 5 * 60 mins
            vessels will be queued and request for berth, 
                if no berth allocated[busy/not_in_service] to vessel:
                    wait_for_berth()
                    if berth get freed: 
                        allocate to vessel at front in the queue
                        move_containers_from_vessels()
                        leave_the_berth()
                else: 
                    allocate to vessel at front in the queue
                    move_containers_from_vessels()
                    leave_the_berth()
            
***
2.  Scenario of Containers and Cranes: move_containers_from_vessels()
***
            All containers numbered from [1-150] will be queued and request for the crane [2 cranes available] to be allocated
            for every container on a vessel: 
                wait_for_crane()
                if crane available to container: 
                    wait_for_truck()
                    if truck available to crane:
                        move_container_to_truck(3 minutes required)
                        move_container_to_yard()
                        release_truck()
                else:
                    wait_for_the_crane()
                    recontinue_from_same_container
                    
***       
3.  Scenario of Crane and Trucks: move_container_to_yard()
***
            Truck take 6 minutes to drop the container to yard block and return.

<br><br>



```python

```
