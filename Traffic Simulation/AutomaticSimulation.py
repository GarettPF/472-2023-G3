# 3.3
from TrafficSimulation2 import *
import VehicleCalculations
import TrafficLightSimulation

# Goal: Run simulation automatically
# Precondition: The system contains a diagram of the virtual road network.
# Postcondition: The traffic in the road network is simulated.


# AutomaticSimulation contains all object lists and functions necessary for automatic simulation.
# First create AutomaticSimulation object, then call update on that object
# Atributes:
#   trafficSystem
#       - TrafficSystem object from TrafficSimulation2.py
#   vehicle_list
#       - vehicle list generated from trafficSystem
#   traffic_light_list
#       - traffic light list generated from trafficSystem
# Methods:
#   vehicle_on_road()
#       -prints all vehicles' position and road
#   traffic_light_on_road()
#       -prints all traffic lights' position and cycle
#   update()
#       -calls vehicle_on_road() and traffic_light_on_road()
class AutomaticSimulation:
    def __init__(self):
         # create a TrafficSystem object from the input file
        self.trafficSystem = TrafficSystem()
        self.trafficSystem.ReadElementsFromFile("./InputFiles/trafficSim2.xml")        
        # Get Vehicle List
        self.vehicle_list = self.trafficSystem.vehicleList
        # Get Traffic Light List
        self.traffic_light_list = self.trafficSystem.trafficLightList


    def vehicle_on_road(self):

        # 1. FOR any vehicle in the road network
        for i in range(len(self.vehicle_list)):
            # 3.1 GOES HERE
            # Execute use-case 3.1 out on the vehicle
            print("Vehicle:" , i)
            print("    -> road: ", self.vehicle_list[i]["road"])
            print("    -> position: ", self.vehicle_list[i]["position"])
            #VehicleCalculations.calculateVehicleSpeedAndPosition(i, 16.6, 100)
            #print(i)
        
    def traffic_light_on_road(self):
        
        # 2. FOR any traffic light in the road network
        for i in range(len(self.traffic_light_list)):
            print("Road: ", self.traffic_light_list[i]["road"])
            print("    -> position: ", self.traffic_light_list[i]["position"])
            print("    -> cycle: ", self.traffic_light_list[i]["cycle"])
            # TrafficLightSimulation.trafficLightInteraction(self.trafficSystem, self.vehicle_list, self.traffic_light_list[i]["cycle"])

    def update(self):
        self.vehicle_on_road()
        self.traffic_light_on_road()


simulation = AutomaticSimulation()
simulation.update()