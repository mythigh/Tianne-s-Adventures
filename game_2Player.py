import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
from tkinter import messagebox, simpledialog, ttk
import pygame  # sound

# ---------------- Initialize Pygame Mixer ----------------
pygame.mixer.init()
pygame.mixer.music.load('photos/music.mp3')
pygame.mixer.music.set_volume(0.1)
collect_channel = pygame.mixer.Channel(1)
effect_channel = pygame.mixer.Channel(2)
move_channel = pygame.mixer.Channel(3)
speak_channel = pygame.mixer.Channel(4)
walk_channel = pygame.mixer.Channel(5)

jump_sound = pygame.mixer.Sound("sounds/jump.wav")
jump_sound.set_volume(0.07)
bounce_sound = pygame.mixer.Sound("sounds/bounce.mp3")
bounce_sound.set_volume(0.07)
walk_sound = pygame.mixer.Sound("sounds/walk.mp3")
walk_sound.set_volume(0.1)
stone_sound = pygame.mixer.Sound("sounds/stone.mp3")
collected_sound = pygame.mixer.Sound("sounds/collected.mp3")
collected_sound.set_volume(0.1)
sparkle_sound = pygame.mixer.Sound("sounds/sparkle.mp3")
sparkle_sound.set_volume(0.1)
speach_sound = pygame.mixer.Sound("sounds/speach1.mp3")
speach_sound.set_volume(0.2)
speach2_sound = pygame.mixer.Sound("sounds/speach2.mp3")
speach2_sound.set_volume(0.2)
push_sound = pygame.mixer.Sound("sounds/push.mp3")
push_sound.set_volume(0.1)
lovesong_sound = pygame.mixer.Sound("sounds/lovesong.mp3")
lovesong_sound.set_volume(0.1)

cat_sound = pygame.mixer.Sound("sounds/cat.mp3")
cat_sound.set_volume(0.1)
dog_sound = pygame.mixer.Sound("sounds/dog.mp3")
dog_sound.set_volume(0.1)
poke_sound = pygame.mixer.Sound("sounds/poke.mp3")
poke_sound.set_volume(0.1)
pasta_sound = pygame.mixer.Sound("sounds/pasta.mp3")
pasta_sound.set_volume(0.1)
art_sound = pygame.mixer.Sound("sounds/art.mp3")
art_sound.set_volume(0.1)
# ---------------- Window Setup ----------------
root = tk.Tk()
root.title("Levi's Adventure")
root.geometry("600x400")

# ---------------- MENU with animated GIF background (REPLACES your static PNG block) ----------------
menu_frame = tk.Frame(root, width=600, height=400)
menu_frame.pack_propagate(False)  # keep fixed size
menu_frame.pack()

# Load animated GIF for menu background
menu_bg_path = "photos/tianne_adventure.gif"  # <-- ensure this .gif exists (change path/name if needed)
menu_bg_gif = Image.open(menu_bg_path)
menu_bg_frames = [
    ImageTk.PhotoImage(frame.copy().resize((600, 400), Image.Resampling.LANCZOS))
    for frame in ImageSequence.Iterator(menu_bg_gif)
]
_menu_bg_index = 0

# Label used as animated background
menu_bg_label = tk.Label(menu_frame)
menu_bg_label.place(x=0, y=0, relwidth=1, relheight=1)
menu_bg_label.lower()  # keep the background behind other widgets

def animate_menu_bg():
    global _menu_bg_index
    menu_bg_label.configure(image=menu_bg_frames[_menu_bg_index])
    menu_bg_label.image = menu_bg_frames[_menu_bg_index]  # prevent GC
    _menu_bg_index = (_menu_bg_index + 1) % len(menu_bg_frames)
    root.after(100, animate_menu_bg)  # adjust animation speed here (ms)

animate_menu_bg()

game_frame = tk.Frame(root, width=600, height=400)
game_frame.place(x=0, y=0)

# ---------------- Canvas ----------------
canvas = tk.Canvas(game_frame, width=600, height=400)
canvas.pack(fill="both", expand=True)

# ---------------- Load Background GIF ----------------
bg_gif = Image.open("photos/animated_background.gif")
bg_frames = [ImageTk.PhotoImage(frame.copy().resize((800, 450), Image.Resampling.LANCZOS))
             for frame in ImageSequence.Iterator(bg_gif)]
bg_frame_index = 0
bg_image_id = canvas.create_image(0, 0, image=bg_frames[0], anchor="nw", tags="background")

# ---------------- Load Images (Player 1 - Tia) ----------------
standing_img = Image.open("photos/tia_stand.png").resize((35, 62), Image.Resampling.LANCZOS)
standing_image = ImageTk.PhotoImage(standing_img)
standing_left_img = standing_img.transpose(Image.FLIP_LEFT_RIGHT)
standing_left_image = ImageTk.PhotoImage(standing_left_img)

walking_gif = Image.open("photos/tia_walk.gif")
walking_frames = [ImageTk.PhotoImage(frame.copy().resize((52, 62), Image.Resampling.LANCZOS))
                  for frame in ImageSequence.Iterator(walking_gif)]
walking_left_frames = [ImageTk.PhotoImage(frame.copy().resize((52, 62), Image.Resampling.LANCZOS).transpose(Image.FLIP_LEFT_RIGHT))
                       for frame in ImageSequence.Iterator(walking_gif)]

jumping_img = Image.open("photos/tia_jump.png").resize((52, 62), Image.Resampling.LANCZOS)
jumping_image = ImageTk.PhotoImage(jumping_img)
jumping_left_img = jumping_img.transpose(Image.FLIP_LEFT_RIGHT)
jumping_left_image = ImageTk.PhotoImage(jumping_left_img)

# ---------------- Load Images (Player 2 - MC) ----------------
mcstanding_img = Image.open("photos/mc_stand.png").resize((50, 65), Image.Resampling.LANCZOS)
mcstanding_image = ImageTk.PhotoImage(mcstanding_img)
mcstanding_left_img = mcstanding_img.transpose(Image.FLIP_LEFT_RIGHT)
mcstanding_left_image = ImageTk.PhotoImage(mcstanding_left_img)

mcwalking_gif = Image.open("photos/mc_walk.gif")
mcwalking_frames = [ImageTk.PhotoImage(frame.copy().resize((50, 65), Image.Resampling.LANCZOS))
                  for frame in ImageSequence.Iterator(mcwalking_gif)]
mcwalking_left_frames = [ImageTk.PhotoImage(frame.copy().resize((50, 65), Image.Resampling.LANCZOS).transpose(Image.FLIP_LEFT_RIGHT))
                       for frame in ImageSequence.Iterator(mcwalking_gif)]

mcjumping_img = Image.open("photos/mc_jump.png").resize((50, 65), Image.Resampling.LANCZOS)
mcjumping_image = ImageTk.PhotoImage(mcjumping_img)
mcjumping_left_img = mcjumping_img.transpose(Image.FLIP_LEFT_RIGHT)
mcjumping_left_image = ImageTk.PhotoImage(mcjumping_left_img)

COLLECTIBLE_W, COLLECTIBLE_H = 40, 40

overlay_img = tk.PhotoImage(file="photos/redscreen.png")
# Cat GIF (animated), resized uniformly
cat_gif = Image.open("photos/cat.gif")
cat_frames = [ImageTk.PhotoImage(frame.copy().resize((COLLECTIBLE_W, COLLECTIBLE_H), Image.Resampling.LANCZOS))
              for frame in ImageSequence.Iterator(cat_gif)]

# Pokéball (Level 1) → 40x40
pokeball_img = ImageTk.PhotoImage(
    Image.open("photos/pokeball.png").resize((23, 20), Image.Resampling.LANCZOS)
)

paint_img = ImageTk.PhotoImage(
    Image.open("photos/paint.png").resize((40, 40), Image.Resampling.LANCZOS)
)

# Pasta (Level 3) → 50x35
pasta_img = ImageTk.PhotoImage(
    Image.open("photos/pasta.png").resize((50, 30), Image.Resampling.LANCZOS)
)

# Dog (Level 4) → 50x35
dog_img = ImageTk.PhotoImage(
    Image.open("photos/dog.png").resize((40, 40), Image.Resampling.LANCZOS)
)

# Heart (Level 4) → 35x35
heart_img = ImageTk.PhotoImage(
    Image.open("photos/heart.png").resize((35, 25), Image.Resampling.LANCZOS)
)

platform_base_pil = Image.open("photos/platform2.png")
trampoline_base_pil = Image.open("photos/trampoline.png")

# keep raw PIL frames (no conversion here)
_spider_pil = Image.open("photos/spider.gif")
SPIDER_PIL_FRAMES_PIL = [frame.copy() for frame in ImageSequence.Iterator(_spider_pil)]


# Pushable Block
block_img_pil = Image.open("photos/block.png").resize((50, 50), Image.Resampling.LANCZOS)
block_image = ImageTk.PhotoImage(block_img_pil)

# ---------------- SPIKE GIF (animated) ----------------
SPIKE_GIF_PATH = "photos/barb.gif"  # <-- put your animated spike GIF here
# Load once as PIL frames; we’ll resize per spike rect
try:
    _spike_pil = Image.open(SPIKE_GIF_PATH)
    SPIKE_PIL_FRAMES = [frm.copy() for frm in ImageSequence.Iterator(_spike_pil)]
except Exception:
    # Fallback: still works if the GIF is missing; animates a single frame
    _spike_fallback = Image.open("photos/barb.png")
    SPIKE_PIL_FRAMES = [_spike_fallback.copy()]

lives_img = ImageTk.PhotoImage(Image.open("photos/life.webp").resize((30, 30)))

# --- Load your GIF frames once at startup ---
overlay_frames = []
confetti_gif = Image.open("photos/confetti.gif")  # <-- path to your gif

canvas_w = 600   # or use canvas.winfo_width() after canvas is drawn
canvas_h = 400   # same here

for frame in ImageSequence.Iterator(confetti_gif):
    resized = frame.copy().resize((canvas_w, canvas_h), Image.Resampling.LANCZOS)
    overlay_frames.append(ImageTk.PhotoImage(resized))

overlay_frame_index = 0
overlay_anim_id = None


# ---------------- Caches ----------------
trampoline_images_cache = []
platform_images_cache = []
spike_images_cache = []  # prevent GC of spike images

# ---------------- Game Variables ----------------
start_x, start_y = 20, 300
character = None           # Player 1
character2 = None          # Player 2 (active on Level 4)

goal_platform = None

all_platforms = []
yellow_platforms = []
collectibles = []
trampolines = []

x_velocity = 0
y_velocity = 0
gravity = 1
jump_strength = -17
trampoline_boost = -25

on_ground = False
facing_right = True
keys_disabled = False

# Player 2
x_velocity2 = 0
y_velocity2 = 0
on_ground2 = False
facing_right2 = True

game_running = False
current_level = 0
game_loop_id = None
level_text_id = None

message_displayed = False
popup_ids = []
spiders = []
toast_id = None
toast_bg_id = None
walking_frame_index = 0
walking_frame_index2 = 0

# --- ENDING / FINAL CINEMATIC STATE ---
final_cinematic_running = False     # we are in the end sequence
final_cinematic_phase = None        # None | 'drop' | 'run' | 'wait'
final_return_scheduled = False
cinematic_no_clamp = False          # disable screen-edge clamp while running offscreen
goal_extra_ids = []                 # to remove decorative goal images

lives = 3
life_icons = []

awaiting_answer = False

# ======== NEW: Lives/Health for Character 1 =========
max_lives = 3
player_lives = max_lives
lives_text_ids = []

# ======== NEW: Spike/hazard reset state =========
awaiting_spike_reset = False  # when True, movement is frozen until SPACE is pressed

def play_music():
    pygame.mixer.music.play(-1)

# ---------------- Menu ----------------
def show_instructions():
    messagebox.showinfo(
        "Instructions",
        "Controls:\n"
        "Left Arrow → Move Left\n"
        "Right Arrow → Move Right\n"
        "Up Arrow → Jump\n"
        "Q → Return to Menu\n\n"
        "Rules:\n"
        "• Collect all items before stepping on goal platform.\n"
        "• AVOID THE SPIDERS AND SPIKES!.\n"
    )

def start_game():
    global game_running, current_level, player_lives
    menu_frame.lower()
    game_frame.lift()
    game_running = True
    current_level = 5     # (0-based)
    player_lives = max_lives  # NEW: reset lives on a fresh start
    init_level(current_level)

    move_character()
    animate_background()
    animate_walking()
    animate_cats()
    animate_collectibles()
    animate_spiders()
    animate_spikes()  # <-- add this


def return_to_menu(event=None):
    global game_running, character, character2, goal_platform, all_platforms, yellow_platforms, collectibles, trampolines, awaiting_spike_reset, final_cinematic_running
    game_running = False
    final_cinematic_running = False
    pygame.mixer.music.play()
    canvas.delete("game")
    all_platforms.clear()
    yellow_platforms.clear()
    collectibles.clear()
    trampolines.clear()
    clear_popup()
    clear_toast()
    game_frame.lower()
    menu_frame.lift()
    # character2 = None
    awaiting_spike_reset = False
    try:
        if lovesong_channel.get_busy():
            lovesong_channel.fadeout(1000)  # fade out over 2s
    except Exception:
        pass

    pygame.mixer.music.unpause()

    enable_all_keys()


def game_loop():
    global game_loop_id
    # --- your update logic (movement, collisions, redraws, etc.) ---

    # schedule next loop
    game_loop_id = root.after(16, game_loop)  # 60 FPS

def init_button_style():
    style = ttk.Style()
    # Use a theme that lets us color buttons (Aqua ignores colors)
    try:
        style.theme_use('clam')
    except tk.TclError:
        pass

    style.configure(
        'Game.TButton',
        background='#84cb53',   # idle bg
        foreground='white',
        # 222222
        borderwidth=0,
        padding=(3, 0),
        font = ("PixelPurl", 30)
    )
    style.map(
        'Game.TButton',
        background=[('active', '#7B3F00'), ('pressed', '#000000'), ('disabled', '#444444')],
        foreground=[('disabled', '#aaaaaa')]
    )

# call once after creating root
init_button_style()
start_btn = ttk.Button(menu_frame, text="START GAME", command=start_game, style='Game.TButton', takefocus=0)
instructions_btn = ttk.Button(menu_frame, text="INSTRUCTIONS", command=show_instructions, style='Game.TButton', takefocus=0)

start_btn.place(relx=0.375, rely=0.95, anchor="center", y= -10)

instructions_btn.place(relx=0.625, rely=0.95, anchor="center", y =-10)
# ---------------- Level Data ----------------
level_data = [
    {   # Level 1
        "platforms": [
            (150, 320, 250, 340, "yellow"),
            (320, 280, 420, 300, "yellow"),
        ],
        "goal": (480, 250, 580, 270),
        "collectibles": [(200, 300)],
        "trampolines": [],
        "question": "What is Pokemon short for? 🐣",
        "answer": "",
        "type": "poke",
    },
    {   # Level 2
        "platforms": [
            (100, 300, 200, 320, "yellow"),
            (280, 220, 380, 240, "yellow"),
            (100, 135, 200, 155, "yellow"),
        ],
        "goal": (470, 130, 570, 150),
        "collectibles": [(150, 100)],
        "trampolines": [],
        "question": "What was Levi's previous name? 🐈",
        "answer": "",
        "type": "cat",
    },
    {   # Level 3  (spikes added below)
        "platforms": [
            (100, 300, 200, 320, "yellow"),
            (330, 240, 430, 260, "yellow"),
            (120, 140, 220, 160, "yellow"),
        ],
        "goal": (330, 100, 430, 120),
        "collectibles": [(170, 110)],
        "trampolines": [],
        "spikes": [              # spike areas (x1,y1,x2,y2) -> one image per area
            (125, 255, 175, 305),
            (355, 195, 405, 245),
        ],
        "question": "When Tianne was younger she once screamed out what food? 🍝",
        "answer": "",
        "type": "pasta",
    },
    {  # Level 4
        "platforms": [(20, 150, 120, 170, "yellow")],
        "goal": (470, 150, 580, 170),
        "collectibles": [(60, 135)],
        "trampolines": [(250, 330, 350, 350)],
        "spikes": [              # spike areas (x1,y1,x2,y2) -> one image per area
            (345, 320, 395, 370),
            (200, 320, 250, 370),
        ],
        "question": "whats mc's favourite art work from you? 🎨 \n(it's all of them just press enter)",
        "answer": "",
        "type": "art",
    },
{  # Level 5 – Trampoline + Spikes + Spider Gauntlet
    "platforms": [
        # (330, 250, 430, 270, "yellow"),  # mid ledge you must reach via trampoline
        (100, 270, 530, 290, "yellow"),  # approach to goal
    ],
    "goal": (250, 150, 350, 170),
    "collectibles": [(560, 330)],       # hover near spider’s patrol to add risk
    "trampolines": [(250, 330, 350, 350)],
    "pushables": [(50, 330)],
    "spikes": [
               # punish late jumps on the right
    ],
    # (x, y, w, h, patrol_left, patrol_right, speed)
    # Patrols along the mid ledge; time your landings!
    "spiders": [
        (330, 325, 150, 70, 105, 350, 5),
    ],
    "question": "whats your favourite dog? 🐕",
    "answer": "",
    "type": "dog",
},
    {  # Level 6
        "platforms": [],
        "goal": (350, 260, 430, 280),
        "collectibles": [(400, 135)],
        "trampolines": [],
        "pushables": [(80, 330)],
        "question": "Wanna like.. like be my.. like girlfriend 👉👈?",
        "answer": "",
        "type": "heart"
    }
]

# ---------------- Helpers ----------------
def add_platform(x1, y1, x2, y2, color, kind=None):
    global platform_images_cache
    width = int(x2 - x1)
    height = int(y2 - y1)

    if color == "yellow":
        resized = platform_base_pil.resize((max(1,width), max(1,height)), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(resized)
        platform_images_cache.append(img_tk)
        pid = canvas.create_image(x1, y1, image=img_tk, anchor="nw", tags="game")
        ptype = kind or "yellow"
    else:
        pid = canvas.create_rectangle(x1, y1, x2, y2, fill=color, width=0, tags="game")
        ptype = kind or color

    data = {"id": pid, "bbox": (x1, y1, x2, y2), "type": ptype}
    all_platforms.append(data)
    if ptype == "yellow":
        yellow_platforms.append(data)
    return pid

def add_goal(x1, y1, x2, y2):
    return add_platform(x1, y1, x2, y2, "", kind="goal")

# ======== SPIKE IMAGE: drawing helper (replaces triangle strip) =========
def add_spike_strip(x1, y1, x2, y2):
    """
    Place an animated spike GIF fitted to the given bbox and register a hazard.
    Stores frames on the platform entry so we can animate later.
    """
    width  = max(1, int(x2 - x1))
    height = max(1, int(y2 - y1))

    # Resize the source GIF frames for this spike’s size
    frames = [
        ImageTk.PhotoImage(frm.copy().resize((width, height), Image.Resampling.LANCZOS))
        for frm in SPIKE_PIL_FRAMES
    ]

    # Keep refs to prevent GC
    if not hasattr(canvas, "spike_frames_cache"):
        canvas.spike_frames_cache = []
    canvas.spike_frames_cache.extend(frames)

    sid = canvas.create_image(x1, y1, image=frames[0], anchor="nw", tags="game")

    all_platforms.append({
        "id": sid,
        "bbox": (x1, y1, x2, y2),
        "type": "spike",
        "frames": frames,
        "frame": 0
    })


def animate_background():
    global bg_frame_index
    if not game_running:
        root.after(100, animate_background)
        return
    canvas.itemconfig(bg_image_id, image=bg_frames[bg_frame_index])
    bg_frame_index = (bg_frame_index + 1) % len(bg_frames)
    root.after(100, animate_background)


def add_floor():
    add_platform(0, 380, 900, 400, "", kind="floor")

def clear_popup():
    global popup_ids, message_displayed
    for pid in popup_ids:
        canvas.delete(pid)
    popup_ids = []
    message_displayed = False

def show_popup(text, persistent=False):
    global popup_ids, message_displayed
    clear_popup()
    rect = canvas.create_rectangle(130, 150, 470, 230, fill="black", outline="white", tags="game")
    txt = canvas.create_text(300, 190, text=text, fill="white", font=("Arial", 16), tags="game")
    popup_ids = [rect, txt]
    message_displayed = persistent
    if not persistent:
        root.after(1500, clear_popup)

def clear_toast():
    global toast_id, toast_bg_id
    if toast_id:
        canvas.delete(toast_id)
        toast_id = None
    if toast_bg_id:
        canvas.delete(toast_bg_id)
        toast_bg_id = None

def show_toast(text):
    global toast_id, toast_bg_id
    clear_toast()
    toast_bg_id = canvas.create_rectangle(180, 8, 420, 34, fill="black", outline="", tags="game")
    toast_id = canvas.create_text(300, 21, text=text, fill="white", font=("Arial", 11, "bold"), tags="game")
    root.after(1200, clear_toast)

# ---------------- Goal Decoration (GIF) ----------------
goal_decor_frames = []
goal_decor_index = 0
goal_decor_id = None

def add_goal_decorative_gif(x1, y1, x2, y2, gif_path):
    global goal_decor_frames, goal_decor_id, goal_decor_index
    pil_gif = Image.open(gif_path)
    goal_decor_frames = [ImageTk.PhotoImage(frame.copy().resize((int(x2 - x1 + 2), int(y2 - y1) + 35), Image.Resampling.LANCZOS))
                         for frame in ImageSequence.Iterator(pil_gif)]
    if not hasattr(canvas, "decorative_images"):
        canvas.decorative_images = []
    canvas.decorative_images.extend(goal_decor_frames)
    goal_decor_id = canvas.create_image(x1+10, y1-45, image=goal_decor_frames[0], anchor="nw", tags="game")
    animate_goal_decor()

def animate_goal_decor():
    global goal_decor_index, goal_decor_frames, goal_decor_id
    if not game_running or goal_decor_id is None or not goal_decor_frames:
        return
    goal_decor_index = (goal_decor_index + 1) % len(goal_decor_frames)
    canvas.itemconfig(goal_decor_id, image=goal_decor_frames[goal_decor_index])
    root.after(120, animate_goal_decor)

def add_goal_decorative_image(x1, y1, x2, y2, image_path):
    global goal_extra_ids
    pil_img = Image.open(image_path).resize((int(x2 - x1), int(y2 - y1)), Image.Resampling.LANCZOS)
    tk_img = ImageTk.PhotoImage(pil_img)
    if not hasattr(canvas, "decorative_images"):
        canvas.decorative_images = []
    canvas.decorative_images.append(tk_img)
    img_id = canvas.create_image(x1, y1, image=tk_img, anchor="nw", tags="game")
    goal_extra_ids.append(img_id)
def start_final_cinematic():
    """Show win message, clear goal+stone, then let both players fall to floor.
       When both are on the floor, auto-run right at speed 2 and return to menu after both exit."""
    global final_cinematic_running, final_cinematic_phase, cinematic_no_clamp
    global x_velocity, x_velocity2, facing_right, facing_right2, lovesong_channel

    if final_cinematic_running:
        return

    show_popup("Congrats, You Win! 🎉❤️\nGame Complete!", persistent=False)

    # 🔊 Play lovesong on a dedicated channel so it won't get cut off
    lovesong_channel = pygame.mixer.Channel(7)  # pick a free channel (0–7 usually safe)
    lovesong_channel.play(lovesong_sound, loops=0)

    pygame.mixer.music.pause()

    show_confetti_overlay()
    clear_goal_and_stone()          # they can now fall

    # enter 'drop' phase: physics continue, inputs disabled elsewhere
    final_cinematic_running = True
    final_cinematic_phase = 'drop'
    cinematic_no_clamp = False

    # stop any manual motion for the fall
    x_velocity = 0
    x_velocity2 = 0
    facing_right = True
    facing_right2 = True


# ---------------- Question Prompt ----------------
def ask_and_check_question(level_index):
    if level_index >= len(level_data):
        print("All levels complete! Returning to menu...")
        return
    global awaiting_answer
    data = level_data[level_index]
    q = data.get("question")
    a = str(data.get("answer", "")).strip().lower()
    if not q:
        advance_level()
        return
    while True:

        resp = simpledialog.askstring("Level Complete!", f"{q}\n\n(Type your answer)")
        if resp is None:
            continue
        if str(resp).strip().lower() == a:
            show_toast("Correct!")
            awaiting_answer = False
            walk_channel.set_volume(10)
            advance_level()
            return
        else:
            messagebox.showerror("Try Again", "That's not quite right. Try again!")

# ------------- Collectible image chooser (per-level) -------------
def collectible_frames_for_level(level_index):
    if level_index == 0:
        return [pokeball_img]
    elif level_index == 1:
        return cat_frames
    elif level_index == 2:
        return [pasta_img]
    elif level_index == 3:
        return [paint_img]
    elif level_index == 4:
        return [dog_img]
    elif level_index == 5:
        return [heart_img]
    else:
        return cat_frames

# ---------------- NEW: Lives UI ----------------
def update_lives_ui():
    """Draw 'LIVES: X' at the top-left with a shadow."""
    global lives_text_ids

# ---------------- Red Overlay ----------------
# ---------------- Red Overlay ----------------
def show_red_overlay():
    # Remove any previous overlay
    canvas.delete("overlay")

    # Draw the overlay image on top
    canvas.create_image(
        0, 0,
        anchor="nw",
        image=overlay_img,
        tags=("overlay", "game")
    )


def clear_red_overlay():
    canvas.delete("overlay")


def animate_overlay():
    """Loop through overlay gif frames."""
    global overlay_frame_index, overlay_anim_id

    if not overlay_frames:
        return

    # Update image on the existing canvas overlay item
    canvas.itemconfig("overlay", image=overlay_frames[overlay_frame_index])

    overlay_frame_index = (overlay_frame_index + 1) % len(overlay_frames)
    overlay_anim_id = canvas.after(100, animate_overlay)  # 100ms per frame (adjust as needed)


def show_confetti_overlay():
    # Remove any previous overlay
    canvas.delete("overlay")

    # Draw the first frame
    if overlay_frames:
        canvas.create_image(
            0, 0,
            anchor="nw",
            image=overlay_frames[0],
            tags=("overlay", "game")
        )

        # Start animation
        global overlay_frame_index
        overlay_frame_index = 0
        animate_overlay()


def clear_confetti_overlay():
    canvas.delete("overlay")

# ---------------- Initialize Level ----------------
def init_level(level_index):
    global game_loop_id
    # cancel old loop if it’s still running
    if game_loop_id is not None:
        root.after_cancel(game_loop_id)
        game_loop_id = None

    global character, character2, goal_platform, collectibles, all_platforms, yellow_platforms, level_text_id
    global x_velocity2, y_velocity2, on_ground2, facing_right2, awaiting_answer, awaiting_spike_reset
    global final_cinematic_running, final_cinematic_phase, cinematic_no_clamp, final_return_scheduled, goal_extra_ids

    canvas.delete("game")
    clear_popup()
    clear_toast()
    all_platforms.clear()
    yellow_platforms.clear()
    collectibles.clear()
    spiders.clear()
    awaiting_answer = False
    awaiting_spike_reset = False
    final_cinematic_running = False  # we are in the end sequence
    final_cinematic_phase = None  # None | 'drop' | 'run' | 'wait'
    final_return_scheduled = False
    cinematic_no_clamp = False  # disable screen-edge clamp while running offscreen
    goal_extra_ids = []  # to remove decorative goal images

    draw_lives(player_lives)


    if level_text_id:
        canvas.delete(level_text_id)
    if level_index < 6:
        myLevel = level_index + 1
    level_text_id = canvas.create_text(592, 16, anchor="ne",
                                       text=f"LEVEL {myLevel}",
                                       font=("PixelPurl", 30, "bold"),
                                       fill="#222222", tags="game")
    level_text_id = canvas.create_text(590, 14, anchor="ne",
                                       text=f"LEVEL {myLevel}",
                                       font=("PixelPurl", 30, "bold"),
                                       fill="white", tags="game")


    # NEW: draw lives indicator
    update_lives_ui()

    # Player 1
    global character
    character = canvas.create_image(start_x, start_y, image=standing_image, anchor="nw", tags="game")
    character2 = canvas.create_image(40, start_y, image=mcstanding_image, anchor="nw", tags="game")


    # Platforms
    data = level_data[level_index]
    for (x1, y1, x2, y2, color) in data["platforms"]:
        add_platform(x1, y1, x2, y2, color)

    # Goal (GIF)
    gx1, gy1, gx2, gy2 = data["goal"]
    goal_platform = add_goal(gx1, gy1, gx2, gy2)
    add_goal_decorative_gif(gx1, gy1, gx2, gy2, "photos/flag1.gif")
    add_goal_decorative_image(gx1, gy1, gx2, gy2, "photos/platform2.png")

    # Floor
    add_floor()

    # Trampolines
    for tramp in data["trampolines"]:
        x1, y1, x2, y2 = tramp
        width = int(x2 - x1)
        height = int(y2 - y1)
        resized = trampoline_base_pil.resize((max(1, width), max(1, height)), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(resized)
        trampoline_images_cache.append(img_tk)
        pid = canvas.create_image(x1, y1, image=img_tk, anchor="nw", tags="game")
        tramp_data = {"id": pid, "bbox": (x1, y1, x2, y2), "type": "trampoline"}
        trampolines.append(tramp_data)
        all_platforms.append(tramp_data)

    # ======== add spikes for this level (if any) ========
    for sp in data.get("spikes", []):
        sx1, sy1, sx2, sy2 = sp
        add_spike_strip(sx1, sy1, sx2, sy2)

    # Spiders (patrolling hazards)
    for sp in data.get("spiders", []):
        # tuple format: (x, y, w, h, patrol_left, patrol_right, speed)
        add_spider(*sp)

    # Collectibles (per-level, UNIFORM SIZE)
    frames_for_level = collectible_frames_for_level(level_index)
    for (cx, cy) in data["collectibles"]:
        first_frame = frames_for_level[0]
        cid = canvas.create_image(cx, cy, image=first_frame, anchor="center", tags="game")
        level = level_data[level_index]
        collectibles.append({
            "id": cid,
            "base_y": cy,
            "offset": 0.0,
            "dir": 1,
            "amp": 10.0,
            "step": 0.6,
            "frame": 0,
            "type": level["type"],
            "frames": frames_for_level
        })

    # Pushable blocks
    if "pushables" in data:
        for (bx, by) in data["pushables"]:
            bid = canvas.create_image(bx, by, image=block_image, anchor="nw", tags="game")
            all_platforms.append({"id": bid, "bbox": (bx+15, by, bx+35, by+40), "type": "pushable"})

    # Player 2 only on Level 5 (index 4) [note: presence controlled as before]
    if level_index >= 0 and character2 is None:
        character2 = canvas.create_image(40, start_y, image=mcstanding_image, anchor="nw", tags="game")
        x_velocity2 = 0
        y_velocity2 = 0
        on_ground2 = False
        facing_right2 = True
    # elif level_index != 5 and character2 is not None:
        # canvas.delete(character2)
        # character2 = None


    reset_character()

def add_spider(x, y, w, h, patrol_left, patrol_right, speed):
    # Build BOTH directions at the requested size
    right_frames_pil = [
        frm.copy().resize((int(w), int(h)), Image.Resampling.LANCZOS)
        for frm in SPIDER_PIL_FRAMES_PIL
    ]
    left_frames_pil = [im.transpose(Image.FLIP_LEFT_RIGHT) for im in right_frames_pil]

    right_frames = [ImageTk.PhotoImage(im) for im in right_frames_pil]
    left_frames  = [ImageTk.PhotoImage(im) for im in left_frames_pil]

    # Keep references to prevent GC
    if not hasattr(canvas, "spider_frames_cache"):
        canvas.spider_frames_cache = []
    canvas.spider_frames_cache.extend(right_frames + left_frames)

    vx = speed if speed != 0 else 2
    init_img = right_frames[0] if vx > 0 else left_frames[0]

    sid = canvas.create_image(x, y, image=init_img, anchor="nw", tags="game")
    data = {
        "id": sid,
        "bbox": (x, y, x + w, y + h),
        "type": "spider",
        "frames_right": right_frames,
        "frames_left": left_frames,
        "frame": 0,
        "w": w,
        "h": h,
        "vx": vx,
        "left": patrol_left,
        "right": patrol_right,
    }
    spiders.append(data)
    all_platforms.append(data)


def animate_spiders():
    if not game_running:
        root.after(120, animate_spiders)
        return

    for sp in spiders:
        x1, y1, x2, y2 = sp["bbox"]

        # Patrol + flip direction at bounds
        nx = x1 + sp["vx"]
        if nx < sp["left"] or nx > sp["right"]:
            sp["vx"] = -sp["vx"]
            nx = x1 + sp["vx"]

        # Choose the correct orientation based on current vx
        using_right = sp["vx"] >= 0
        frames = sp["frames_right"] if using_right else sp["frames_left"]

        # Animate current orientation
        sp["frame"] = (sp["frame"] + 1) % len(frames)
        canvas.itemconfig(sp["id"], image=frames[sp["frame"]])

        # Move and update bbox
        dx = nx - x1
        if dx:
            canvas.move(sp["id"], dx, 0)
            sp["bbox"] = (x1 + dx, y1, x2 + dx, y2)

    root.after(10, animate_spiders)


def animate_spikes():
    if not game_running:
        root.after(120, animate_spikes)
        return

    for plat in all_platforms:
        if plat.get("type") == "spike" and plat.get("frames"):
            plat["frame"] = (plat["frame"] + 1) % len(plat["frames"])
            canvas.itemconfig(plat["id"], image=plat["frames"][plat["frame"]])

    root.after(120, animate_spikes)

def reset_character():
    global x_velocity, y_velocity, on_ground
    global x_velocity2, y_velocity2, on_ground2
    if not character:
        return
    bbox = canvas.bbox(character)
    if bbox:
        x1, y1, x2, y2 = bbox
        canvas.move(character, start_x - x1, start_y - y1)
    x_velocity = 0
    y_velocity = 0
    on_ground = False

    if character2:
        x_velocity2 = 0
        y_velocity2 = 0
        on_ground2 = False

def draw_lives(player_lives):
    global life_icons
    # Clear old icons
    for icon in life_icons:
        canvas.delete(icon)
    life_icons = []
    # Draw one heart per life
    for i in range(player_lives):
        x = 20 + i * 27   # spacing
        y = 20
        icon = canvas.create_image(x, y, image=lives_img, anchor="nw", tags="game")
        life_icons.append(icon)

# ======== NEW: hazard hit handler (spikes/spiders hurt Player 1) =========
def on_spike_hit():
    global awaiting_spike_reset, x_velocity, y_velocity, player_lives

    if final_cinematic_running:
        return

    if awaiting_spike_reset:
        return
    stone_sound.play()
    x_velocity = 0
    y_velocity = 0

    # >>> ADD THIS <<<
    show_red_overlay()   # draw the red tint now (popup will render on top)

    # lose a life
    player_lives = max(0, player_lives - 1)
    draw_lives(player_lives)
    if player_lives <= 0:
        show_popup("oh no you lose. try again", persistent=True)
    else:
        show_popup(f"Ouch! You were hit.\nLives left: {player_lives}\nPress SPACE to try again.", persistent=True)
    awaiting_spike_reset = True


# ---------------- Movement / Physics ----------------
def rects_overlap(a, b):
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    return (ax2 > bx1 and ax1 < bx2 and ay2 > by1 and ay1 < by2)

def is_on_platform_type(entity_id, type_name):
    """True if entity's feet are on top of a platform of the given type."""
    if not entity_id:
        return False
    eb = canvas.bbox(entity_id)
    if not eb:
        return False
    ex1, ey1, ex2, ey2 = eb
    feet = ey2
    for plat in all_platforms:
        if plat.get("type") == type_name:
            gx1, gy1, gx2, gy2 = plat["bbox"]
            if (ex2 > gx1 and ex1 < gx2) and (gy1 - 6) <= feet <= (gy1 + 8):
                return True
    return False

def is_on_goal_platform(entity_id):
    return is_on_platform_type(entity_id, "goal")

def clear_goal_and_stone():
    """Remove goal platform, its decorations, and any pushable 'stone' blocks."""
    global goal_platform, goal_decor_id, goal_extra_ids
    # goal platform
    if goal_platform:
        canvas.delete(goal_platform)
        for p in list(all_platforms):
            if p.get("id") == goal_platform:
                all_platforms.remove(p)
                break
        goal_platform = None
    # decorations
    if goal_decor_id:
        canvas.delete(goal_decor_id)
        goal_decor_id = None
    for did in goal_extra_ids:
        canvas.delete(did)
    goal_extra_ids = []
    # stones (pushables)
    for p in list(all_platforms):
        if p.get("type") == "pushable":
            canvas.delete(p["id"])
            all_platforms.remove(p)

# --- Global input gate ---
keys_are_disabled = False

def _eat_event(event=None):
    # Returning "break" stops the event from reaching any other bindings
    return "break"

def disable_all_keys():
    """Completely disable game input during cinematics."""
    global keys_are_disabled
    if keys_are_disabled:
        return
    keys_are_disabled = True

    # Remove your game handlers
    try:
        root.unbind("<KeyPress>")
        root.unbind("<KeyRelease>")
    except Exception:
        pass

    # Swallow any stray key events app-wide
    root.bind_all("<KeyPress>", _eat_event)
    root.bind_all("<KeyRelease>", _eat_event)

def enable_all_keys():
    """Restore game input (call when you’re back at the menu)."""
    global keys_are_disabled
    if not keys_are_disabled:
        return
    keys_are_disabled = False

    # Stop swallowing events
    try:
        root.unbind_all("<KeyPress>")
        root.unbind_all("<KeyRelease>")
    except Exception:
        pass

    # Reattach your handlers
    root.bind("<KeyPress>", key_press)
    root.bind("<KeyRelease>", key_release)


def move_character():
    global y_velocity, on_ground, facing_right
    global y_velocity2, on_ground2, facing_right2, awaiting_answer, x_velocity, x_velocity2
    global final_cinematic_phase, final_return_scheduled, cinematic_no_clamp
    if not game_running:
        return


    # Freeze movement while waiting for spike reset
    if awaiting_spike_reset:
        root.after(30, move_character)
        return

    # --- Player 1 physics & collisions ---
    y_velocity += gravity
    canvas.move(character, x_velocity, y_velocity)

    coords = canvas.bbox(character)
    if not coords:
        root.after(30, move_character)
        return
    x1, y1, x2, y2 = coords

    if x1 < 0 and not cinematic_no_clamp:
        canvas.move(character, -x1, 0)
    elif x2 > 600 and not cinematic_no_clamp:
        canvas.move(character, 600 - x2, 0)

    on_ground = False
    landed_on_goal = False

    # FIX: compute previous bottom to prevent tunneling through floor/platforms
    prev_y2 = y2 - y_velocity

    for plat in all_platforms:
        px1, py1, px2, py2 = plat["bbox"]

        # ======== spikes/spiders act as hazard, not as a platform ========
        if plat["type"] in ("spike", "spider"):
            # Any overlap counts as a hit (slightly inset for fairness)
            if rects_overlap((x1+12, y1+12, x2-12, y2-10), (px1, py1, px2, py2)):
                on_spike_hit()
                # stop further processing to avoid snap/land after hit
                break
            continue

        # --- Land on top of platforms (including pushable) ---
        # FIX: anti-tunneling – detect crossing the top surface between frames
        if (x2 > px1 and x1 < px2) and (y_velocity >= 0) and (prev_y2 <= py1 + 4 <= y2):
            dy = (py1 + 4) - y2  # snap exactly onto the top
            canvas.move(character, 0, dy)
            y_velocity = 0
            on_ground = True
            if plat["type"] == "goal":
                landed_on_goal = True
            if plat["type"] == "trampoline":
                y_velocity = trampoline_boost
                on_ground = False
                bounce_sound.play()

        # --- Side collisions with PUSHABLE (Player 1 cannot push) ---
        if plat["type"] == "pushable":
            cx1, cy1, cx2, cy2 = canvas.bbox(character)
            on_top = (0 <= cy2 - py1 <= 5) and (cx2 > px1 and cx1 < px2)
            if on_top:
                continue
            else:
                if (cy2 > py1 and cy1 < py2):  # vertical overlap
                    if x_velocity > 0 and cx2 > px1 and cx1 < px1:  # walking right into block
                        overlap = cx2 - px1
                        if overlap > 0:

                            canvas.move(character, -overlap, 0)

                    elif x_velocity < 0 and cx1 < px2 and cx2 > px2:  # walking left into block
                        overlap = px2 - cx1
                        if overlap > 0:
                            canvas.move(character, overlap, 0)

            continue

    # --- Player 1 sprite state ---
    if not on_ground:
        canvas.itemconfig(character, image=jumping_image if facing_right else jumping_left_image)
    elif x_velocity == 0:
        canvas.itemconfig(character, image=standing_image if facing_right else standing_left_image)

    # --- Player 2 physics & collisions (only when present) ---
    landed_on_goal2 = False
    if character2:
        # NEW: flag to detect when Player 2 is actually pushing
        p2_slow = False

        y_velocity2 += gravity
        canvas.move(character2, x_velocity2, y_velocity2)

        coords2 = canvas.bbox(character2)
        if coords2:
            cx1, cy1, cx2, cy2 = coords2

            if cx1 < 0 and not cinematic_no_clamp:
                canvas.move(character2, -cx1, 0)
            elif cx2 > 800 and not cinematic_no_clamp:
                canvas.move(character2, 800 - cx2, 0)

            on_ground2 = False
            support_under_p2 = None

            # FIX: anti-tunneling for player 2 as well
            prev_y2_p2 = cy2 - y_velocity2

            for plat in all_platforms:
                px1, py1, px2, py2 = plat["bbox"]

                # Player 2: spikes hazard too (even though not present on Lv5)
                if plat["type"] == "spike":
                    if rects_overlap((cx1, cy1, cx2, cy2), (px1, py1, px2, py2)):
                        # Do NOT reduce Player 1 lives for Player 2 collisions.
                        # Simply freeze & show retry popup like a miss.
                        on_spike_hit()
                        break
                    continue

                # Land on top (anti-tunneling)
                if (cx2 > px1 and cx1 < px2) and (y_velocity2 >= 0) and (prev_y2_p2 <= py1 + 4 <= cy2):
                    dy2 = (py1 + 4) - cy2
                    canvas.move(character2, 0, dy2)
                    y_velocity2 = 0
                    on_ground2 = True
                    support_under_p2 = plat["type"]

                    if plat["type"] == "goal":
                        landed_on_goal2 = True
                    if plat["type"] == "trampoline":
                        y_velocity2 = trampoline_boost
                        bounce_sound.play()
                        on_ground2 = False

                # -------- Player 2 pushes block --------
                if plat["type"] == "pushable":
                    cx1, cy1, cx2, cy2 = canvas.bbox(character2)

                    if support_under_p2 == "pushable":
                        continue
                    if support_under_p2 != "floor":
                        continue

                    if (cy2 > py1 and cy1 < py2):
                        dx = 0
                        if x_velocity2 > 0 and cx2 > px1 and cx1 < px1:
                            dx = x_velocity2
                        elif x_velocity2 < 0 and cx1 < px2 and cx2 > px2:
                            dx = x_velocity2

                        if dx != 0:
                            nbx1 = px1 + dx
                            nbx2 = px2 + dx
                            if nbx1 < 0:
                                dx -= nbx1
                            if nbx2 > 600:
                                dx -= (nbx2 - 600)

                            can_move = True
                            test_bbox = (px1 + dx, py1, px2 + dx, py2)
                            for other in all_platforms:
                                if other is plat:
                                    continue
                                if other["type"] in ("yellow", "floor", "goal"):
                                    if rects_overlap(test_bbox, other["bbox"]):
                                        can_move = False
                                        break

                            if can_move and dx != 0:
                                # NEW: halve push speed and mark slowdown
                                if dx > 0:
                                    dx = max(1, dx // 2)
                                else:
                                    dx = min(-1, dx // 2)
                                p2_slow = True
                                push_sound.play()
                                canvas.move(plat["id"], dx, 0)
                                plat["bbox"] = (px1 + dx, py1, (px2) + dx, py2)

            # NEW: if pushing this frame, reduce Player 2's net horizontal movement by half
            if p2_slow and x_velocity2 != 0:
                sx = 1 if x_velocity2 >= 0 else -1
                # Pull back by the extra half-step so net = half speed
                adjust = - ( (abs(x_velocity2) - (abs(x_velocity2) // 2)) * sx )
                canvas.move(character2, adjust, 0)

                # re-clamp bounds after adjustment
                coords2 = canvas.bbox(character2)
                if coords2:
                    cx1, cy1, cx2, cy2 = coords2
                    if cx1 < 0:
                        canvas.move(character2, -cx1, 0)
                    elif cx2 > 800:
                        canvas.move(character2, 800 - cx2, 0)

            # --- Player 2 sprite state ---
            if not on_ground2:
                canvas.itemconfig(character2, image=mcjumping_image if facing_right2 else mcjumping_left_image)
            elif x_velocity2 == 0:
                canvas.itemconfig(character2, image=mcstanding_image if facing_right2 else mcstanding_left_image)

    # --- Collectible collection (by either player) ---
    for col in collectibles[:]:
        col_bbox = canvas.bbox(col["id"])
        if col_bbox:
            cx1, cy1, cx2, cy2 = col_bbox
            # player 1 overlap
            if (x2 > cx1 and x1 < cx2) and (y2 > cy1 and y1 < cy2):
                canvas.delete(col["id"])
                collectibles.remove(col)
                if col["type"] == "heart":
                    collect_channel.play(collected_sound)
                elif col["type"] == "cat":
                    effect_channel.play(collected_sound)
                    collect_channel.play(cat_sound)
                elif col["type"] == "dog":
                    effect_channel.play(collected_sound)
                    collect_channel.play(dog_sound)
                elif col["type"] == "art":
                    effect_channel.play(collected_sound)
                    collect_channel.play(art_sound)
                elif col["type"] == "poke":
                    effect_channel.play(collected_sound)
                    collect_channel.play(poke_sound)
                elif col["type"] == "pasta":
                    effect_channel.play(collected_sound)
                    collect_channel.play(pasta_sound)
                show_toast("Item collected!")
                continue
            # player 2 overlap
            if character2:
                p2 = canvas.bbox(character2)
                if p2:
                    px1, py1, px2, py2 = p2
                    if (px2 > cx1 and px1 < cx2) and (py2 > cy1 and py1 < cy2):
                        canvas.delete(col["id"])
                        collectibles.remove(col)
                        collected_sound.play()
                        show_toast("Item collected!")
                        continue


    # --- Final cinematic phase machine ---
    if final_cinematic_running:

        if final_cinematic_phase == 'drop':
            # wait until BOTH are standing on the floor
            if is_on_platform_type(character, 'floor') and (character2 is None or is_on_platform_type(character2, 'floor')):
                final_cinematic_phase = 'run'
                cinematic_no_clamp = True
                disable_all_keys()
                x_velocity = 2
                if character2:
                    x_velocity2 = 2


        elif final_cinematic_phase == 'run':
            b1 = canvas.bbox(character)
            b2 = canvas.bbox(character2) if character2 else None
            off1 = bool(b1 and b1[0] > 620)
            off2 = bool((not character2) or (b2 and b2[0] > 620))
            if off1 and off2 and not final_return_scheduled:
                final_cinematic_phase = 'wait'
                final_return_scheduled = True
                # stop walking but keep no_clamp True so nothing snaps back
                x_velocity = 0
                if character2:
                    x_velocity2 = 0
                root.after(4000, return_to_menu)
        # no special handling needed for 'wait'

    # --- Goal reached logic ---
    if final_cinematic_running:
        pass  # ignore goal logic during ending
    else:
        last_level = (current_level == len(level_data) - 1)
        if last_level:
            both_on_goal = (
                    len(collectibles) == 0
                    and character2 is not None
                    and is_on_goal_platform(character)
                    and is_on_goal_platform(character2)
            )
            if both_on_goal and not final_cinematic_running:
                start_final_cinematic()
            elif ((locals().get('landed_on_goal', False) or locals().get('landed_on_goal2', False))
                  and len(collectibles) > 0):
                show_toast("Collect all items before reaching the goal!")
        else:
            if ((locals().get('landed_on_goal', False) or locals().get('landed_on_goal2', False))
                    and len(collectibles) == 0):
                if not awaiting_answer:
                    awaiting_answer = True
                    walk_channel.set_volume(0)
                    ask_and_check_question(current_level)
            elif ((locals().get('landed_on_goal', False) or locals().get('landed_on_goal2', False))
                  and len(collectibles) > 0):
                show_toast("Collect all items before reaching the goal!")

    root.after(30, move_character)

# ---------------- Animation ----------------
def animate_cats():
    if not game_running:
        return
    # Only animate if the collectible has multiple frames (i.e., cat gif)
    for col in collectibles:
        frames = col.get("frames", [])
        if len(frames) > 1:
            col["frame"] = (col["frame"] + 1) % len(frames)
            canvas.itemconfig(col["id"], image=frames[col["frame"]])
    root.after(120, animate_cats)

def animate_walking():
    global walking_frame_index, walking_frame_index2
    if not game_running:
        return
    # Player 1 walking frames
    coords = canvas.coords(character)
    if coords and x_velocity != 0 and on_ground:
        if facing_right:
            canvas.itemconfig(character, image=walking_frames[walking_frame_index])
        else:
            canvas.itemconfig(character, image=walking_left_frames[walking_frame_index])
        walking_frame_index = (walking_frame_index + 1) % len(walking_frames)

        if walking_frame_index == 0:
            walk_channel.play(walk_sound)

    # Player 2 walking frames (only when present)
    if character2:
        coords2 = canvas.coords(character2)
        if coords2 and x_velocity2 != 0 and on_ground2:
            if facing_right2:
                canvas.itemconfig(character2, image=mcwalking_frames[walking_frame_index2])
            else:
                canvas.itemconfig(character2, image=mcwalking_left_frames[walking_frame_index2])
            walking_frame_index2 = (walking_frame_index2 + 1) % len(mcwalking_frames)

            if walking_frame_index2 == 0:
                walk_channel.play(walk_sound)

    root.after(80, animate_walking)

def animate_collectibles():
    if not game_running:
        return
    for col in collectibles:
        if col["offset"] >= col["amp"]:
            col["dir"] = -1
        elif col["offset"] <= -col["amp"]:
            col["dir"] = 1
        col["offset"] += col["dir"] * col["step"]
        x, _ = canvas.coords(col["id"])
        canvas.coords(col["id"], x, col["base_y"] + col["offset"])
    root.after(30, animate_collectibles)

# ---------------- Keys ----------------
def key_press(event):
    global x_velocity, y_velocity, on_ground, facing_right
    global x_velocity2, y_velocity2, on_ground2, facing_right2, awaiting_spike_reset
    global player_lives, max_lives, current_level

    if keys_disabled:
        return  # ignore all keystrokes

    if final_cinematic_running:
        return

    ks = event.keysym

    if ks.lower() == "q":
        return_to_menu()
        return

    # ======== handle popup-close + reset after hazard hit ========
    if ks == "space":
        if awaiting_spike_reset:
            clear_red_overlay()
            clear_popup()
            awaiting_spike_reset = False
            if player_lives <= 0:
                player_lives = max_lives
                current_level = 0
            init_level(current_level)
        # otherwise: ignore space completely during gameplay
        return

    # Prevent space from doing anything else accidentally
    if ks == "space":
        return

    if ks.lower() == "8" and current_level > 3:
        speak_channel.play(speach_sound)

    if ks.lower() == "y" and current_level > 3:
        speak_channel.play(speach2_sound)

    # Player 1 controls (arrows + space)
    if ks == "Left":
        x_velocity = -5
        facing_right = False
    elif ks == "Right":
        x_velocity = 5
        facing_right = True
    elif ks == ("Up"):
        if on_ground:
            y_velocity = jump_strength
            on_ground = False
            move_channel.play(jump_sound)

    # Player 2 controls (Level 5 only): A/D to move, W to jump
    if character2:
        if ks.lower() == "a":
            x_velocity2 = -5
            facing_right2 = False
        elif ks.lower() == "d":
            x_velocity2 = 5
            facing_right2 = True
        elif ks.lower() == "w":
            if on_ground2:
                y_velocity2 = jump_strength
                on_ground2 = False
                move_channel.play(jump_sound)
def key_release(event):
    global x_velocity, x_velocity2
    ks = event.keysym
    if ks in ("Left", "Right"):
        x_velocity = 0
    if character2:
        if ks.lower() in ("a", "d"):
            x_velocity2 = 0

def advance_level():
    global current_level
    clear_popup()
    current_level += 1
    sparkle_sound.play()
    if current_level < len(level_data):
        init_level(current_level)
    else:

        show_popup("Congrats, You Win! 🎉\nGame Complete!", persistent=False)
        root.after(5000, return_to_menu)

# ---------------- Bind Keys ----------------
root.bind("<KeyPress>", key_press)
root.bind("<KeyRelease>", key_release)

# ---------------- Start with Menu ----------------
menu_frame.lift()
play_music()
root.mainloop()
