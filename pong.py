from turtle import Turtle, TurtleScreen, _Screen


class Window(_Screen):
    def __init__(self, title: str, color: str, w: float, h: float) -> None:
        super().__init__()
        TurtleScreen.__init__(self, Window._canvas)
        if Turtle._screen is None:
            Turtle._screen = self
        self.title(title)
        self.bgcolor(color)
        self.setup(width=w, height=h)
        self.tracer(0)


class Ball(Turtle):
    def __init__(self, dx, dy) -> None:
        super().__init__()
        self.speed(0)
        self.shape('square')
        self.color('white')
        self.penup()
        self.goto(0, 0)
        self.dx = dx
        self.dy = dy


class Paddle(Turtle):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.speed(0)
        self.shape('square')
        self.color('white')
        self.shapesize(stretch_wid=5, stretch_len=1)
        self.penup()
        self.goto(x, y)

    def move_up(self) -> None:
        self.sety(self.ycor() + 20)

    def move_down(self) -> None:
        self.sety(self.ycor() - 20)

    def change_color(self, color: str) -> None:
        self.color(color)


class Player:
    def __init__(self, name, x, y) -> None:
        self.name = name
        self.paddle = Paddle(x, y)
        self.score = 0

    def reset_score(self):
        self.score = 0

    def goal(self):
        self.score += 1


class Pen(Turtle):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.speed(0)
        self.color('White')
        self.penup()
        self.hideturtle()
        self.goto(x, y)


class Game:
    def __init__(self, x, y) -> None:
        self.window = Window('Pong by @AlLaktah', 'black', x, y)
        self.player_l = Player('Player A', -(x/2 - 50), 0)
        self.player_r = Player('Player B', x/2 - 50, 0)
        self.ball = Ball(0.1, 0.1)
        self.pen = Pen(0, y/2 - 40)
        self.pen.write('{}: {} {}: {}'.format(self.player_l.name, self.player_l.score,
                       self.player_r.name, self.player_r.score), align='center', font=('Courier', 24, 'normal'))

    def init_hotkeys(self) -> None:
        self.window.onkeypress(self.player_l.paddle.move_up, 'w')
        self.window.onkeypress(self.player_l.paddle.move_down, 's')
        self.window.onkeypress(self.player_r.paddle.move_up, 'Up')
        self.window.onkeypress(self.player_r.paddle.move_down, 'Down')
        self.window.listen()

    def ball_logic(self) -> None:
        if self.ball.ycor() > 290:
            self.ball.sety(290)
            self.ball.dy *= -1

        if self.ball.ycor() < -290:
            self.ball.sety(-290)
            self.ball.dy *= -1

        if self.ball.xcor() > 390:
            self.ball.goto(0, 0)
            self.player_l.goal()
            self.ball.dx *= -1
            self.pen.clear()
            self.pen.write('{}: {} {}: {}'.format(self.player_l.name, self.player_l.score,
                           self.player_r.name, self.player_r.score), align='center', font=('Courier', 24, 'normal'))

        if self.ball.xcor() < -390:
            self.ball.goto(0, 0)
            self.player_r.goal()
            self.ball.dx *= -1
            self.pen.clear()
            self.pen.write('{}: {} {}: {}'.format(self.player_l.name, self.player_l.score,
                           self.player_r.name, self.player_r.score), align='center', font=('Courier', 24, 'normal'))

        if self.ball.xcor() < -390:
            self.ball.goto(0, 0)
            self.ball.dx *= -1

        if (self.ball.xcor() > 340 and self.ball.xcor() < 350) and (self.ball.ycor() < self.player_r.paddle.ycor() + 40 and self.ball.ycor() > self.player_r.paddle.ycor() - 40):
            self.ball.setx(340)
            self.ball.dx *= -1

        if (self.ball.xcor() < -340 and self.ball.xcor() > -350) and (self.ball.ycor() < self.player_l.paddle.ycor() + 40 and self.ball.ycor() > self.player_l.paddle.ycor() - 40):
            self.ball.setx(-340)
            self.ball.dx *= -1

    def start(self) -> None:
        self.init_hotkeys()
        while True:
            self.window.update()
            self.ball.setposition(
                self.ball.xcor() + self.ball.dx, self.ball.ycor() + self.ball.dy)
            self.ball_logic()
