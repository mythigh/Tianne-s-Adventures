import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox

# ---------------- Window Setup ----------------
root = tk.Tk()
root.title("Basic 2D Platformer")
root.geometry("600x400")

# ---------------- Canvas ----------------
canvas = tk.Canvas(root, width=600, height=400, bg="skyblue")
canvas.pack(fill="both", expand=True)

# ---------------- Load Images ----------------
standing_img = Image.open("photos/tia_stand.png").resize((40, 40), Image.Resampling.LANCZOS)
standing_image = ImageTk.PhotoImage(standing_img)

walking_img = Image.open("photos/tia_walk.png").resize((40, 40), Image.Resampling.LANCZOS)
walking_image = ImageTk.PhotoImage(walking_img)

jumping_img = Image.open("photos/tia_jump.png").resize((40, 40), Image.Resampling.LANCZOS)
jumping_image = ImageTk.PhotoImage(jumping_img)

# ---------------- Game Variables ----------------
start_x, start_y = 50, 300
character = None
goal_platform = None
yellow_platforms = []
all_platforms = []
x_velocity = 0
y_velocity = 0
gravity = 1
jump_strength = -15
on_ground = False
message_displayed = False
popup_text = None
game_running = False
menu_hint_text = None

# ---------------- Menu ----------------
menu_frame = tk.Frame(root, width=600, height=400, bg="lightblue")
menu_frame.place(x=0, y=0)


def show_instructions():
    messagebox.showinfo(
        "Instructions",
        "Controls:\n"
        "Left Arrow → Move Left\n"
        "Right Arrow → Move Right\n"
        "Space → Jump\n"
        "Q → Return to Menu\n\n"
        "Rules:\n"
        "Jump across yellow platforms to reach the green goal platform.\n"
        "When you land on the green platform, the message 'I love you ❤️' appears.\n"
        "Press SPACE to reset after reaching the goal."
    )


def start_game():
    global game_running
    menu_frame.place_forget()  # hide menu
    init_game()
    game_running = True
    move_character()


def return_to_menu(event=None):
    global character, goal_platform, yellow_platforms, all_platforms, game_running, menu_hint_text
    game_running = False
    canvas.delete("game")  # delete all game objects
    all_platforms.clear()
    yellow_platforms.clear()
    character = None
    goal_platform = None
    if menu_hint_text:
        canvas.delete(menu_hint_text)
    menu_frame.place(x=0, y=0)


# Menu buttons
start_btn = tk.Button(menu_frame, text="Start Game", font=("Arial", 16), width=15, command=start_game)
start_btn.place(relx=0.5, rely=0.4, anchor="center")

instructions_btn = tk.Button(menu_frame, text="Instructions", font=("Arial", 16), width=15, command=show_instructions)
instructions_btn.place(relx=0.5, rely=0.55, anchor="center")


# ---------------- Game Initialization ----------------
def init_game():
    global character, goal_platform, yellow_platforms, all_platforms, menu_hint_text
    # Add top hint text
    menu_hint_text = canvas.create_text(10, 10, anchor="nw", text="Press Q to return to menu", font=("Arial", 12),
                                        fill="white", tags="game")

    # Create character
    character = canvas.create_image(start_x, start_y, image=standing_image, anchor="nw", tags="game")

    # Create platforms
    goal_platform = canvas.create_rectangle(500, 250, 580, 270, fill="green", tags="game")  # goal
    yellow_platforms = [
        canvas.create_rectangle(150, 320, 250, 340, fill="yellow", tags="game"),
        canvas.create_rectangle(300, 280, 400, 300, fill="yellow", tags="game"),
        canvas.create_rectangle(200, 220, 300, 240, fill="yellow", tags="game"),
        canvas.create_rectangle(400, 180, 500, 200, fill="yellow", tags="game"),
    ]
    all_platforms.extend(yellow_platforms + [goal_platform])


# ---------------- Game Functions ----------------
def reset_character():
    global x_velocity, y_velocity, on_ground
    coords = canvas.bbox(character)
    x1, y1, x2, y2 = coords
    canvas.move(character, start_x - x1, start_y - y1)
    x_velocity = 0
    y_velocity = 0
    on_ground = False


def show_message():
    global popup_text, message_displayed
    message_displayed = True
    canvas.create_rectangle(150, 170, 450, 230, fill="black", outline="white", tags=("popup_bg", "game"))
    popup_text = canvas.create_text(
        300, 200,
        text="I love you ❤️\nPress SPACE to continue",
        font=("Arial", 16),
        fill="white",
        anchor="center",
        justify="center",
        tags=("popup", "game")
    )
    canvas.tag_raise("popup_bg")
    canvas.tag_raise("popup")


def hide_message(event=None):
    global message_displayed
    if message_displayed:
        canvas.delete("popup")
        canvas.delete("popup_bg")
        message_displayed = False
        reset_character()


def move_character():
    global y_velocity, on_ground

    if not game_running:
        return  # stop loop if game ended

    if not message_displayed:
        # Apply gravity
        y_velocity += gravity
        canvas.move(character, x_velocity, y_velocity)

        # Get current position
        coords = canvas.bbox(character)
        x1, y1, x2, y2 = coords

        on_ground = False

        # Check collisions with all platforms
        for plat in all_platforms:
            px1, py1, px2, py2 = canvas.coords(plat)
            if (x2 > px1 and x1 < px2) and (y2 >= py1 and y2 <= py2 + 10) and y_velocity >= 0:
                y_velocity = 0
                on_ground = True
                canvas.move(character, 0, py1 - y2)
                if plat == goal_platform:
                    show_message()

        # Floor collision
        if y2 >= 400:
            y_velocity = 0
            on_ground = True
            canvas.move(character, 0, 400 - y2)

        # ---------------- Update character image ----------------
        if not on_ground:
            canvas.itemconfig(character, image=jumping_image)
        elif x_velocity != 0:
            canvas.itemconfig(character, image=walking_image)
        else:
            canvas.itemconfig(character, image=standing_image)

    root.after(30, move_character)


# ---------------- Key Handlers ----------------
def key_press(event):
    global x_velocity, y_velocity, on_ground
    if event.keysym.lower() == "q":
        return_to_menu()
        return
    if message_displayed and event.keysym == "space":
        hide_message()
        return
    if not message_displayed:
        if event.keysym == "Left":
            x_velocity = -5
        elif event.keysym == "Right":
            x_velocity = 5
        elif event.keysym == "space" and on_ground:
            y_velocity = jump_strength
            on_ground = False


def key_release(event):
    global x_velocity
    if not message_displayed and event.keysym in ["Left", "Right"]:
        x_velocity = 0


# ---------------- Bind Keys ----------------
root.bind("<KeyPress>", key_press)
root.bind("<KeyRelease>", key_release)

root.mainloop()
