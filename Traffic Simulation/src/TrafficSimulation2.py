import xml.etree.ElementTree as ET

# checkLightState function
# attributes:
#   light - the current state of the light
#   time - the current time
# Precondition: 
#   There exists a light element, and a current time variable
# Postcondition
#   Returns True if given light element should be green at the current time, false otherwise

def checkLightState(light, time):
    cycleIteration = int(time / light["cycle"])
    if (cycleIteration % 2 == 0):
        return False # Assumes red light initial value
    else:
        return True

# Element class›
# attributes:
#   attributeListDictionary - dictionary of attributes
#   elementType -
# methods:
#   Append
#   __getitem__ overload
#   __str__ overload

class Element:
    # Constructor
    # parameters:
    #   attributeTypeList - list of dictionary keys
    #   attributeValueList - list of dictionary values
    # precondition:
    #   new Element instance does not exist
    # postcondition:
    #   new Element instance exists with attributeValueList
    #   defined by parameters
    def __init__(self, elementType="VEHICLE", attributeTypeList=[], attributeValueList=[]):
        assert len(attributeTypeList) == len(attributeValueList)
        assert elementType in ["VEHICLE", "TRAFFIC LIGHT", "ROAD", "VEHICLE GENERATOR", "BUSSTOP", "CROSSROADS"]
        self.attributeListDictionary = {}
        self.elementType = elementType
        for i in range(0, len(attributeTypeList)):
            self.attributeListDictionary.update({attributeTypeList[i]: attributeValueList[i]})

    # Append
    # parameters:
    #   attributeType
    #   attributeValue
    # precondition:
    #   none
    # postcondition:
    #   attributeListDictioary has been updated
    #   with a new entry defined by the
    #   parameters
    def Append(self, attributeType, attributeValue):
        self.attributeListDictionary.update({attributeType: attributeValue})

    # __getitem__
    # parameters:
    #   attributeType
    # precondition:
    #   attributeValueList contains an entry with the [attributeType] key
    # postcondition:
    #   none
    # returns:
    #   the value referenced by the [attributeType] key
    def __getitem__(self, attributeType):
        assert attributeType in self.attributeListDictionary
        return self.attributeListDictionary[attributeType]

    # __str__
    # parameters:
    #   none
    # precondition:
    #   none
    # postcondition:
    #   none
    # returns:
    #   attributeListDictionary.__str__()
    def __str__(self):
        return f'{self.elementType} {self.attributeListDictionary}'

# TrafficSystem class
# attributes:
#   roadList - list of roads
#   trafficLightList - list of traffic lights
#  vehicleList - list of vehicles
# methods:
#   GetElementsByAttributeType
#   PrintElements
#   AppendElement
#   ReadElementsFromFile

class TrafficSystem:
    def __init__(self):
        self.roadList = []
        self.trafficLightList = []
        self.busStopList = []
        self.vehicleList = []
        self.vehicleGeneratorList = []
        self.errorList = []   
        self.intersectionList = []  # This is 2D array

    def generateSimpleOutputString(self, time):
        output = ""
        for road in self.roadList:
            # Initialize Output Strings
            roadString = "|"
            trafficLightString = "|"
            busStopString = "|"
            for i in range(0, road["length"]):
                roadString = roadString + '='
                trafficLightString = trafficLightString + " "
                busStopString = busStopString + " "
            roadString = roadString + "|"
            trafficLightString = trafficLightString + "|"
            busStopString = busStopString + "|"
            # Fetch vehicles
            for vehicle in self.vehicleList:
                if (vehicle["road"] == road["name"]):
                    if (vehicle["type"] == "car"):
                        roadString = roadString[:vehicle["position"] + 1] + 'C' + roadString[vehicle["position"] + 2:]
                    elif (vehicle["type"] == "bus"):
                        roadString = roadString[:vehicle["position"] + 1] + 'B' + roadString[vehicle["position"] + 2:]
                    elif (vehicle["type"] == "fire truck"):
                        roadString = roadString[:vehicle["position"] + 1] + 'F' + roadString[vehicle["position"] + 2:]
                    elif (vehicle["type"] == "ambulance"):
                        roadString = roadString[:vehicle["position"] + 1] + 'A' + roadString[vehicle["position"] + 2:]
                    elif (vehicle["type"] == "police van"):
                        roadString = roadString[:vehicle["position"] + 1] + 'P' + roadString[vehicle["position"] + 2:]
                    else:
                        roadString = roadString[:vehicle["position"] + 1] + '?' + roadString[vehicle["position"] + 2:]
            # Fetch traffic lights
            for trafficLight in self.trafficLightList:
                if (trafficLight["road"] == road["name"]):
                    # Insert variable 'state' equal to current state of light
                    trafficLightIsGreen = checkLightState(trafficLight, time)
                    if (trafficLightIsGreen):
                         trafficLightString = trafficLightString[:trafficLight["position"] + 1] + "G" + trafficLightString[trafficLight["position"] + 2:]
                    else:
                         trafficLightString = trafficLightString[:trafficLight["position"] + 1] + "R" + trafficLightString[trafficLight["position"] + 2:]
            # Fetch bus stops
            for busStop in self.busStopList:
                 if (busStop["road"] == road["name"]):
                      if (trafficLightString[busStop["position"]] == ' '):
                           trafficLightString = trafficLightString[:busStop["position"] + 1] + "|" + trafficLightString[busStop["position"] + 2:]
                 busStopString = busStopString[:busStop["position"] + 1] + "B" + busStopString[busStop["position"] + 2:]
                      
            output = output + "\n" + road["name"] + "\n"
            output = output + " > road          " + roadString + "\n"
            output = output + " > trafficLights " + trafficLightString + "\n"
            output = output + " > bus stops     " + busStopString + "\n"
        return output

    def RenderSimpleGraphicsToFile(self, time, fileName):
        f = open(fileName, "w")
        f.write(self.generateSimpleOutputString(time))
        f.close()
        return self.generateSimpleOutputString(time)

    def ReadElementsFromFile(self, fileName):
        tree = ET.parse(fileName)
        root = tree.getroot()

        for elem in root:
            if elem.tag == "ROAD":
                #error checking for invalid attributes of element - this is done for each element type
                for subelem in elem:
                    if subelem.tag != "name" and subelem.tag != "length":
                        self.errorList.append("- \"" + subelem.tag + "\" is not an acceptable attribute of \"" + elem.tag + "\"")
                name = elem.find("name").text
                length = int(elem.find("length").text)
                self.roadList.append({"name": name, "length": length})
            elif elem.tag == "TRAFFICLIGHT":
                for subelem in elem:
                    if subelem.tag != "road" and subelem.tag != "position" and subelem.tag != "cycle":
                        self.errorList.append("- \"" + subelem.tag + "\" is not an acceptable attribute of \"" + elem.tag + "\"")
                road = elem.find("road").text
                position = int(elem.find("position").text)
                cycle = int(elem.find("cycle").text)
                self.trafficLightList.append({"road": road, "position": position, "cycle": cycle})
            elif elem.tag == "BUSSTOP":
                for subelem in elem:
                    if subelem.tag != "road" and subelem.tag != "position" and subelem.tag != "cycle":
                        self.errorList.append("- \"" + subelem.tag + "\" is not an acceptable attribute of \"" + elem.tag + "\"")
                name = elem.find("road").text
                position = int(elem.find("position").text)
                waitingtime = int(elem.find("waitingtime").text)
                self.busStopList.append({"road": name, "position": position, "waitingtime": waitingtime})    
            elif elem.tag == "VEHICLE":
                type = None #if a type is recognized it will be updated - these can be removed down the road when/if type becomes required
                for subelem in elem:
                    if subelem.tag != "road" and subelem.tag != "position" and subelem.tag != "speed" and subelem.tag != "acceleration" and subelem.tag != "type":
                        self.errorList.append("- \"" + subelem.tag + "\" is not an acceptable attribute of \"" + elem.tag + "\"")
                    if subelem.tag == "type":
                        type = elem.find("type").text   #recognized a type in the vehicle element so found it - finding when its not there throws an error
                road = elem.find("road").text
                position = int(elem.find("position").text)
                if (elem.find("speed") is not None and '.' in elem.find("speed").text) or (elem.find("acceleration") is not None and '.' in elem.find("acceleration").text):
                    speed = float(elem.find("speed").text)
                    acceleration = float(elem.find("acceleration").text)
                else:
                    speed = int(elem.find("speed").text)
                    acceleration = int(elem.find("acceleration").text)
                self.vehicleList.append({"road": road, "position": position, "speed": speed, "acceleration": acceleration, "type": type})
            elif elem.tag == "VEHICLEGENERATOR":
                type = None 
                for subelem in elem:
                    if subelem.tag != "name" and subelem.tag != "frequency" and subelem.tag != "speed" and subelem.tag != "acceleration" and subelem.tag != "type":
                        self.errorList.append("- \"" + subelem.tag + "\" is not an acceptable attribute of \"" + elem.tag + "\"")
                    if subelem.tag == "type":
                        type = elem.find("type").text
                name = elem.find("name").text
                frequency = int(elem.find("frequency").text)
                speed = int(elem.find("speed").text)
                acceleration = float(elem.find("acceleration").text)
                type = elem.find("type").text
                self.vehicleGeneratorList.append({"name": name, "frequency": frequency, "speed": speed, "acceleration": acceleration, "type": type})
            elif elem.tag == "CROSSROADS":
                temp_list = []
                # iterate through the child elements of the CROSSROADS element
                for subelem in elem:
                    # check if the child element is a road element
                    if subelem.tag == "road":
                        # get the position attribute and text of the road element
                        position = subelem.get("position")
                        road = subelem.text
                        # add the intersection to the intersection list
                        temp_list.append({"position": int(position), "road": road})
                    else:
                        # handle the case where the child element is not a road element
                        error_msg = "- \"" + subelem.tag + "\" is not an acceptable attribute of \"" + elem.tag + "\""
                        self.errorList.append(error_msg)

                self.intersectionList.append(temp_list)
            
            

    
            #checking for unacceptable element input
            else:
                self.errorList.append("- \"" + elem.tag + "\" is not an acceptable element")
        
        #checking if simulation is consistent
        #rule 1 - each vehicle must be on existing road
        vehicles = self.vehicleList
        roads = self.roadList
        deleteIndexList = []
        for i in range(len(vehicles)):             #iterating through all the vehicles    
            thisRoad = vehicles[i]["road"]         #finding name of road vehicle is on
            onRoad = False                         #this is our flag for if we find the road it's on
            for x in range(len(roads)):            #iterating through our list of roads 
                if thisRoad == roads[x]["name"]:   #found the road car is on
                    onRoad = True
            if onRoad == False:                    #if the vehicle is not on road, remove it from list
                deleteIndexList.append(i)          #cannot remove vehicles now or will damage outer loop - keeping track of index instead
                self.errorList.append("- A vehicle was found on the road \"" + thisRoad + "\" which does not exist")       #error message    
        #now delete all the vehicles not on a road referring to our deleteIndexList
        for i in sorted(deleteIndexList, reverse = True):   #deleting larger numbers first so it does not reassign indexes
            del self.vehicleList[i]
        
        #rule 2 - each traffic light must be on existing road
        #follows the same logic as above - will probably create an onExistingRoad function to make it more readable and efficient 
        trafficLights = self.trafficLightList
        roads = self.roadList
        deleteIndexList = []
        for i in range(len(trafficLights)):                
            thisRoad = trafficLights[i]["road"]         
            onRoad = False                         
            for x in range(len(roads)):            
                if thisRoad == roads[x]["name"]:  
                    onRoad = True
            if onRoad == False:                    
                deleteIndexList.append(i)          
                self.errorList.append("- A traffic light was found on the road \"" + thisRoad + "\" which does not exist")         
        for i in sorted(deleteIndexList, reverse = True):  
            del self.trafficLightList[i]

        #rule 3 - each vehicle generator must be on existing road
        # vehicleGenerators = self.vehicleGeneratorList
        # roads = self.roadList
        # deleteIndexList = []
        # for i in range(len(vehicleGenerators)):                
        #     thisRoad = vehicleGenerators[i]["name"]         
        #     onRoad = False                         
        #     for x in range(len(roads)):            
        #         if thisRoad == roads[x]["name"]:  
        #             onRoad = True
        #     if onRoad == False:                    
        #         deleteIndexList.append(i)          
        #         self.errorList.append("- A vehicle generator was found on the road \"" + thisRoad + "\" which does not exist")         
        # for i in sorted(deleteIndexList, reverse = True):  
        #     del self.vehicleGeneratorList[i]

        #rule 4 - The position of each vehicle is less than the length of the road.
        vehicles = self.vehicleList
        roads = self.roadList
        deleteIndexList = []
        for i in range(len(vehicles)):             
            thisPosition = vehicles[i]["position"]                  #iterate through cars finding road & position
            thisRoad = vehicles[i]["road"]       
            isLess = False                         
            for x in range(len(roads)):                             #iterating through roads until we find a match
                if thisRoad == roads[x]["name"]:                    #found the road car is on
                    if thisPosition < roads[x]["length"]:           #now checking position is less than road length
                        isLess = True
            if isLess == False:                    #if the vehicle position greater than lenght, remove it 
                deleteIndexList.append(i)         
                self.errorList.append("- A vehicle was found with a position not on it's road \"" + thisRoad + "\" ")       
        #delete all the vehicles not on a road referring to our deleteIndexList
        for i in sorted(deleteIndexList, reverse = True):   
            del self.vehicleList[i]

        #rule 5 - The position of each traffic light is less than the length of the road.
        trafficLights = self.trafficLightList
        roads = self.roadList
        deleteIndexList = []
        for i in range(len(trafficLights)):                
            thisRoad = trafficLights[i]["road"]                  #iterate through lights finding road & position
            thisPosition = trafficLights[i]["position"]       
            isLess = False                         
            for x in range(len(roads)):                             #iterating through roads until we find a match
                if thisRoad == roads[x]["name"]:                    #found the road car is on
                    if thisPosition < roads[x]["length"]:           #now checking position is less than road length
                        isLess = True
            if isLess == False:                    #if the vehicle position greater than lenght, remove it 
                deleteIndexList.append(i)         
                self.errorList.append("- A traffic light was found with a position not on it's road \"" + thisRoad + "\" ")       
        #delete all the vehicles not on a road referring to our deleteIndexList
        for i in sorted(deleteIndexList, reverse = True):   
            del self.trafficLightList[i]
            
        # Rule 6 - There is a maximum of one vehicle generator on each road
        vehicleGenerators = self.vehicleGeneratorList
        roads = self.roadList
        deleteIndexList = []
        for i in range(len(vehicleGenerators)):           # Iterate through generators finding road it is on
            thisRoad = vehicleGenerators[i]["name"]
            hasGen = False                                
            for x in range(len(roads)):                   # Iterate through roads to find match
                if thisRoad == roads[x]["name"]:          # Found generator on road
                    hasGen = True
            if hasGen == True:                            # If road already has a generator, max generators has been met
                max = True
            if max == True:
                deleteIndexList.append(i)
                self.errorList.append("- This road: " + thisRoad + " has max amount of vehicle generators.")
        for i in sorted(deleteIndexList, reverse = True):
            del self.vehicleGeneratorList[i]

        # Rule 7 - A traffic light must not be within the deceleration distance of another traffic light
        trafficLights = self.trafficLightList
        roads = self.roadList
        deleteIndexList = []
        for i in range(len(trafficLights)):                # Iterate to find road and position of traffic light
            thisRoad = trafficLights[i]["road"]         
            thisPosition = trafficLights[i]["position"]
            thisLight = trafficLights[i]
            for x in range(i + 1, len(trafficLights)):            
                otherRoad = trafficLights[x]["road"]         
                otherPosition = trafficLights[x]["position"]
                otherLight = trafficLights[x]
            if thisRoad == otherRoad:                    
                distance = abs(thisPosition - otherPosition)
                if distance < 30:                           # 30 is deceleration distance
                    deleteIndexList.append(i)
                    self.errorList.append("- Traffic light " + thisLight + " is within deceleration distance of traffic light " + otherLight + ".")

        for i in sorted(deleteIndexList, reverse = True):  
            del self.trafficLightList[i]
