import turtle
import random
import time

FRAME_RATE = 30
TIME_FOR_1_FRAME = 1 / FRAME_RATE

window = turtle.Screen()
window.tracer(0)
window.setup(0.5, 0.75)
window.bgcolor(0.2, 0.2, 0.2)
window.title("Turtle Invaders")

CANNON_STEP = 3
LASER_SPEED = 10
LASER_LENGTH = 20
ALIEN_SPAWN_INTERVAL = 1.2 
ALIEN_SPEED = 2
LEFT = -window.window_width() / 2
RIGHT = window.window_width() / 2
TOP = window.window_height() / 2
BOTTOM = -window.window_height() / 2
FLOOR_LEVEL = 0.9 * BOTTOM
GUTTER = 0.025 * window.window_width()

cannon = turtle.Turtle()
cannon.penup()
cannon.color("purple")
cannon.shape("square")
cannon.setposition(0, FLOOR_LEVEL)
cannon.cannon_movement = 0 #-1 is left, 0 is stationary, 1 is right

text = turtle.Turtle()
text.penup()
text.hideturtle()
text.setposition(LEFT * 0.8, TOP * 0.8)
text.color(1, 1, 1)

lasers = []
aliens = []

def draw_cannon():
    cannon.clear()
    cannon.turtlesize(1, 4)  # Base
    cannon.stamp()
    cannon.sety(FLOOR_LEVEL + 10)
    cannon.turtlesize(1, 1.5)  # Next tier
    cannon.stamp()
    cannon.sety(FLOOR_LEVEL + 20)
    cannon.turtlesize(0.8, 0.3)  # Tip of cannon
    cannon.stamp()
    cannon.sety(FLOOR_LEVEL)

def move_left():
    cannon.cannon_movement = -1

def move_right():
    cannon.cannon_movement = 1

def stop_cannon_movment():
    cannon.cannon_movement = 0

def create_laser():
    laser = turtle.Turtle()
    laser.penup()
    laser.color(1,0,1)
    laser.hideturtle()
    laser.setposition(cannon.xcor(), cannon.ycor())
    laser.setheading(90)
    laser.forward(20)
    laser.pendown()
    laser.pensize(5)
    lasers.append(laser)

def move_laser(laser):
    laser.clear()
    laser.forward(LASER_SPEED)
    laser.forward(LASER_LENGTH)
    laser.forward(-LASER_LENGTH)

def create_alien():
    alien = turtle.Turtle()
    alien.penup()
    alien.turtlesize(1.5)
    alien.setposition(
        random.randint(int(LEFT + GUTTER), int(RIGHT - GUTTER)),
        TOP
    )
    alien.shape("turtle")
    alien.setheading(-90)
    alien.color(random.random(), random.random(), random.random())
    aliens.append(alien)

def remove_sprite(sprite, sprite_list):
    sprite.clear()
    sprite.hideturtle()
    window.update()
    sprite_list.remove(sprite)
    turtle.turtles().remove(sprite)

def update_difficulty(score):
    global ALIEN_SPEED, ALIEN_SPAWN_INTERVAL
    if score > 10:
        ALIEN_SPEED = 5
        ALIEN_SPAWN_INTERVAL = 1.0
    if score > 20: 
        ALIEN_SPEED = 6.5
        ALIEN_SPAWN_INTERVAL = 0.8

window.onkeypress(move_left, "Left")
window.onkeypress(move_right, "Right")
window.onkeyrelease(stop_cannon_movment, "Left")
window.onkeyrelease(stop_cannon_movment, "Right")
window.onkeypress(create_laser, "space")
window.onkeypress(turtle.bye, "q")
window.listen()

draw_cannon()

#Game loop
alien_timer = 0
game_timer = time.time()
score = 0
game_running = True
while game_running:
    timer_this_frame = time.time()
    update_difficulty(score)
    time_elapsed = time.time() - game_timer
    text.clear()
    text.write(
        f"Time: {time_elapsed:5.1f}s\nScore: {score:5}",
        font=("Courier", 20, "bold")
    )
    new_x = cannon.xcor() + CANNON_STEP * cannon.cannon_movement
    if LEFT + GUTTER <= new_x <= RIGHT - GUTTER:
        cannon.setx(new_x)
        draw_cannon()

    for laser in lasers:
        move_laser(laser)
        if laser.ycor() > TOP:
            remove_sprite(laser, lasers)
            break
        for alien in aliens.copy():
            if laser.distance(alien) < 20:
                remove_sprite(alien, aliens)
                remove_sprite(laser, lasers)
                score += 1
                break
    if time.time() - alien_timer > ALIEN_SPAWN_INTERVAL:
        create_alien()
        alien_timer = time.time()
    for alien in aliens:
        alien.forward(ALIEN_SPEED)
        #Check for game over
        if alien.ycor() < FLOOR_LEVEL:
            game_running = False
            break
    
    time_for_this_frame = time.time() - timer_this_frame
    if time_for_this_frame < TIME_FOR_1_FRAME:
        time.sleep(TIME_FOR_1_FRAME - time_for_this_frame)
    window.update()

splash_text = turtle.Turtle()
splash_text.hideturtle()
splash_text.color(1, 1, 1)
splash_text.write("GAME OVER", font=("Courier", 40, "bold"), align="center")

#All code goes above this
turtle.done()