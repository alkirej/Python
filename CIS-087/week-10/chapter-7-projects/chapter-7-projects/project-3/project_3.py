"""
File:   project_3.py
Author: Jeff Alkire
Date:   10-28-2022
Description:
    Project 3 from chapter 7 of Python text.
    Draw a Koch snowflake
"""
from turtle import Turtle

FRACTAL_LINE_LEN=1000.0
FRACTAL_LEVEL=5

def draw_fractal_line(tur: Turtle, level: int, length: float) -> None:
    if 0 >= level:
        tur.forward(length)
    else:
        new_len = length / 3
        draw_fractal_line(tur,level-1,new_len)
        tur.left(60)
        draw_fractal_line(tur,level-1,new_len)
        tur.right(120)
        draw_fractal_line(tur,level-1,new_len)
        tur.left(60)
        draw_fractal_line(tur,level-1,new_len)


def main():
    tur = Turtle()
    tur.hideturtle()
    tur.speed(0)
    tur.pencolor("blue") # nice winter color
    tur.up()
    # Center fractal for levels > 0
    tur.goto(-FRACTAL_LINE_LEN//2,FRACTAL_LINE_LEN * 7//24)
    tur.down()

    tur.setheading(0)
    for n in range(3):
        draw_fractal_line(tur, FRACTAL_LEVEL, FRACTAL_LINE_LEN)
        tur.right(120)

    input("Enter to finish:")

if __name__ == "__main__":
    main()