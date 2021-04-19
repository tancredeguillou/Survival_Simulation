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

    def __init__(self, file, readable=True):
        # readable is if we need to preprocess the json file since it is in a human readable format
        # the correct format is exactly one line per json object
        self.file = file # read only
        self.readable = readable

        self.data = self.read_file() # read only
        self.x_size = self.data[0]['x_size']
        self.y_size = self.data[0]['y_size']
        self.max_water_capacity = self.data[0]['max_water_capacity_cell']
        self.max_inventory = self.data[0]['max_water_capacity_agent']

        self.time = 0 # read only

        # assuming there is one line for each [0, self.max_time]
        self.max_time = len(self.data)-2
        assert(self.data[-1]['tick_number'] == self.max_time)
        self.agents = []
        self.max_agent = 10
        self.load()

    def load(self):
        #reinitialize agents and cells
        self.cells = []
        #temporary array as we want to keep track of the velocity
        newAgents = []

        d = self.data[self.time+1]
        assert(d['tick_number'] == self.time)
        #agents on the next iteration, we want to know their position
        nextTime = self.time+2
        if self.time == self.max_time:
            nextTime = 1

        desired_pos_agents = self.data[nextTime]['agents']

        j = 0 
        for agent in d['agents']:
            newAgents.append(Agent(agent['id'], agent['x'], agent['y'], desired_pos_agents[j]['x'], desired_pos_agents[j]['y'], agent['inventory']))
            j += 1
        for cell in d['cells']:
            self.cells.append(Cell(cell['x'], cell['y'], cell['water']))
        
        i = 0
        for agent in self.agents:
            newAgents[i].vel = agent.vel
            i += 1
        self.agents = newAgents

        if self.time == self.max_time:
            self.time = 0
        else:
            self.time += 1
    
    def read_file(self):
        # takes self.file and returns a list of json objects from the file
        with open(self.file) as f:
            s = f.read()
        if self.readable:
            s = self.reformat_from_readable(s)
        return [json.loads(line) for line in s.splitlines()]


    def reformat_from_readable(self, s):
        # human readable play not have exactly one line per json object
        # This uses the observation that in json }{ cannot occur in a single object
        # Note: so long as no string value containing } whitespace { appears in the json document
        return ''.join(s.split()).replace('}{', '}\n{')

    def count_survivors(self):
        return sum(1 for agent in self.agents if agent.inventory > 0)
