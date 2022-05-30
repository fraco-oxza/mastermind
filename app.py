# Python Version 3.10.9
# [GCC 11.2.0] on linux
#
# Copyright (c) 2022 Francisco Carvajal Ossa
#
# Name: MasterMind
# Version: 1.0.3
# Author: Francisco Carvajal Ossa <fcarvajal22@alumnos.utalca.cl>
# License: All Rights Reserved
from typing import Tuple

import turtle
import random
import math

KEY_LENGTH = 5  # The length for the user and secret key
MAX_ATTEMPTS = 10  # Maximum attempts to discover the secret key


# =============================================================================
# =                                                                           =
# =                       Section: Color Operations                           =
# =                                                                           =
# =============================================================================

# String to store all colors availables in the game
# The syntax must be the next
#
# -[Color Key]|[Color name]:[Color Code(Hex)];
#
# One per line
COLORS = """
-n|naranjo:#F6421B;
-c|celeste:#26B2EB;
-v|verde:#24D417;
-a|amarillo:#F6C202;
-p|purpura:#8217D4;
-b|blanco:#FEFDFA;
-r|rosado:#FF21D1;
"""


def get_all_colors() -> str:
    """
    Function to get all colors keys from the COLORS const
    in one str
    """
    i = 0
    colors = ""

    while i < len(COLORS):
        if COLORS[i] == "-":  # Find the dash for find the Color Key
            colors += COLORS[i + 1]  # Append the Color Key to the Colors
        i += 1

    return colors


def get_hex_color(color_code: str) -> str:
    """
    Function to get a Color Code from the
    COLORS const based on a Color Key.
    If not exists, return a empty string
    """
    i = 0
    last_is_dash = False
    color = ""

    while i < len(COLORS):
        if COLORS[i] == "-":  # Find the dash
            last_is_dash = True
        else:
            if last_is_dash and COLORS[i] == color_code:
                while COLORS[i] != "#":
                    # Forward in the COLORS until the Number sign
                    i += 1
                while COLORS[i] != ";":
                    # Save the Color Code that ends in the Semicolon sign
                    color += COLORS[i]
                    i += 1
                return color
            last_is_dash = False
        i += 1
    return color  # Return the empty string, if not exists one color with that Code


def get_name_color(color_code: str) -> str:
    """
    Function to get a Name Color from the
    COLORS const based on a Color Key.
    If not exists, return a empty string
    """
    i = 0
    last_is_dash = False
    color = ""

    while i < len(COLORS):
        if COLORS[i] == "-":
            last_is_dash = True  # find the dash
        else:
            if last_is_dash and COLORS[i] == color_code:
                while COLORS[i - 1] != "|":
                    i += 1
                while COLORS[i] != ":":
                    color += COLORS[i]  # Save the Color name letter by letter
                    i += 1
                return color
            last_is_dash = False
        i += 1
    return color


def remove_color_index(colors: str, index: int) -> str:
    """
    Function to remove from colors one letter specified by the index,
    this function will to create a new string without of the letter in
    index position
    """
    clean_colors = ""
    i = 0
    while i < len(colors):
        if i != index:
            clean_colors += colors[i]
        i += 1
    return clean_colors


def clear_color(possible_colors: str, color_to_remove: str) -> str:
    """
    Function to remove from "possible_colors all chars that be equal to the
    string "color_to_remove"
    """
    i = 0
    clean_colors = ""
    while i < len(possible_colors):
        if possible_colors[i] != color_to_remove:
            clean_colors += possible_colors[i]
        i += 1
    return clean_colors


# =============================================================================
# =                                                                           =
# =                       Section: Logic of game                              =
# =                                                                           =
# =============================================================================


def generate_random_color(possible_colors: str) -> str:
    """Function to get a random color from possible_colors"""
    index = random.randint(0, len(possible_colors) - 1)
    rand_color = possible_colors[index]

    return rand_color


def create_secret_key(possible_colors: str, key_length: int) -> str:
    """
    Function to obtain a string of colors, based on a string of possible colors
    and a requested length. It should be noted that colors cannot be repeated,
    therefore, the key_length parameter must not be greater than the length of
    the possible_colors parameter.
    """
    secret_key = ""
    i = 0
    while i < key_length:
        color = generate_random_color(possible_colors)
        # Colors are eliminated as they have been used, to avoid repetition
        possible_colors = clear_color(possible_colors, color)

        secret_key += color
        i += 1

    return secret_key


def count_color_hits(secret_key: str, user_key: str) -> int:
    """
    Function to compare the user key with the secret key.
    It will return how many colors the user has matched regardless
    of whether they are in the correct position or not.
    """
    col_hits = 0
    i = 0
    while i < len(secret_key):
        j = 0
        while j < len(user_key):
            if secret_key[i] == user_key[j]:
                col_hits += 1
                # colors that have already been counted are removed,
                # to avoid counting them too many times
                secret_key = remove_color_index(secret_key, i)
                user_key = remove_color_index(user_key, j)
                # the iterators are readjusted, since
                # now the chain will be one unit shorter
                i -= 1
                j -= 1
            j += 1
        i += 1
    return col_hits


def count_hits(secret_key: str, user_key: str) -> Tuple[int, int]:
    """ 
    Function to count the number of colors that the user has hit, 
    giving priority to the colors that are in the correct position, 
    compared to the colors that are, but not in the correct position.
 
    The first value returned from left to right, are the positional 
    hits, the second is the color hits

    pos_hits, col_hits = count_hits("nar", "ran")
    # pos_hits: 1 
    # col_hits: 2
    """
    if secret_key == user_key:
        return len(secret_key), 0

    pos_hits = 0

    # clean strings, without the positional hits, 
    # to be able to count the color hits.
    secret_key_no_pos_hits = ""
    user_key_no_pos_hits = ""

    i = 0
    while i < len(secret_key):
        if secret_key[i] == user_key[i]:
            pos_hits += 1
        else:
            secret_key_no_pos_hits += secret_key[i]
            user_key_no_pos_hits += user_key[i]
        i += 1

    col_hits = count_color_hits(secret_key_no_pos_hits, user_key_no_pos_hits)

    return pos_hits, col_hits

# =============================================================================
# =                                                                           =
# =                     Section: Graphics of game                             =
# =                                                                           =
# =============================================================================


def init_screen() -> turtle._Screen:
    """ 
    function to create the window where the game will be drawn. 
    The size of the window will depend on the number of maximum attempts 
    and the length of the key.
    """ 
    screen = turtle.Screen()

    screen.setup(KEY_LENGTH * 50 + 220, 200 + MAX_ATTEMPTS * 60)
    screen.screensize(KEY_LENGTH * 50 + 220, 200 + MAX_ATTEMPTS * 60)
    screen.bgcolor("#232323")

    return screen


def draw_key(key: str, t: turtle.Turtle):
    """ 
    Function to draw the combination of circles that are indicated in the 
    key string, respecting the indicated colors.
    """ 
    i = 0
    while i < len(key):
        hex_color = get_hex_color(key[i])
        t.color(hex_color)
        t.pendown()
        t.begin_fill()
        t.circle(20)
        t.end_fill()
        t.penup()
        t.forward(50)
        i += 1


def draw_secret_key(secret_key: str, t: turtle.Turtle):
    """
    Function used to print the secret key, indicating to the 
    user what it was and highlighting it by enclosing it in a 
    rectangle to add contrast.
    """

    # Write the text 
    initial_x, initial_y = t.position()
    t.up()
    t.goto(initial_x - 10, initial_y + 10)
    t.color("#f0f0f0")
    t.write("Combinación Correcta: ")
    
    # Draw the rectangle
    t.goto(initial_x, initial_y)
    t.right(180)
    t.forward(25)
    t.right(180)
    t.color("#111111")
    t.begin_fill()
    t.pendown()
    t.forward(KEY_LENGTH * 50)
    t.right(90)
    t.forward(60)
    t.right(90)
    t.forward(KEY_LENGTH * 50)
    t.right(90)
    t.forward(60)
    t.penup()
    t.end_fill()

    # Draw circles using the draw_key function
    t.up()
    t.setpos(initial_x, initial_y - 50)
    t.setheading(0)
    draw_key(secret_key, t)


def draw_hits(position: int, color: int, t: turtle.Turtle):
    """
    Function to indicate to the user through the screen 
    how many hits his combination has. It will first draw 
    n gray circles indicating n positional hits, and then 
    draw m cream circles to indicate m color hits.
    """
    # Positional Hits 
    i = 0
    while i < position:
        t.color("#928374")
        t.pendown()
        t.begin_fill()
        t.circle(5)
        t.end_fill()
        t.penup()
        t.forward(15)
        i += 1
    # Color Hits
    i = 0
    while i < color:
        t.color("#fbf1c7")
        t.pendown()
        t.begin_fill()
        t.circle(5)
        t.end_fill()
        t.penup()
        t.forward(15)
        i += 1


# =============================================================================
# =                                                                           =
# =                     Section: Input Process                                =
# =                                                                           =
# =============================================================================

def contain_only_allow_colors(key: str) -> bool:
    """
    function to check that all the characters of the string key 
    are valid as Color Code in the constant COLORS
    """
    # Get all colors in the COLORS const
    colors = get_all_colors()
    i = 0
    while i < len(key):
        is_on_colors = False
        j = 0
        while j < len(colors) and not is_on_colors:
            if key[i] == colors[j]:
                is_on_colors = True
            j += 1
        if not is_on_colors:
            # Immediately when a color is not this returns False 
            return False
        i += 1
    return True


def get_user_key() -> str:
    """ 
    Function to ask the user for his key prediction. Check that the 
    key entered is valid, if it is not, it will continue asking until the 
    user enters a valid key. In addition, the user can enter the question symbol
    for a small guide and the list of colors. 
    """
    is_valid_key = False
    user_key = ""
    while not is_valid_key:
        raw_user_key = trim(
            input("Ingrese ? para dudas y colores\nIngrese su opción: ")
        )

        if raw_user_key == "?":
            print_colors()
        elif raw_user_key == "":
            print("ERROR: Ingrese una cadena")
        elif len(raw_user_key) != KEY_LENGTH:
            print("ERROR: La cadena DEBE tener " +
                  str(KEY_LENGTH) + " colores")
        elif not contain_only_allow_colors(raw_user_key):
            print("ERROR: Debe ingresar la letra de un color valido")
        else:
            is_valid_key = True
            user_key = raw_user_key

    return user_key


def trim(s: str) -> str:
    """Function to remove all spaces at the beginning and end of a string"""

    result = ""

    start = 0
    while start < len(s) and s[start] == " ":
        start += 1

    end = len(s) - 1
    while end >= 0 and s[end] == " ":
        end -= 1

    for i in range(start, end + 1):
        result += s[i]

    return result


def user_wants_to_continue(msg: str) -> bool:
    """
    Function to ask the user if he wants to continue playing. 
    It will prompt the user until they indicate a valid option.
    """

    has_answer = False
    while not has_answer:
        raw_answer = input(msg + ", ¿Desea seguir jugando?(s/n): ")
        raw_answer = trim(raw_answer)
        if raw_answer == "s":
            return True
        if raw_answer == "n":
            return False
        print("ERROR: Ingrese una opción, s ó n")
    return False


def print_colors():
    """ 
    Function that prints a list of the colors contained in the constant COLORS. 
    In addition to giving a brief explanation of how to enter the key. 
    """ 
    print("Lista de colores: ")
    i = 0
    colors = get_all_colors()
    while i < len(colors):
        print(colors[i] + " - " + get_name_color(colors[i]))
        i += 1
    print("Ingrese la inicial de los colores en forma de cadena\nEjemplo: ")
    print("    Para la secuencia Rosado(r)-Amarillo(a)-Naranjo(n)")
    print("    La cadena a introducir seria: ran")


def game_loop(t: turtle.Turtle, screen: turtle._Screen):
    """ 
    This function is responsible for executing the logic of the game. Among his
    responsibilities is to generate a key for each game, acquire user data, 
    calculate where to draw each thing, keep a count of points, print the 
    statistics and check if the user wants to continue playing.
    """ 
    # TODO: Print the instructions

    games = 0
    points = 0
    tries = 0
    user_want_to_exit = False
    while not user_want_to_exit:
        score = 1000
        games += 1
        t.clear()

        width, _ = screen.screensize()
        init_x = (width - KEY_LENGTH * 50 + 30) / 2 - width / 2
        y = (200 + MAX_ATTEMPTS * 60) / 2 - 100

        secret_key = create_secret_key(get_all_colors(), KEY_LENGTH)

        win = False
        attemp = 1
        while not win:
            t.up()
            t.goto(init_x, y)

            tries += 1

            user_key = get_user_key()
            draw_key(user_key, t)
            pos_hits, col_hits = count_hits(secret_key, user_key)
            draw_hits(pos_hits, col_hits, t)
            if pos_hits == KEY_LENGTH:
                t.up()
                t.goto(init_x, y - 50)
                win = True
                draw_secret_key(secret_key, t)
                points += score
                user_want_to_exit = not user_wants_to_continue(
                    "Ha ganado esta ronda")
            elif attemp >= MAX_ATTEMPTS:
                t.up()
                t.goto(init_x, y - 50)
                win = True
                draw_secret_key(secret_key, t)
                user_want_to_exit = not user_wants_to_continue(
                    "Ha perdido esta ronda")
            else:
                score /= 2

            y -= 50
            attemp += 1
        print("Ya lleva ", math.floor(points), "puntos")
    end_text = """\n====================================================

                    Juego Terminado
                    ---------------

        Puntos:                     {}\n
        Partidas jugadas:           {}
        Promedio de intentos:       {}\n
        Largo de clave:             {}
        Cantidad de Colores:        {}

===================================================="""
    print(
        end_text.format(
            math.floor(points),
            games,
            round(tries / games),
            KEY_LENGTH,
            len(get_all_colors()),
        )
    )


def main():
    """ 
    Main function, from here the functions are called to start the game.
    """ 
    print_colors()
    screen = init_screen()
    turtle_instance = turtle.Turtle()
    turtle_instance.speed(0)
    game_loop(turtle_instance, screen)


if __name__ == "__main__":
    main()
    input("Presione enter para salir")
