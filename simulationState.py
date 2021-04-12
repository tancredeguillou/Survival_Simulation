import json
import numpy as np

class Cell():

    def __init__(self, x, y, water):
        self.pos = np.array([x, y])
        self.water = water

class Agent():

    def __init__(self, id, x, y, desired_x, desired_y, inventory):
        self.pos = np.array([x, y])
        self.desired_pos = np.array([desired_x, desired_y])
        self.vel = np.array([0, 0])
        self.inventory = inventory
        #id seems to be artificial here
        self.id = id


class State():

    def __init__(self, file):
        #opening the json file
        f = open(file)

        #getting the dictionary
        data = json.load(f)

        self.file = file
        self.max_water_capacity = data['max_water_capacity']
        self.max_time = data['max_time']

        f.close()

        self.agents = []
        self.time = 0
        self.max_agent = 50
        self.load()

    def load(self):
        #reinitialize agents and cells
        self.cells = []
        #temporary array as we want to keep track of the velocity
        newAgents = []

        #opening the json file
        f = open(self.file)

        #getting the dictionary
        data = json.load(f)

        for d in data['tick_line']:
            if d['tick_number'] == self.time:
                for agent in d['agents']:
                    newAgents.append(Agent(agent['id'], agent['x'], agent['y'], agent['desired_x'], agent['desired_y'], agent['inventory']))
                for cell in d['cells']:
                    self.cells.append(Cell(cell['x'], cell['y'], cell['water']))
        
        i = 0
        for agent in self.agents:
            newAgents[i].vel = agent.vel
            i += 1
        self.agents = newAgents

        f.close()

        if self.time == self.max_time:
            self.time = 0
        else:
            self.time += 1
