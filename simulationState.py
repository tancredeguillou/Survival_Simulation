import json
import numpy as np

class Cell():

    def __init__(self, x, y, water):
        self.pos = np.array(x, y)
        self.x = x
        self.y = y
        self.water = water

class Agent():

    def __init__(self, id, x, y, desired_x, desired_y, inventory):
        self.x = x
        self.y = y
        self.desired_x = x
        self.desired_y = y
        self.inventory = inventory
        self.id = id
        self.velocity_x = 0
        self.velocity_y = 0

        #For now let's pretend the agents move randomly, so we add a velocity
        #self.vx = 2
        #self.vy = 2


class State():

    def __init__(self, file):
        #opening the json file
        f = open(file)

        #getting the dictionary
        data = json.load(f)

        self.file = file
        self.max_water_capacity = data['max_water_capacity']

        f.close()

        self.time = 0
        self.max_time = 30
        self.max_agent = 50
        self.load(0)

    def load(self, time):
        #reinitialize agents and cells
        self.agents = []
        self.cells = []

        #opening the json file
        f = open(self.file)

        #getting the dictionary
        data = json.load(f)

        for d in data['tick_line']:
            if d['tick_number'] == time:
                for agent in d['agents']:
                    self.agents.append(Agent(agent['id'], agent['x'], agent['y'], agent['desired_x'], agent['desired_y'], agent['inventory']))
                for cell in d['cells']:
                    self.cells.append(Cell(cell['x'], cell['y'], cell['water']))

        f.close()
