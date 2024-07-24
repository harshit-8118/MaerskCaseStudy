# MaerskCaseStudy


# Work in progress until deadline, 
# Please don't judge it too hurry, Nicer code is in my machine. 

### Case Study - Simulating a container
***


    Process: { Process for unloading containers from vessels, Process for loading containers onto the truck }
    Resource: { Berths[2], Trucks[3], Cranes[2] }
    Event: { Request for berth, Request for truck, Request for crane }
    Environment: { Container terminal }
    
    Container terminal has limited number of resources {berths, cranes, and trucks} to operate the containers in parallel.
    
***
1.  Scenario of Vessels and Berths: 
***
            vessels are coming with probability, i.e. exponentially distributed with an average time of [u = 5hrs] = 5 * 60 mins
            vessels that came to terminal, note their arrival time
            vessels will be queued and request for berth, 
                if no berth allocated[busy/not_in_service] to vessel:
                    vessel wait_for_berth()
                    if any berth freed: 
                        note its berthing time
                        give it to vessel at front in the queue
                        Process_for_unloading_container()
                        leave_the_berth()
                else: 
                    note its berthing time
                    give it to vessel at front in the queue
                    Process_for_unloading_container()
                    leave_the_berth()
            
***
2.  Scenario of Containers and Cranes: Process_for_unloading_containers()
***
            All containers numbered from [1-150] will be queued and request for the crane [2 cranes available] to be allocated
                if crane available to container: 
                    crane will pick a container at front at a time
                    3 minutes of time will elapsed by the crane to move container + waiting time for truck.
                    Process_for_loading_container_on_truck()
                else:
                    wait_for_the_crane()
                    
***       
3.  Scenario of Crane and Trucks: Process_for_loading_container_on_truck()
***
            Cranes request for the truck [3 trucks available] truck's service time per container is 6 minutes.
                if atleast truck available: 
                    crane queued at front will get the truck and load the container.
                    Truck take 6 minutes to drop the container to yard block and return.

***
Flow diagram: 
![image](https://github.com/user-attachments/assets/9279b72f-4037-42bb-953e-69995e174903)
            
<br><br>
