# Author: Gaurang Patel

import math
from random import randint
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

plt.ion() # enable interactive mode (continue graphing without having to close the window)
plt.show() # show the plot

#To help in calculating the direction to move the elevator
def sign(x):
    # Return the sign of x (0 if x is 0).
    if x > 0: # x positive
        return 1
    elif x < 0: # x negative
        return -1
    else: # x zero
        return 0

#3DPoint Class
class Point3D():
    ''' 3D point representation using x,y and z coordinates'''
    def __init__(self, x, y, z): 
        #class constructor
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)
    
    def __eq__(self, other): # comparison
        return self.x == other.x and self.y == other.y and self.z == other.z
    
    def __str__(self): # string representation
        return '<{}, {}, {}>'.format(self.x, self.y, self.z)
    
    def add(self, other): # add two points together
        return Point3D(self.x+other.x, self.y+other.y, self.z+other.z)
    
    def distance(self, other): # get distance between two points
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2)
    
    def get_direction_vector(self, other):
        # Return a vecotr of 1, 0 or -1 in each dimension corresponding to the direction you would have to move from the self point to get to the other point.
        return Point3D(sign(other.x-self.x), sign(other.y-self.y), sign(other.z-self.z))
    
    def aslist(self): # Return the Point3D object as a list of three numbers.
        return [self.x, self.y, self.z]

def get_random_point(x0, x1, y0, y1, z0, z1):
    # return a Point3D object with random coordinates within the given x,y,z intervals.
    return Point3D(randint(x0, x1), randint(y0, y1), randint(z0, z1))

#Person Class
class Person:
    '''Person's info and methods with respect to wonkavator'''
    def __init__( self, name , cur_pos, dst_pos):
        # class constructor
        self.name = name
        self.cur_pos = cur_pos
        self.dst_pos = dst_pos
        self.arrived = False
    
    def arrive_at_destination(self):
        #When person reached the destination
        self.cur_pos = self.dst_pos
        self.arrived = True
        print(self.__str__())
        
    def __str__(self): # string representation
        return "Name:" + self.name + "; cur: " + str(self.cur_pos) + "; dst:" + str(self.dst_pos)

#Factory Class
class Factory:
    def __init__(self, factory_size, people, elevator): 
        # class constructor
        self.factory_size = factory_size
        self.people = people
        self.elevator = elevator 
        self.axes = plt.axes(projection='3d')
    
    #Run the elevator
    def run(self):
        '''This method is the main loop for the simulation and it operates the elevator. Particularly, this function checks if the elevator is currently in a room where there are people who want to enter the elevator, and/or if there are people in the elevator whose destination point is the current room and who thus want to leave the elevator.
        '''
        for person in self.people:
            #If there is a person(s) who are in the elevator 
            if person in elevator.people_in_elevator:
                #if the person's destination is the current room
                if elevator.cur_pos == person.dst_pos:
                    #the person need to be dropped off in that room
                    elevator.person_leaves(person)
                                       
            #Person(s) who are in the same room as the elevator and need to be picked up
            if elevator.cur_pos == person.cur_pos:
                #Person has not already arrived at their destination room
                if not person.arrived:
                    #Person gets picked up
                    elevator.person_enters(person)

        # Move the elevator until all person reach the destination
        if not self.is_finished():
            self.elevator.move(self.people)
    
    #Plotting function
    def show(self):
        self.axes.clear() # clear the previous window contents

        # set the axis bounds
        self.axes.set_xlim(0, factory_size.x)
        self.axes.set_ylim(0, factory_size.y)
        self.axes.set_zlim(0, factory_size.z)
        self.axes.set_xticks(list(range(factory_size.x+1)))
        self.axes.set_yticks(list(range(factory_size.y+1)))
        self.axes.set_zticks(list(range(factory_size.z+1)))
        
        # show a blue dot for each person not yet in the elevator / not yet arrived at their destination
        xs, ys, zs = [], [], []
        for person in self.people:
            if not person.arrived and person not in self.elevator.people_in_elevator:
                xs.append(person.cur_pos.x)
                ys.append(person.cur_pos.y)
                zs.append(person.cur_pos.z)
        self.axes.scatter3D(xs, ys, zs, color='blue')
        
        # show a red dot for the destinations of the people currently in the elevator
        edxs, edys, edzs = [], [], []
        for person in self.people:
            if person in self.elevator.people_in_elevator:
                edxs.append(person.dst_pos.x)
                edys.append(person.dst_pos.y)
                edzs.append(person.dst_pos.z)
        self.axes.scatter3D(edxs, edys, edzs, color='red')
        
        # show a green dot for the elevator itself
        self.axes.scatter3D([self.elevator.cur_pos.x], [self.elevator.cur_pos.y], [self.elevator.cur_pos.z], color='green')
        
        plt.draw()
        plt.pause(0.5)
    
    #When all person reached their destinations
    def is_finished(self):
        return all(person.arrived for person in self.people)

#Elevator Class   
class Wonkavator:
    def __init__(self, factory_size): 
        #class constructor
        self.cur_pos = Point3D(0, 0, 0)
        self.factory_size = factory_size
        self.people_in_elevator = [] # the list of people currently in the elevator
        
    def move(self, people): # move the elevator
        # get the direction in which to move      
        direction = self.choose_direction(people)
        
        # check if the direction is correct
        if any(not isinstance(d, int) for d in direction.aslist()):
            raise ValueError("Direction values must be integers.")
        if any(abs(d) > 1 for d in direction.aslist()):
            raise ValueError("Directions can only be 0 or 1 in any dimension.")
        if all(d == 0 for d in direction.aslist()):
            raise ValueError("The elevator cannot stay still (direction is 0 in all dimensions).")
        if any(d < 0 or d > s for d, s in zip(self.cur_pos.add(direction).aslist(), self.factory_size.aslist())):
            raise ValueError("The elevator cannot move outside the bounds of the grid.")
        
        # move the elevator in the correct direction
        self.cur_pos = self.cur_pos.add(direction)

    def choose_direction(self, people):
        #Choose the direction to move the elevator
        direction = None
        if len(self.people_in_elevator) == 0:  
            #No one inside elevator hence elevator should pick up a person
            #So to do that making initially closest_dist = infinity (very high value)
            closest_dist = math.inf  

            #finding the min-distance from all waiting people
            for person in people:
                #person should be waiting and not inside elevator 
                if not person.arrived and person not in self.people_in_elevator:  
                    #calculate the distance between elevator and person's waiting room
                    dist = person.cur_pos.distance(self.cur_pos)
                    # go towards the direction to whichever is closest distance (min distance)
                    if dist < closest_dist:  
                        closest_dist = dist
                        direction = self.cur_pos.get_direction_vector(person.cur_pos)
        else:  
            #drop the person whoever is closest to thier destination
            closest_dist = math.inf  
            for person in self.people_in_elevator:  
                #calculate the distance
                dist = person.dst_pos.distance(self.cur_pos)  
                if dist < closest_dist:  
                    closest_dist = dist 
                    direction = self.cur_pos.get_direction_vector(person.dst_pos)
        return direction  
        
    def person_enters(self, person): # person arrives in elevator
        if person.arrived:
            raise Exception("A person can only enter the elevator if they have not yet reached their destination.")
        self.people_in_elevator.append(person) # add them to the list
    
    def person_leaves(self, person): # person departs elevator
        if person.dst_pos != elevator.cur_pos:
            raise Exception("A person can only leave the elevator if the elevator has reached their destination point.")  
        person.arrive_at_destination() # let the person know they have arrived
        self.people_in_elevator.remove(person) # remove them from the list

#Testing the code
if __name__ == '__main__':    
    factory_size = Point3D(5, 5, 5)
    # create the people objects
    people = []
    for name in ["Candice", "Arnav", "Belle", "Cecily", "Faizah", "Nabila", "Tariq", "Benn"]:
        cur = get_random_point(0, factory_size.x-1, 0, factory_size.y-1, 0, factory_size.z-1)
        dst = get_random_point(0, factory_size.x-1, 0, factory_size.y-1, 0, factory_size.z-1)
        people.append(Person(name, cur, dst))
    
    
    # create the elevator
    elevator = Wonkavator(factory_size) #initially (<0,0,0> and [] )
    
    # create the factory
    factory = Factory(factory_size, people, elevator) #Initially (<5,5,5> [Persons Objects], Elevator Object)
    
    while True:
        factory.run()
        factory.show()
        
        # check if everyone has arrived at their destinations
        if factory.is_finished():
            break
    
    print("Everyone has arrived.")