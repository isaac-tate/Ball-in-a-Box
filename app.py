import pygame
from pygame import mouse

WINDOW_SHAPE = (800, 500)
BALL_RADIUS = 50
FPS = 100
GRAVITY = 9.8/(FPS//3)
WALL_LOSS_RATIO = 0.8


#START
pygame.init()
window = pygame.display.set_mode(WINDOW_SHAPE)
clock = pygame.time.Clock()
running = True

ball_location = (WINDOW_SHAPE[0]//2, WINDOW_SHAPE[1]//2)
ball_velocity = (0, 0) #(x, y)

def draw_ball(ball_location, ball_velocity, clicked=False):

    new_velocity = ball_velocity
    new_location = ball_location

    #check bottom bountry
    if ball_location[1] + BALL_RADIUS > WINDOW_SHAPE[1]:
        new_velocity = (ball_velocity[0] * WALL_LOSS_RATIO, -ball_velocity[1] * WALL_LOSS_RATIO)
        new_location = (ball_location[0] + new_velocity[0], WINDOW_SHAPE[1]-BALL_RADIUS)
        print("BOTTOM")

    #Check top boundry
    elif ball_location[1] - BALL_RADIUS < 0:
        new_velocity = (ball_velocity[0] * WALL_LOSS_RATIO, -ball_velocity[1] * WALL_LOSS_RATIO)
        new_location = (ball_location[0] + new_velocity[0], BALL_RADIUS)
        print("TOP")

    #Check left boundry
    elif ball_location[0] - BALL_RADIUS < 0:
        new_velocity = (-ball_velocity[0] * WALL_LOSS_RATIO, ball_velocity[1])
        new_location = (BALL_RADIUS, ball_location[1] + new_velocity[1])
        print("LEFT")

    #Check right boundry
    elif ball_location[0] + BALL_RADIUS > WINDOW_SHAPE[0]:
        new_velocity = (-ball_velocity[0] * WALL_LOSS_RATIO, ball_velocity[1])
        new_location = (WINDOW_SHAPE[0]-BALL_RADIUS, ball_location[1] + new_velocity[1])
        print("RIGHT")

    else:
        #Adjust velocity for grtavity
        this_gravity = GRAVITY
        if clicked:
            this_gravity = 0

        new_velocity = (ball_velocity[0], ball_velocity[1] + this_gravity)
        new_location = (ball_location[0] + new_velocity[0], ball_location[1] + new_velocity[1])


    pygame.draw.circle(window, (0, 255, 0), new_location, BALL_RADIUS)

    #return new values
    return (new_location, new_velocity)

movement = []
clicked = False

while running:

    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if (mouse_pos[0] > ball_location[0] - BALL_RADIUS) and (mouse_pos[0] < ball_location[0] + BALL_RADIUS):
                if (mouse_pos[1] > ball_location[1] - BALL_RADIUS) and (mouse_pos[1] < ball_location[1] + BALL_RADIUS):
                    print("BALL CLICKED")
                    clicked = True

        if event.type == pygame.MOUSEBUTTONUP:
            try:
                clicked = False
                x_vel = (movement[-1][0] - movement[-5][0])/5
                y_vel = ((movement[-1][1] - movement[-5][1])/5)

                ball_location = mouse_pos
                ball_velocity = (x_vel, y_vel)

                movement = []
            except:
                print("No movement")

 
    #Draw background
    window.fill((255, 255, 255))

    if clicked:
        movement.append(mouse_pos)
        new_ball_values = draw_ball(mouse_pos, (0, 0), clicked=True)

    else:
        #Update ball
        new_ball_values = draw_ball(ball_location, ball_velocity)
        ball_location = new_ball_values[0]
        ball_velocity = new_ball_values[1]

    pygame.display.flip()
    clock.tick(FPS)

