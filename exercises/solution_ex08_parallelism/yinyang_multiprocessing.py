#!/usr/bin/env python3
"""
Attempt to use multiprocessing in the asteroids game

WARNING: this program doesn't work!
It tries to replace thread.Thread with multiprocessing.Process,
but each process launches a new Python interpreter, and the interpreters
don't share a common graphics canvas.

Based on code from "Python Programming Fundamentals" by Kent Lee
"""

import turtle
from multiprocessing import Process, Pool


def draw_fish(heading, radius, color):
    pen = turtle.Turtle()
    pen.speed(10)
    pen.setheading(heading)
    pen.width(3)
    pen.color("black", color)  # pen color, fill color
    pen.begin_fill()
    pen.circle(radius/2., 180)
    pen.circle(radius, 180)
    pen.left(180)
    pen.circle(-radius/2., 180)
    pen.end_fill()


def draw_dot(heading, fish_radius, color):
    pen = turtle.Turtle()
    pen.speed(10)
    pen.setheading(heading)
    pen.left(90)
    pen.up()
    pen.forward(fish_radius*0.35)
    pen.right(90)
    pen.down()
    pen.color("black", color)
    pen.begin_fill()
    pen.circle(fish_radius*0.15)
    pen.end_fill()


def draw_yin(radius):
    draw_fish(0, radius, "black")


def draw_yin_dot(fish_radius):
    draw_dot(0, fish_radius, "white")


def draw_yang(radius):
    draw_fish(180, radius, "white")


def draw_yang_dot(fish_radius):
    draw_dot(180, fish_radius, "black")


def main():
    init_screen()

    fish_radius = 200

    processes = [
        Process(target=draw_yin, args=(fish_radius,)),
        Process(target=draw_yin_dot, args=(fish_radius,)),
        Process(target=draw_yang, args=(fish_radius,)),
        Process(target=draw_yang_dot, args=(fish_radius,)),
    ]

    for process in processes:
        process.start()

    # Won't work because each Process runs in its own Python interpreter.
    # TODO: could we share the Turtle Screen or Tk Canvas using
    # multiprocessing.Value or multiprocessing.Queue?


def init_screen():
    # Delete the turtle's drawings from the screen, re-center the turtle and
    # set variables to the default values
    screen = turtle.Screen()
    screen.setup(width=500, height=500)
    screen.title('Yin Yang')
    turtle.reset()
    turtle.bgcolor('#E8E8F6')
    turtle.hideturtle()


if __name__ == '__main__':
    print("\n====== Warning: this program doesn't work! ========")
    print("You can have multiple *threads* drawing on the same canvas, "
          "but not multiple *processes*")
    main()
    turtle.mainloop()
