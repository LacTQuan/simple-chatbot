import turtle
import random

wn = turtle.Screen()
wn.title("Pong Game by Lạc Thiệu Quân")
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.tracer(0)

# Score
score_a = 0
score_b = 0

# Paddle A
paddle_a = turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape("square")
paddle_a.color("white")
paddle_a.penup()
paddle_a.goto(-350, 0)
paddle_a.shapesize(stretch_wid=5, stretch_len=1)

# Paddle B
paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.color("white")
paddle_b.penup()
paddle_b.goto(350, 0)
paddle_b.shapesize(stretch_wid=5, stretch_len=1)

# Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("circle")
ball.color("yellow")
ball.penup()
ball.goto(0, 0)
ball.dx = 0.15
ball.dy = 0.15

# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Player A: 0   Player B: 0", align="center", font=("Courier", 24, "normal"))

# Function
def paddle_a_up():
    y = paddle_a.ycor()
    y += 30
    paddle_a.sety(min(y, 250))

def paddle_a_down():
    y = paddle_a.ycor()
    y -= 30
    paddle_a.sety(max(y, -250))

def paddle_b_up():
    y = paddle_b.ycor()
    y += 30
    paddle_b.sety(min(y, 250))

def paddle_b_down():
    y = paddle_b.ycor()
    y -= 30
    paddle_b.sety(max(y, -250))

# Keyboard binding
wn.listen()
wn.onkeypress(paddle_a_up, "w")
wn.onkeypress(paddle_a_down, "s")
wn.onkeypress(paddle_b_up, "Up")
wn.onkeypress(paddle_b_down, "Down")

randMove = [-1, 1]

#Main game loop
while True:
    wn.update()

    # Move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Border checking
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1
    if ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= -1

    if ball.xcor() > 390:
        ball.goto(0, 0)
        score_a += 1
        ball.dx *= random.choice(randMove)
        pen.clear()
        pen.write("Player A: {}   Player B: {}".format(score_a, score_b), align="center", font=("Courier", 24, "normal"))

    if ball.xcor() < -390:
        ball.goto(0, 0)
        score_b += 1
        ball.dx *= random.choice(randMove)
        pen.clear()
        pen.write("Player A: {}   Player B: {}".format(score_a, score_b), align="center", font=("Courier", 24, "normal"))

    # Paddle and ball collisions
    if (ball.xcor() > 340 and ball.xcor() < 350) and (ball.ycor() <= paddle_b.ycor() + 40 and ball.ycor() >= paddle_b.ycor() - 40):
        ball.dx *= -1
        ball.dy *= -1
        ball.setx(340)

    if (ball.xcor() < -340 and ball.xcor() > -350) and (ball.ycor() <= paddle_a.ycor() + 40 and ball.ycor() >= paddle_a.ycor() - 40):
        ball.dx *= -1
        ball.dy *= -1
        ball.setx(-340)
