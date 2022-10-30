"""
File:   project_1.py
Author: Jeff Alkire
Date:   10-28-2022
Description:
    Project 1 from chapter 7 of Python text.
    Draw a circle given a Turtle object, circle center, and radius.
"""
from turtle import Turtle
from math import pi

def distance_to_move(radius: float):
    return radius * 2 * pi / 120

def draw_axes(tur: Turtle):
    tur.pencolor("grey")
    tur.up()
    tur.goto(-200,0)
    tur.setheading(0)
    tur.down()
    tur.forward(400)
    tur.up()
    tur.goto(0,-200)
    tur.setheading(90)
    tur.down()
    tur.forward(400)

def goto_start_loc(tur: Turtle, center: (float,float), radius: float):
    tur.up()
    (x,y) = center
    tur.goto(x+radius,y)
    tur.setheading(90)
    tur.down()

def drawCircle(tur: Turtle, center: (float,float), radius: float):
    goto_start_loc(tur, center, radius)
    tur.pencolor("red")
    for i in range(120):
        tur.forward(distance_to_move(radius))
        tur.left(3)

def main():
    t = Turtle()
    t.hideturtle()
    draw_axes(t)
    drawCircle(t,(50,-50), 50)

    input("Enter to exit program.")

if __name__ == "__main__":
    main()