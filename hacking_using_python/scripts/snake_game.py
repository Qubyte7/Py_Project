from turtle import *
from random import randrange
from freegames import square, vector
import subprocess
import time

# Initialize variables
food = vector(0, 0)
snake = [vector(10, 0)]
aim = vector(0, -10)
score = 0
game_over = False

# Create turtles for display
score_turtle = Turtle()
game_over_turtle = Turtle()
restart_turtle = Turtle()

# Setup display turtles
for turtle in [score_turtle, game_over_turtle, restart_turtle]:
    turtle.hideturtle()
    turtle.penup()

score_turtle.goto(0, 190)
score_turtle.write("Score: 0", align="center", font=("Arial", 14, "normal"))

def change(x, y):
    """Change snake direction if game is active."""
    if not game_over:
        aim.x = x
        aim.y = y

def inside(head):
    """Return True if head is within boundaries."""
    return -200 < head.x < 190 and -200 < head.y < 190

def restart():
    """Reset game state."""
    global game_over, snake, food, aim, score
    game_over = False
    snake = [vector(10, 0)]
    aim = vector(0, -10)
    food.x = randrange(-15, 15) * 10
    food.y = randrange(-15, 15) * 10
    score = 0
    
    # Clear displays
    score_turtle.clear()
    game_over_turtle.clear()
    restart_turtle.clear()
    clear()
    
    # Reset score display
    score_turtle.write(f"Score: {score}", align="center", font=("Arial", 14, "normal"))
    move()

def move():
    """Move snake forward one segment."""
    global game_over, score
    if game_over:
        return
    
    head = snake[-1].copy()
    head.move(aim)
    
    # Check for collision
    if not inside(head) or head in snake:
        game_over = True
        square(head.x, head.y, 9, 'red')
        update()
        game_over_turtle.write("Game Over!", align="center", font=("Arial", 24, "bold"))
        restart_turtle.goto(0, -30)
        restart_turtle.write("Press SPACE to Restart", align="center", font=("Arial", 14, "normal"))
        return
    
    snake.append(head)
    
    # Check food collision
    if head == food:
        score += 1
        score_turtle.clear()
        score_turtle.write(f"Score: {score}", align="center", font=("Arial", 14, "normal"))
        food.x = randrange(-15, 15) * 10
        food.y = randrange(-15, 15) * 10
    else:
        snake.pop(0)
    
    clear()
    
    # Draw snake with gradient colors
    for i, body in enumerate(snake):
        color = '#2E8B57' if i % 2 == 0 else '#3CB371'  # SeaGreen and MediumSeaGreen
        if body == snake[-1]:
            color = '#228B22'  # ForestGreen for head
        square(body.x, body.y, 9, color)
    
    # Draw food
    square(food.x, food.y, 9, '#FF4500')  # OrangeRed color
    update()
    ontimer(move, 100)

# Game setup
setup(420, 420, 370, 0)
hideturtle()
tracer(False)
listen()
onkey(lambda: change(10, 0), 'Right')
onkey(lambda: change(-10, 0), 'Left')
onkey(lambda: change(0, 10), 'Up')
onkey(lambda: change(0, -10), 'Down')
onkey(restart, 'space')



# Initial food position
food.x = randrange(-15, 15) * 10
food.y = randrange(-15, 15) * 10

move()
done()
