import sys, pygame, math
import numpy as np
from simulationState import State

WIDTH = 900
HEIGHT = 600
SIZE = (WIDTH, HEIGHT)
SCREEN = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Survival")

FPS = 60
BLACK = (0, 0, 0)

PIT_MAX_RADIUS = 50
AGENT_MAX_SPEED = 2
AGENT_STEER_STRENGTH = 2
AGENTS_WANDER_STRENGTH = 0.5

def colorPercentage(n):
    return 255 * (n / 100.0)

def pit_radius(water_percentage):
    return PIT_MAX_RADIUS * water_percentage


#drawing on the screen : we draw each cells and each agent
def draw_window(state):
    for cell in state.cells:
        drawCell(cell, state.max_water_capacity)
    for agent in state.agents:
        drawAgent(agent)
    pygame.display.update()


#drawing the cells : we are drawing the water resources on the map
def drawCell(cell, max_water_capacity):
        x = cell.x
        y = cell.y
        #drawing a water pit, its radius depends on the number of left water
        pygame.draw.circle(SCREEN, (0, 0, 255), (x, y), pit_radius(cell.water / max_water_capacity))

#drawing the agents : 
def drawAgent(agent):
    center = (agent.x, agent.y)
    #an agent will be represented as a circle on the screen
    pygame.draw.circle(SCREEN, (127, 127, 0), center, 4)

#updating the states will be done with the logs from the simulation.
# For visualisation we will for now simulate a very simple behaviour...
def updateAgent(state):
    for agent in state.agents:
        #verify that agent can still move in its current direction : he does not hit a border
        if agent.x + agent.vx > WIDTH or agent.x + agent.vx < 0:
            #if so, the agent goes in opposit direction (as I said it's very simple only to visualise...)
            agent.vx = -agent.vx
        #same thing for y direction
        if agent.y + agent.vy > HEIGHT or agent.y + agent.vy < 0:
            agent.vy = -agent.vy
        #we now must verify that the agent does not hit a water pit
        for cell in state.cells:
            #computing the distance between water pit's center and agent's center
            dist = math.hypot(agent.x-cell.x, agent.y-cell.y)
            #if the distance is lower than the radius, then again change the direction
            if dist < pit_radius(cell.water / state.max_water_capacity):
                agent.vx = -agent.vx
                agent.vy = -agent.vy
        #finally update the new positions
        desiredDirection = 
        agent.x += agent.vx
        agent.y += agent.vy

def main():


    time = 0
    state = State("/Users/tancrede/Desktop/projects/survival_simulation/data.json")

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        #state.load(time)
        draw_window(state)
        updateAgent(state)
        SCREEN.fill(BLACK)
        
    pygame.quit()


if __name__ == "__main__":
    main()
