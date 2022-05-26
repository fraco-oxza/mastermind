"""
Created on Wednesday May 11, 2022 at 02:09 PM

@Author: fraco
"""
import turtle
import random
import math

KEY_LENGTH = 5
MAX_ATTEMPTS = 8
COLORS = """
-n|naranjo:#F6421B;
-c|celeste:#26B2EB;
-v|verde:#24D417;
-a|amarillo:#F6C202;
-p|purpura:#8217D4;
-b|blanco:#FEFDFA;
-r|rosado:#FF21D1;
"""

# =============================================================================
# =                                                                           =
# =                       Section: Logic of game                              =
# =                                                                           =
# =============================================================================


def get_all_colors() -> str:
    i = 0
    colors = ""

    while i < len(COLORS):
        if COLORS[i] == "-":
            colors += COLORS[i + 1]
        i += 1

    return colors


def get_hex_color(initial: str) -> str:
    i = 0
    last_is_dash = False
    color = ""

    while i < len(COLORS):
        if COLORS[i] == "-":
            last_is_dash = True
        else:
            if last_is_dash and COLORS[i] == initial:
                while COLORS[i] != "#":
                    i += 1
                while COLORS[i] != ";":
                    color += COLORS[i]
                    i += 1
                return color
            last_is_dash = False
        i += 1
    return color


def get_name_color(initial: str) -> str:
    i = 0
    last_is_dash = False
    color = ""

    while i < len(COLORS):
        if COLORS[i] == "-":
            last_is_dash = True
        else:
            if last_is_dash and COLORS[i] == initial:
                while COLORS[i - 1] != "|":
                    i += 1
                while COLORS[i] != ":":
                    color += COLORS[i]
                    i += 1
                return color
            last_is_dash = False
        i += 1
    return color


def remove_color_index(colors: str, index: int):
    clean_colors = ""
    i = 0
    while i < len(colors):
        if i != index:
            clean_colors += colors[i]
        i += 1
    return clean_colors


def generate_random_color(possible_colors: str) -> str:
    "Function to get a random color from a string of color initials"
    index = random.randint(0, len(possible_colors) - 1)
    rand_color = possible_colors[index]

    return rand_color


def create_secret_key(possible_colors: str, key_length: int) -> str:
    """
    function to obtain a string of colors, based on a string of possible colors
    and a requested length. It should be noted that colors cannot be repeated,
    therefore, the key_length parameter must not be greater than the length of
    the possible_colors parameter.
    """
    secret_key = ""
    for _ in range(key_length):
        color = generate_random_color(possible_colors)

        secret_key += color

    return secret_key


def count_color_hits(secret_key: str, user_key: str):
    col_hits = 0
    i = 0
    while i < len(secret_key):
        j = 0
        while j < len(user_key):
            if secret_key[i] == user_key[j]:
                col_hits += 1
                secret_key = remove_color_index(secret_key, i)
                user_key = remove_color_index(user_key, j)
                i -= 1
                j -= 1
            j += 1
        i += 1
    return col_hits


def count_hits(secret_key: str, user_key: str):
    if secret_key == user_key:
        return len(secret_key), 0

    pos_hits = 0

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


def init_screen():
    screen = turtle.Screen()

    screen.setup(KEY_LENGTH * 50 + 220, 200 + MAX_ATTEMPTS * 60)
    screen.screensize(KEY_LENGTH * 50 + 220, 200 + MAX_ATTEMPTS * 60)
    screen.bgcolor("#232323")

    return screen


def draw_user_selection(user_key: str, t: turtle.Turtle):
    i = 0
    while i < len(user_key):
        hex_color = get_hex_color(user_key[i])
        t.color(hex_color)
        t.pendown()
        t.begin_fill()
        t.circle(20)
        t.end_fill()
        t.penup()
        t.forward(50)
        i += 1


def draw_secret_key(secret_key: str, t: turtle.Turtle):
    initial_x, initial_y = t.position()
    t.up()
    t.goto(initial_x-10, initial_y+10)
    t.color("#f0f0f0")
    t.write("Combinación Correcta: ")
    t.goto(initial_x, initial_y)
    t.right(180)
    t.forward(25)
    t.right(180)
    t.color("#111111")
    t.begin_fill()
    t.pendown()

    t.forward(KEY_LENGTH*50)
    t.right(90)
    t.forward(60)
    t.right(90)
    t.forward(KEY_LENGTH*50)
    t.right(90)
    t.forward(60)
    t.penup()
    t.end_fill()
    t.up()
    t.setpos(initial_x, initial_y-50)
    t.setheading(0)
    draw_user_selection(secret_key, t)


def draw_hits(position: int, color: int, t: turtle.Turtle):
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
            return False
        i += 1
    return True


def get_user_key():
    is_valid_key = False
    user_key = ""
    while not is_valid_key:
        raw_user_key = trim(input(
            "Ingrese ? para dudas y colores\nIngrese su opción: "))

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
    result = ""

    start = 0
    while start < len(s) and s[start] == " ":
        start += 1

    end = len(s) - 1
    while end >= 0 and s[end] == " ":
        end -= 1

    for i in range(start, end+1):
        result += s[i]

    return result


def user_wants_to_continue(msg: str) -> bool:
    has_answer = False
    while not has_answer:
        raw_answer = input(msg+", ¿Desea seguir jugando?(s/n): ")
        raw_answer = trim(raw_answer)
        if raw_answer == "s":
            return True
        if raw_answer == "n":
            has_answer = True
        print("ERROR: Ingrese una opción, s ó n")
    return False


def print_colors():
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
    # TODO: Print the instructions

    points = 0
    user_want_to_exit = False
    while not user_want_to_exit:
        score = 1000
        t.clear()

        width, _ = screen.screensize()
        init_x = (width - KEY_LENGTH * 50 + 30) / 2 - width / 2
        y = (200+MAX_ATTEMPTS*60)/2 - 100
        secret_key = create_secret_key(get_all_colors(), KEY_LENGTH)
        win = False
        attemp = 1
        while not win:
            t.up()
            t.goto(init_x, y)

            user_key = get_user_key()
            draw_user_selection(user_key, t)
            pos_hits, col_hits = count_hits(secret_key, user_key)
            draw_hits(pos_hits, col_hits, t)
            if pos_hits == KEY_LENGTH:
                t.up()
                t.goto(init_x, y-50)
                win = True
                draw_secret_key(secret_key, t)
                points += score
                user_want_to_exit = not user_wants_to_continue(
                    "Ha ganado esta ronda")
            elif attemp >= MAX_ATTEMPTS:
                t.up()
                t.goto(init_x, y-50)
                win = True
                draw_secret_key(secret_key, t)
                user_want_to_exit = not user_wants_to_continue(
                    "Ha perdido esta ronda")
            else:
                score /= 2

            y -= 50
            attemp += 1
        print("Ya lleva ", math.floor(points), "puntos")
    print("Ha Obtenido ", math.floor(points), "puntos")


def main():
    print_colors()
    screen = init_screen()
    turtle_instance = turtle.Turtle()
    turtle_instance.speed(0)
    game_loop(turtle_instance, screen)


if __name__ == "__main__":
    main()
    input("Presione enter para salir")
