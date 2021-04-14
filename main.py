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

def clamp_norm(v, n_max):
    vx = v[0]
    vy = v[1]
    n = math.sqrt(vx**2 + vy**2)
    if n == 0:
        return 0
    f = min(n, n_max) / n
    return np.array([f * vx, f * vy])

#drawing on the screen : we draw each cells and each agent
def draw_window(state):
    for cell in state.cells:
        drawCell(cell, state.max_water_capacity)
    for agent in state.agents:
        drawAgent(agent)
    pygame.display.update()


#drawing the cells : we are drawing the water resources on the map
def drawCell(cell, max_water_capacity):
        #drawing a water pit, its radius depends on the number of left water
        pygame.draw.circle(SCREEN, (0, 0, 255), cell.pos, pit_radius(cell.water / max_water_capacity))

#drawing the agents : 
def drawAgent(agent):
    #an agent will be represented as a circle on the screen
    pygame.draw.circle(SCREEN, (127, 127, 0), agent.pos, 4)

#updating the states will be done with the logs from the simulation.
# For visualisation we will for now simulate a very simple behaviour...
def updateAgent(state):
    for agent in state.agents:
        #verify that agent can still move in its current direction : he does not hit a border
        #if (agent.pos + agent.vel).any() > np.array([WIDTH, HEIGHT]).any() or (agent.pos + agent.vel).any() < np.array([0, 0]).any():
            #if so, the agent goes in opposit direction (as I said it's very simple only to visualise...)
            #agent.vel = -agent.vel
        #we now must verify that the agent does not hit a water pit
        #for cell in state.cells:
            #computing the distance between water pit's center and agent's center
            #dist = math.hypot(agent.pos[0]-cell.pos[0], agent.pos[1]-cell.pos[1])
            #if the distance is lower than the radius, then again change the direction
            #if dist < pit_radius(cell.water / state.max_water_capacity):
                #agent.vel[0] = -agent.vel[0]
                #agent.vel[1] = -agent.vel[1]
        #finally update the new positions
        temp = agent.desired_pos - agent.pos
        desiredDirection = temp / np.linalg.norm(temp)

        desiredVelocity = desiredDirection * AGENT_MAX_SPEED
        desiredSteeringForce = (desiredVelocity - agent.vel) * AGENT_STEER_STRENGTH
        acceleration = clamp_norm(desiredSteeringForce, AGENT_STEER_STRENGTH) / 1

        agent.vel = clamp_norm(agent.vel + acceleration, AGENT_MAX_SPEED) / 1
        agent.pos = agent.pos + agent.vel

def main():

    state = State("/Users/tancrede/Desktop/projects/survival_simulation/data.json")

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        nexttime = True
        for agent in state.agents:
            if not (np.isclose(agent.desired_pos, agent.pos, rtol=1e-05, atol=2).all()):
                nexttime = False
        if nexttime:
            state.load()

        draw_window(state)
        updateAgent(state)
        SCREEN.fill(BLACK)
        
    pygame.quit()


if __name__ == "__main__":
    main()
