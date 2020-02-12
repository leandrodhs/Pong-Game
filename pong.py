import time
import random
import turtle

# Window creation and setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
# Create a window to show the game
window = turtle.Screen()
window.title("Pong Game")
# Set the backgroud color
window.bgcolor("black")
window.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
window.tracer(0)

# Game setup
PLAYER_SIZE = 5
PLAYER_START_X = 350
PLAYER_START_Y = 0
PLAYER_SPEED = 10
UP = 1
DOWN = -1
BALL_SPEED = 1
PLAYER_WIDTH = 20
PLAYER_HEIGHT = PLAYER_WIDTH * PLAYER_SIZE
BALL_DIAMETER = 20
DISTANCE_TO_COLLISION = (PLAYER_WIDTH + BALL_DIAMETER) / 2

gameIsRunning = False
score_a = 0
score_b = 0
score_text = "Player A: {}, Player B: {}"

# Player A
player_a = turtle.Turtle()
# Turn off animation and go as fast as possible
player_a.speed(0)
player_a.shape("square")
player_a.shapesize(stretch_wid=PLAYER_SIZE, stretch_len=1)
player_a.color("white")
player_a.penup()
player_a.goto(-PLAYER_START_X, PLAYER_START_Y)

# Player B
player_b = turtle.Turtle()
# Turn off animation and go as fast as possible
player_b.speed(0)
player_b.shape("square")
player_b.shapesize(stretch_wid=PLAYER_SIZE, stretch_len=1)
player_b.color("white")
player_b.penup()
player_b.goto(PLAYER_START_X, PLAYER_START_Y)

# Player A starts
startingPlayer = player_a

# Ball
ball = turtle.Turtle()
# Turn off animation and go as fast as possible
ball.speed(0)
ball.shape("circle")
ball.color("white")
ball.penup()
# Start with player_a
ball.goto(startingPlayer.xcor() + DISTANCE_TO_COLLISION, PLAYER_START_Y)
# Movement speed
ball.dy = BALL_SPEED * random.choice([-1, 1])
ball.dx = BALL_SPEED

pen = turtle.Turtle()
pen.speed(0)
pen.hideturtle()
pen.color("white")
pen.penup()
pen.goto(0, round(SCREEN_HEIGHT * 0.8 / 2))
pen.write(score_text.format(score_a, score_b), align="center", font=("courier", 14, "normal"))

# Movements
def playerAUp():
	playerMove(player_a, direction=UP)

def playerADown():
	playerMove(player_a, direction=DOWN)

def playerBUp():
	playerMove(player_b, direction=UP)

def playerBDown():
	playerMove(player_b, direction=DOWN)

def playerMove(player, direction=UP):
	if (-SCREEN_HEIGHT < 2 * player.ycor() - PLAYER_HEIGHT and direction == DOWN) or (2 * player.ycor() + PLAYER_HEIGHT < SCREEN_HEIGHT and direction == UP):
		y = player.ycor()
		y += PLAYER_SPEED * direction
		player.sety(y)

def startGame():
	global gameIsRunning
	gameIsRunning = True

window.listen()
window.onkeypress(playerAUp, "w")
window.onkeypress(playerADown, "s")
window.onkeypress(playerBUp, "Up")
window.onkeypress(playerBDown, "Down")
window.onkeypress(startGame, "space")

def checkCollision(ball, player1):
	return abs(player1.xcor()) - abs(ball.xcor()) == DISTANCE_TO_COLLISION and player1.ycor() - PLAYER_HEIGHT / 2 <= ball.ycor() <= player1.ycor() + PLAYER_HEIGHT / 2

def sign(x):
	if x >= 0:
		return 1
	else:
		return -1

# Main loop
while True:
	if gameIsRunning:
		ball.setx(ball.xcor() + ball.dx)
		ball.sety(ball.ycor() + ball.dy)

		# Border check Y
		if abs(ball.ycor()) >= (SCREEN_HEIGHT - BALL_DIAMETER) / 2:
			ball.dy *= -1

		if abs(ball.xcor()) - DISTANCE_TO_COLLISION >= SCREEN_WIDTH / 2:
			# Ball went outside the screen
			if ball.xcor() < 0:
				# Player B won!
				startingPlayer = player_a
				score_b += 1
			else:
				# Player A won
				startingPlayer = player_b
				score_a += 1
			ball.goto(startingPlayer.xcor() - DISTANCE_TO_COLLISION * sign(ball.xcor()), startingPlayer.ycor())
			pen.clear()
			pen.write(score_text.format(score_a, score_b), align="center", font=("courier", 14, "normal"))
			gameIsRunning = False
			ball.dx *= -1
			ball.dy *= random.choice([-1, 1])

		elif checkCollision(ball, player_a) or checkCollision(ball, player_b):
			ball.dx *= -1
	else:
		ball.sety(startingPlayer.ycor())
	window.update()
	time.sleep(0.004)
