#!/usr/bin/env python3
"""       turtle-example-suite:

            tdemo_yinyang.py

Another drawing suitable as a beginner's
programming example.

The small circles are drawn by the circle
command.

Code from "Python Programming Fundamentals" by Kent Lee
"""

import turtle


def draw_fish(pen, radius, color1, color2):
    pen.color("black", color1)  # pen color, fill color
    pen.begin_fill()
    pen.circle(radius/2., 180)
    pen.circle(radius, 180)
    pen.left(180)
    pen.circle(-radius/2., 180)
    pen.end_fill()
    pen.left(90)
    pen.up()
    pen.forward(radius*0.35)
    pen.right(90)
    pen.down()
    pen.color(color1, color2)
    pen.begin_fill()
    pen.circle(radius*0.15)
    pen.end_fill()


def draw_yin(pen):
    pen.setx(0)
    pen.sety(0)
    draw_fish(pen, 200, "black", "white")


def draw_yang(pen):
    pen.setx(0)
    pen.sety(0)
    pen.setheading(180)
    draw_fish(pen, 200, "white", "black")


def main():
    screen = turtle.Screen()
    screen.title('Yin Yang')
    screen.setup(width=500, height=500)

    # Delete the pen's drawings from the screen, re-center the pen and
    # set variables to the default values
    pen = turtle.Turtle()
    turtle.bgcolor('#E8E8F6')
    pen.reset()
    pen.width(3)

    draw_yin(pen)
    draw_yang(pen)

    pen.hideturtle()

if __name__ == '__main__':
    main()
    turtle.mainloop()
