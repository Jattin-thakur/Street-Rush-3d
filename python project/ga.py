import ursina
import random
import json
import os

# =========================================================
# GAME WINDOW SETUP
# =========================================================
app = ursina.Ursina()

ursina.window.title = "Street Rush 3D - Ultimate Racing"
ursina.window.borderless = False
ursina.window.color = ursina.color.rgb(100, 180, 255)
ursina.window.show_ursina_splash = False

# =========================================================
# SAVE SYSTEM
# =========================================================
SAVE_FILE = "racing_save.json"

default_save = {
    "coins": 0,
    "best_score": 0,
    "selected_car": 0,
    "unlocked_cars": [0],
    "max_level": 1
}

save_data = default_save.copy()

def load_game():
    global save_data
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as file:
                old_data = json.load(file)
            save_data = default_save.copy()
            save_data.update(old_data)
            if "unlocked_cars" not in save_data:
                save_data["unlocked_cars"] = [0]
            if "selected_car" not in save_data or save_data["selected_car"] not in save_data["unlocked_cars"]:
                save_data["selected_car"] = 0
            if "max_level" not in save_data:
                save_data["max_level"] = 1
        except Exception:
            save_data = default_save.copy()

def save_game():
    try:
        with open(SAVE_FILE, "w") as file:
            json.dump(save_data, file, indent=4)
    except Exception as e:
        print("Save error:", e)

load_game()

# =========================================================
# CAR CATALOGUE
# =========================================================
CARS_DATA = [
    {
        "name": "Red Racer",
        "color": ursina.color.red,
        "price": 0,
        "speed_bonus": 0,
        "accent": ursina.color.black
    },
    {
        "name": "Blue Storm",
        "color": ursina.color.azure,
        "price": 50,
        "speed_bonus": 2,
        "accent": ursina.color.white
    },
    {
        "name": "Golden GT",
        "color": ursina.color.gold,
        "price": 100,
        "speed_bonus": 4,
        "accent": ursina.color.orange
    },
    {
        "name": "Green Beast",
        "color": ursina.color.lime,
        "price": 200,
        "speed_bonus": 6,
        "accent": ursina.color.black
    },
    {
        "name": "Purple X",
        "color": ursina.color.violet,
        "price": 350,
        "speed_bonus": 9,
        "accent": ursina.color.cyan
    }
]

# =========================================================
# VIBRANT LEVEL THEMES (CITY, DESERT, ICE, SPACE, VOLCANO)
# =========================================================
LEVEL_THEMES = [
    {
        "name": "City Highway",
        "sky_color": ursina.color.rgb(100, 180, 255),       # Bright Sky Blue
        "ground_color": ursina.color.rgb(50, 180, 70),       # Grass Green
        "road_color": ursina.color.rgb(50, 50, 60),          # Asphalt Grey
        "rail_color": ursina.color.white,
        "stripe_color": ursina.color.red,
        "line_color": ursina.color.yellow,
        "prop_trunk_color": ursina.color.rgb(120, 70, 30),
        "prop_foliage_color": ursina.color.rgb(40, 180, 60),
        "prop_type": "tree"
    },
    {
        "name": "Desert Canyon",
        "sky_color": ursina.color.rgb(255, 140, 50),        # Sunset Orange
        "ground_color": ursina.color.rgb(235, 170, 80),      # Desert Sand
        "road_color": ursina.color.rgb(85, 60, 45),          # Terracotta Road
        "rail_color": ursina.color.rgb(210, 100, 30),        # Rust Orange
        "stripe_color": ursina.color.yellow,
        "line_color": ursina.color.white,
        "prop_trunk_color": ursina.color.rgb(40, 160, 60),    # Cactus Green
        "prop_foliage_color": ursina.color.rgb(255, 210, 40),
        "prop_type": "cactus"
    },
    {
        "name": "Arctic Glacier",
        "sky_color": ursina.color.rgb(130, 210, 255),       # Ice Cyan Sky
        "ground_color": ursina.color.rgb(235, 248, 255),     # Snow White
        "road_color": ursina.color.rgb(40, 80, 120),         # Ice Blue Road
        "rail_color": ursina.color.cyan,
        "stripe_color": ursina.color.azure,
        "line_color": ursina.color.cyan,
        "prop_trunk_color": ursina.color.rgb(160, 220, 255),
        "prop_foliage_color": ursina.color.white,
        "prop_type": "ice_pine"
    },
    {
        "name": "Neon Cyber Space",
        "sky_color": ursina.color.rgb(25, 10, 50),          # Midnight Purple Space
        "ground_color": ursina.color.rgb(65, 20, 100),        # Synthwave Grid Purple
        "road_color": ursina.color.rgb(25, 25, 40),          # Cyber Black Road
        "rail_color": ursina.color.magenta,
        "stripe_color": ursina.color.cyan,
        "line_color": ursina.color.magenta,
        "prop_trunk_color": ursina.color.cyan,                # Neon Light Poles
        "prop_foliage_color": ursina.color.magenta,
        "prop_type": "neon_beacon"
    },
    {
        "name": "Volcanic Inferno",
        "sky_color": ursina.color.rgb(220, 40, 20),         # Fiery Lava Red
        "ground_color": ursina.color.rgb(60, 20, 20),        # Obsidian Rock
        "road_color": ursina.color.rgb(40, 28, 28),          # Charcoal Road
        "rail_color": ursina.color.orange,
        "stripe_color": ursina.color.yellow,
        "line_color": ursina.color.red,
        "prop_trunk_color": ursina.color.rgb(80, 30, 20),
        "prop_foliage_color": ursina.color.rgb(255, 110, 0),   # Lava Flame Orange
        "prop_type": "volcano_spire"
    }
]

def get_level_target(lvl):
    return 15 + (lvl - 1) * 15

def get_level_theme(lvl):
    idx = (lvl - 1) % len(LEVEL_THEMES)
    return LEVEL_THEMES[idx]

# =========================================================
# GAME STATE VARIABLES
# =========================================================
score = 0
current_level = 1
level_target = get_level_target(1)

base_speed = 15
current_speed = 15
nitro = 100

game_over = False
game_started = False
game_paused = False
level_complete = False
shop_open = False
is_nitro_active = False

LANES = [-4.5, -2.25, 0, 2.25, 4.5]

# =========================================================
# 3D WORLD & ENVIRONMENT SETUP
# =========================================================
# Built-in Sky Entity
sky = ursina.Sky(color=ursina.color.rgb(100, 180, 255))
sky.texture = None

# Ground Grass / Sand / Snow / Synthwave Terrain
ground = ursina.Entity(
    model="plane",
    scale=300,
    position=(0, -0.05, 50),
    color=ursina.color.rgb(50, 180, 70)
)

# Asphalt Road
road = ursina.Entity(
    model="cube",
    scale=(14, 0.2, 300),
    position=(0, 0.05, 50),
    color=ursina.color.rgb(50, 50, 60)
)

# Side Guard Rails
left_rail = ursina.Entity(
    model="cube",
    scale=(0.4, 0.5, 300),
    position=(-7.1, 0.3, 50),
    color=ursina.color.white
)
right_rail = ursina.Entity(
    model="cube",
    scale=(0.4, 0.5, 300),
    position=(7.1, 0.3, 50),
    color=ursina.color.white
)

# Safety Strip Borders
left_stripe = ursina.Entity(
    model="cube",
    scale=(0.6, 0.25, 300),
    position=(-6.6, 0.16, 50),
    color=ursina.color.red
)
right_stripe = ursina.Entity(
    model="cube",
    scale=(0.6, 0.25, 300),
    position=(6.6, 0.16, 50),
    color=ursina.color.red
)

# Dynamic Moving Road Markings
road_lines = []
for z in range(-60, 200, 12):
    for x in (-2.25, 2.25):
        line = ursina.Entity(
            model="cube",
            scale=(0.25, 0.05, 4.5),
            position=(x, 0.18, z),
            color=ursina.color.yellow
        )
        road_lines.append(line)

# Side Scenery Props List
scenery_props = []

# Camera default setup
ursina.camera.position = (0, 6, -20)
ursina.camera.rotation_x = 15

# =========================================================
# APPLY THEME TO WORLD
# =========================================================
def apply_level_theme(theme):
    sky.color = theme["sky_color"]
    sky.texture = None
    ursina.window.color = theme["sky_color"]
    ground.color = theme["ground_color"]
    road.color = theme["road_color"]
    left_rail.color = theme["rail_color"]
    right_rail.color = theme["rail_color"]
    left_stripe.color = theme["stripe_color"]
    right_stripe.color = theme["stripe_color"]

    for line in road_lines:
        line.color = theme["line_color"]

    # Rebuild scenery props according to current theme type
    for p in scenery_props:
        ursina.destroy(p)
    scenery_props.clear()

    prop_type = theme["prop_type"]

    for z in range(-50, 200, 25):
        for side in (-11, 11):
            if prop_type == "tree":
                trunk = ursina.Entity(
                    model="cube",
                    scale=(0.6, 3.5, 0.6),
                    position=(side, 1.75, z),
                    color=theme["prop_trunk_color"]
                )
                foliage = ursina.Entity(
                    parent=trunk,
                    model="sphere",
                    scale=(3.5, 3.5, 3.5),
                    position=(0, 0.8, 0),
                    color=theme["prop_foliage_color"]
                )
            elif prop_type == "cactus":
                trunk = ursina.Entity(
                    model="cube",
                    scale=(0.7, 4.0, 0.7),
                    position=(side, 2.0, z),
                    color=theme["prop_trunk_color"]
                )
                ursina.Entity(
                    parent=trunk,
                    model="cube",
                    scale=(2.0, 0.5, 0.5),
                    position=(0, 0.2, 0),
                    color=theme["prop_trunk_color"]
                )
                ursina.Entity(
                    parent=trunk,
                    model="cube",
                    scale=(0.5, 1.2, 0.5),
                    position=(0.8, 0.6, 0),
                    color=theme["prop_trunk_color"]
                )
                ursina.Entity(
                    parent=trunk,
                    model="cube",
                    scale=(0.5, 1.2, 0.5),
                    position=(-0.8, 0.6, 0),
                    color=theme["prop_trunk_color"]
                )
            elif prop_type == "ice_pine":
                trunk = ursina.Entity(
                    model="cube",
                    scale=(0.5, 2.0, 0.5),
                    position=(side, 1.0, z),
                    color=theme["prop_trunk_color"]
                )
                foliage = ursina.Entity(
                    parent=trunk,
                    model="cone",
                    scale=(3.2, 4.5, 3.2),
                    position=(0, 1.5, 0),
                    color=theme["prop_foliage_color"]
                )
            elif prop_type == "neon_beacon":
                trunk = ursina.Entity(
                    model="cube",
                    scale=(0.4, 5.0, 0.4),
                    position=(side, 2.5, z),
                    color=theme["prop_trunk_color"]
                )
                ursina.Entity(
                    parent=trunk,
                    model="cube",
                    scale=(1.4, 1.4, 1.4),
                    position=(0, 0.6, 0),
                    color=theme["prop_foliage_color"]
                )
            elif prop_type == "volcano_spire":
                trunk = ursina.Entity(
                    model="cone",
                    scale=(2.5, 5.0, 2.5),
                    position=(side, 2.5, z),
                    color=theme["prop_trunk_color"]
                )
                ursina.Entity(
                    parent=trunk,
                    model="sphere",
                    scale=(1.2, 1.2, 1.2),
                    position=(0, 0.5, 0),
                    color=theme["prop_foliage_color"]
                )
            scenery_props.append(trunk)

# Apply default level 1 theme at startup
apply_level_theme(LEVEL_THEMES[0])

# =========================================================
# CAR CREATION HELPER
# =========================================================
def build_car_entity(color, accent_color=ursina.color.black, is_player=False):
    root = ursina.Entity()

    chassis = ursina.Entity(
        parent=root,
        model="cube",
        scale=(1.6, 0.55, 3.2),
        position=(0, 0.55, 0),
        color=color
    )

    cabin = ursina.Entity(
        parent=root,
        model="cube",
        scale=(1.1, 0.45, 1.6),
        position=(0, 0.95, -0.1),
        color=accent_color
    )

    ursina.Entity(
        parent=root,
        model="cube",
        scale=(1.0, 0.35, 0.4),
        position=(0, 0.96, 0.6),
        rotation_x=25,
        color=ursina.color.rgb(120, 200, 245)
    )

    ursina.Entity(
        parent=root,
        model="cube",
        scale=(1.0, 0.35, 0.4),
        position=(0, 0.96, -0.75),
        rotation_x=-25,
        color=ursina.color.rgb(80, 140, 180)
    )

    for x in (-0.55, 0.55):
        ursina.Entity(
            parent=root,
            model="cube",
            scale=(0.3, 0.15, 0.1),
            position=(x, 0.55, 1.6),
            color=ursina.color.white
        )

    for x in (-0.55, 0.55):
        ursina.Entity(
            parent=root,
            model="cube",
            scale=(0.3, 0.15, 0.1),
            position=(x, 0.55, -1.6),
            color=ursina.color.red
        )

    for x in (-0.85, 0.85):
        for z in (-0.9, 0.9):
            wheel = ursina.Entity(
                parent=root,
                model="cube",
                scale=(0.28, 0.45, 0.7),
                position=(x, 0.28, z),
                color=ursina.color.rgb(20, 20, 20)
            )
            ursina.Entity(
                parent=wheel,
                model="cube",
                scale=(1.1, 0.5, 0.5),
                position=(0, 0, 0),
                color=ursina.color.light_gray
            )

    ursina.Entity(
        parent=root,
        model="cube",
        scale=(1.5, 0.1, 0.4),
        position=(0, 1.15, -1.5),
        color=accent_color
    )

    if is_player:
        root.nitro_glow = ursina.Entity(
            parent=root,
            model="cube",
            scale=(0.4, 0.4, 0.8),
            position=(0, 0.4, -1.8),
            color=ursina.color.cyan,
            enabled=False
        )

    return root

# Player Entity
player = None

def create_player_car():
    global player
    if player is not None:
        ursina.destroy(player)
    
    selected_idx = save_data.get("selected_car", 0)
    car_info = CARS_DATA[selected_idx]
    
    player = build_car_entity(
        color=car_info["color"],
        accent_color=car_info["accent"],
        is_player=True
    )
    player.position = (0, 0, -8)

# Garage Shop Preview Car
shop_preview_car = None

def update_shop_preview():
    global shop_preview_car
    if shop_preview_car is not None:
        ursina.destroy(shop_preview_car)
    selected_idx = save_data.get("selected_car", 0)
    car_info = CARS_DATA[selected_idx]
    shop_preview_car = build_car_entity(
        color=car_info["color"],
        accent_color=car_info["accent"]
    )
    shop_preview_car.position = (0, 1.2, 0)
    shop_preview_car.scale = 1.3
    shop_preview_car.enabled = shop_open

# =========================================================
# DYNAMIC TRAFFIC & OBSTACLE SPAWNING
# =========================================================
traffic_list = []
obstacle_list = []
coin_list = []

TRAFFIC_COLORS = [
    ursina.color.azure,
    ursina.color.orange,
    ursina.color.yellow,
    ursina.color.lime,
    ursina.color.violet,
    ursina.color.white,
    ursina.color.pink
]

def rebuild_world_entities():
    for t in traffic_list:
        ursina.destroy(t)
    for o in obstacle_list:
        ursina.destroy(o)
    for c in coin_list:
        ursina.destroy(c)

    traffic_list.clear()
    obstacle_list.clear()
    coin_list.clear()

    num_traffic = min(12, 5 + current_level)
    num_obstacles = min(10, 3 + current_level)
    num_coins = 12

    for _ in range(num_traffic):
        t_car = build_car_entity(
            color=random.choice(TRAFFIC_COLORS),
            accent_color=ursina.color.dark_gray
        )
        t_car.position = (
            random.choice(LANES),
            0,
            random.randint(40, 180)
        )
        traffic_list.append(t_car)

    for _ in range(num_obstacles):
        obs = ursina.Entity(
            model="cube",
            scale=(1.8, 1.1, 0.9),
            position=(
                random.choice(LANES),
                0.6,
                random.randint(50, 180)
            ),
            color=ursina.color.orange
        )
        ursina.Entity(
            parent=obs,
            model="cube",
            scale=(1.02, 0.25, 1.02),
            position=(0, 0.1, 0),
            color=ursina.color.yellow
        )
        ursina.Entity(
            parent=obs,
            model="cube",
            scale=(0.3, 0.4, 0.3),
            position=(0, 0.7, 0),
            color=ursina.color.red
        )
        obstacle_list.append(obs)

    for _ in range(num_coins):
        coin = ursina.Entity(
            model="sphere",
            scale=(0.7, 0.7, 0.2),
            position=(
                random.choice(LANES),
                1.1,
                random.randint(30, 150)
            ),
            color=ursina.color.gold
        )
        ursina.Entity(
            parent=coin,
            model="cube",
            scale=(0.4, 0.4, 1.1),
            color=ursina.color.yellow
        )
        coin_list.append(coin)

rebuild_world_entities()
create_player_car()

# =========================================================
# UI & HUD ELEMENTS
# =========================================================
# Main Menu Entity
menu_ui = ursina.Entity(parent=ursina.camera.ui)

menu_panel = ursina.Entity(
    parent=menu_ui,
    model="quad",
    scale=(0.7, 0.80),
    color=ursina.color.rgba(15, 20, 35, 0.90)
)

menu_title = ursina.Text(
    parent=menu_ui,
    text="STREET RUSH 3D",
    origin=(0, 0),
    y=0.30,
    scale=2.2,
    color=ursina.color.yellow
)

menu_sub = ursina.Text(
    parent=menu_ui,
    text="Explore Desert, Ice, Space & Volcano Themes",
    origin=(0, 0),
    y=0.22,
    scale=1.1,
    color=ursina.color.white
)

menu_info = ursina.Text(
    parent=menu_ui,
    text="Highest Level: 1  |  Coins: 0  |  Best Score: 0",
    origin=(0, 0),
    y=0.12,
    scale=1.3,
    color=ursina.color.cyan
)

start_button = ursina.Button(
    parent=menu_ui,
    text="START RACE",
    color=ursina.color.azure,
    scale=(0.32, 0.08),
    y=-0.03
)

shop_button = ursina.Button(
    parent=menu_ui,
    text="GARAGE / SHOP (S)",
    color=ursina.color.orange,
    scale=(0.32, 0.08),
    y=-0.14
)

quit_button = ursina.Button(
    parent=menu_ui,
    text="QUIT GAME",
    color=ursina.color.red,
    scale=(0.32, 0.08),
    y=-0.25
)

# Shop UI
shop_ui = ursina.Entity(parent=ursina.camera.ui, enabled=False)

shop_panel = ursina.Entity(
    parent=shop_ui,
    model="quad",
    scale=(0.95, 0.85),
    color=ursina.color.rgba(15, 20, 30, 0.92)
)

shop_title = ursina.Text(
    parent=shop_ui,
    text="CAR GARAGE",
    origin=(0, 0),
    y=0.38,
    scale=2.2,
    color=ursina.color.gold
)

shop_coins_text = ursina.Text(
    parent=shop_ui,
    text="Coins: 0",
    origin=(0, 0),
    y=0.30,
    scale=1.4,
    color=ursina.color.yellow
)

shop_message = ursina.Text(
    parent=shop_ui,
    text="",
    origin=(0, 0),
    y=-0.28,
    scale=1.2,
    color=ursina.color.lime
)

back_button = ursina.Button(
    parent=shop_ui,
    text="BACK TO MENU",
    color=ursina.color.gray,
    scale=(0.25, 0.08),
    y=-0.38
)

shop_car_buttons = []

# Game HUD
hud_ui = ursina.Entity(parent=ursina.camera.ui, enabled=False)

hud_panel_left = ursina.Entity(
    parent=hud_ui,
    model="quad",
    scale=(0.46, 0.22),
    position=(-0.62, 0.37),
    color=ursina.color.rgba(0, 0, 0, 0.65)
)

hud_panel_right = ursina.Entity(
    parent=hud_ui,
    model="quad",
    scale=(0.46, 0.22),
    position=(0.62, 0.37),
    color=ursina.color.rgba(0, 0, 0, 0.65)
)

level_hud_text = ursina.Text(
    parent=hud_ui,
    text="LEVEL 1",
    position=(-0.83, 0.45),
    scale=1.4,
    color=ursina.color.gold
)

theme_hud_text = ursina.Text(
    parent=hud_ui,
    text="THEME: City Highway",
    position=(-0.83, 0.39),
    scale=1.1,
    color=ursina.color.cyan
)

score_text = ursina.Text(
    parent=hud_ui,
    text="Score: 0 / 15",
    position=(-0.83, 0.33),
    scale=1.2,
    color=ursina.color.white
)

coins_text = ursina.Text(
    parent=hud_ui,
    text="Coins: 0",
    position=(-0.83, 0.28),
    scale=1.2,
    color=ursina.color.yellow
)

speed_text = ursina.Text(
    parent=hud_ui,
    text="Speed: 15 km/h",
    position=(0.42, 0.45),
    scale=1.3,
    color=ursina.color.cyan
)

nitro_text = ursina.Text(
    parent=hud_ui,
    text="Nitro: 100%",
    position=(0.42, 0.39),
    scale=1.3,
    color=ursina.color.lime
)

diff_text = ursina.Text(
    parent=hud_ui,
    text="Difficulty: Normal",
    position=(0.42, 0.33),
    scale=1.2,
    color=ursina.color.orange
)

pause_btn_hud = ursina.Button(
    parent=hud_ui,
    text="PAUSE (P)",
    color=ursina.color.azure,
    scale=(0.14, 0.06),
    position=(0, 0.43)
)

# =========================================================
# PAUSE MENU UI
# =========================================================
pause_ui = ursina.Entity(parent=ursina.camera.ui, enabled=False)

pause_panel = ursina.Entity(
    parent=pause_ui,
    model="quad",
    scale=(0.65, 0.65),
    color=ursina.color.rgba(15, 20, 35, 0.92)
)

pause_title = ursina.Text(
    parent=pause_ui,
    text="GAME PAUSED",
    origin=(0, 0),
    y=0.22,
    scale=2.2,
    color=ursina.color.yellow
)

resume_button = ursina.Button(
    parent=pause_ui,
    text="RESUME / CONTINUE (P)",
    color=ursina.color.azure,
    scale=(0.36, 0.08),
    y=0.08
)

pause_shop_button = ursina.Button(
    parent=pause_ui,
    text="GARAGE / SHOP (S)",
    color=ursina.color.orange,
    scale=(0.36, 0.08),
    y=-0.03
)

pause_restart_button = ursina.Button(
    parent=pause_ui,
    text="RESTART RACE (R)",
    color=ursina.color.lime,
    scale=(0.36, 0.08),
    y=-0.14
)

pause_menu_button = ursina.Button(
    parent=pause_ui,
    text="MAIN MENU (M)",
    color=ursina.color.red,
    scale=(0.36, 0.08),
    y=-0.25
)

# =========================================================
# CRASH / GAME OVER UI (HIGH VISIBILITY)
# =========================================================
game_over_ui = ursina.Entity(parent=ursina.camera.ui, enabled=False)

game_over_panel = ursina.Entity(
    parent=game_over_ui,
    model="quad",
    scale=(0.7, 0.72),
    color=ursina.color.rgba(25, 20, 40, 0.95)
)

ursina.Entity(
    parent=game_over_ui,
    model="quad",
    scale=(0.71, 0.73),
    z=0.01,
    color=ursina.color.gold
)

game_over_title = ursina.Text(
    parent=game_over_ui,
    text="CRASHED! GAME OVER",
    origin=(0, 0),
    y=0.26,
    scale=2.2,
    color=ursina.color.red
)

game_over_info = ursina.Text(
    parent=game_over_ui,
    text="",
    origin=(0, 0),
    y=0.12,
    scale=1.3,
    color=ursina.color.yellow
)

restart_button = ursina.Button(
    parent=game_over_ui,
    text="RETRY RACE (R)",
    color=ursina.color.azure,
    scale=(0.34, 0.08),
    y=-0.04
)

game_over_shop_button = ursina.Button(
    parent=game_over_ui,
    text="GARAGE / SHOP (S)",
    color=ursina.color.orange,
    scale=(0.34, 0.08),
    y=-0.15
)

game_over_menu_button = ursina.Button(
    parent=game_over_ui,
    text="MAIN MENU (M)",
    color=ursina.color.red,
    scale=(0.34, 0.08),
    y=-0.26
)

# =========================================================
# LEVEL COMPLETE UI
# =========================================================
level_complete_ui = ursina.Entity(parent=ursina.camera.ui, enabled=False)

level_complete_panel = ursina.Entity(
    parent=level_complete_ui,
    model="quad",
    scale=(0.7, 0.72),
    color=ursina.color.rgba(10, 35, 20, 0.95)
)

ursina.Entity(
    parent=level_complete_ui,
    model="quad",
    scale=(0.71, 0.73),
    z=0.01,
    color=ursina.color.cyan
)

level_complete_title = ursina.Text(
    parent=level_complete_ui,
    text="LEVEL CLEARED!",
    origin=(0, 0),
    y=0.26,
    scale=2.4,
    color=ursina.color.gold
)

level_complete_info = ursina.Text(
    parent=level_complete_ui,
    text="",
    origin=(0, 0),
    y=0.10,
    scale=1.3,
    color=ursina.color.white
)

next_level_button = ursina.Button(
    parent=level_complete_ui,
    text="NEXT LEVEL (SPACE)",
    color=ursina.color.lime,
    scale=(0.36, 0.08),
    y=-0.06
)

level_shop_button = ursina.Button(
    parent=level_complete_ui,
    text="GARAGE / SHOP (S)",
    color=ursina.color.orange,
    scale=(0.36, 0.08),
    y=-0.17
)

level_menu_button = ursina.Button(
    parent=level_complete_ui,
    text="MAIN MENU (M)",
    color=ursina.color.red,
    scale=(0.36, 0.08),
    y=-0.27
)

# =========================================================
# SHOP LOGIC
# =========================================================
def buy_or_select_car(idx):
    global shop_message
    car = CARS_DATA[idx]
    
    if idx in save_data["unlocked_cars"]:
        save_data["selected_car"] = idx
        save_game()
        shop_message.text = f"{car['name']} Selected!"
        shop_message.color = ursina.color.lime
        update_shop()
        create_player_car()
        return

    if save_data["coins"] < car["price"]:
        shop_message.text = "Not enough coins!"
        shop_message.color = ursina.color.red
        return

    save_data["coins"] -= car["price"]
    save_data["unlocked_cars"].append(idx)
    save_data["selected_car"] = idx
    save_game()
    
    shop_message.text = f"Purchased {car['name']}!"
    shop_message.color = ursina.color.yellow
    update_shop()
    create_player_car()

def update_shop():
    shop_coins_text.text = f"Coins: {save_data['coins']}"
    selected_idx = save_data.get("selected_car", 0)
    
    for i, btn in enumerate(shop_car_buttons):
        car = CARS_DATA[i]
        if i in save_data["unlocked_cars"]:
            if i == selected_idx:
                btn.text = f"{car['name']}\n[ SELECTED ]"
                btn.color = ursina.color.green
            else:
                btn.text = f"{car['name']}\n[ SELECT ]"
                btn.color = ursina.color.azure
        else:
            btn.text = f"{car['name']}\n${car['price']} COINS"
            btn.color = ursina.color.orange

    update_shop_preview()

# Build Shop Buttons
for i, car in enumerate(CARS_DATA):
    btn = ursina.Button(
        parent=shop_ui,
        text=car["name"],
        color=car["color"],
        scale=(0.17, 0.10),
        x=-0.38 + (i * 0.19),
        y=-0.12
    )
    btn.on_click = lambda idx=i: buy_or_select_car(idx)
    shop_car_buttons.append(btn)

# =========================================================
# GAME STATE TRANSITIONS
# =========================================================
def update_menu_text():
    menu_info.text = (
        f"Highest Level: {save_data.get('max_level', 1)}  |  "
        f"Coins: {save_data['coins']}  |  "
        f"Best Score: {save_data['best_score']}"
    )

def start_game(start_lvl=1):
    global game_started, game_over, game_paused, level_complete, shop_open, current_level, level_target
    game_started = True
    game_over = False
    game_paused = False
    level_complete = False
    shop_open = False
    
    current_level = start_lvl
    level_target = get_level_target(current_level)

    # Apply environment theme for current level
    theme = get_level_theme(current_level)
    apply_level_theme(theme)

    menu_ui.enabled = False
    shop_ui.enabled = False
    game_over_ui.enabled = False
    pause_ui.enabled = False
    level_complete_ui.enabled = False
    hud_ui.enabled = True

    if shop_preview_car:
        shop_preview_car.enabled = False

    rebuild_world_entities()
    reset_objects()
    create_player_car()

def next_level():
    global current_level
    start_game(start_lvl=current_level + 1)

def toggle_pause():
    global game_paused
    if not game_started or game_over or level_complete or shop_open:
        return
    game_paused = not game_paused
    pause_ui.enabled = game_paused
    hud_ui.enabled = not game_paused

def open_shop():
    global shop_open
    shop_open = True
    menu_ui.enabled = False
    game_over_ui.enabled = False
    pause_ui.enabled = False
    level_complete_ui.enabled = False
    hud_ui.enabled = False
    shop_ui.enabled = True
    update_shop()

def close_shop():
    global shop_open
    shop_open = False
    shop_ui.enabled = False
    if shop_preview_car:
        shop_preview_car.enabled = False

    if game_started and not game_over:
        if level_complete:
            level_complete_ui.enabled = True
        elif game_paused:
            pause_ui.enabled = True
        else:
            hud_ui.enabled = True
    else:
        menu_ui.enabled = True
        update_menu_text()

def return_to_menu():
    global game_started, game_over, game_paused, level_complete, shop_open
    game_started = False
    game_over = False
    game_paused = False
    level_complete = False
    shop_open = False

    hud_ui.enabled = False
    game_over_ui.enabled = False
    pause_ui.enabled = False
    level_complete_ui.enabled = False
    shop_ui.enabled = False
    menu_ui.enabled = True
    
    update_menu_text()

def quit_game():
    raise SystemExit

# Button Connections
start_button.on_click = lambda: start_game(1)
shop_button.on_click = open_shop
quit_button.on_click = quit_game
back_button.on_click = close_shop

pause_btn_hud.on_click = toggle_pause
resume_button.on_click = toggle_pause
pause_shop_button.on_click = open_shop
pause_restart_button.on_click = lambda: start_game(current_level)
pause_menu_button.on_click = return_to_menu

restart_button.on_click = lambda: start_game(current_level)
game_over_shop_button.on_click = open_shop
game_over_menu_button.on_click = return_to_menu

next_level_button.on_click = next_level
level_shop_button.on_click = open_shop
level_menu_button.on_click = return_to_menu

update_menu_text()

# =========================================================
# RESET OBJECTS & LEVEL COMPLETION
# =========================================================
def reset_objects():
    global score, base_speed, current_speed, nitro, game_over, game_paused
    
    selected_idx = save_data.get("selected_car", 0)
    car_bonus = CARS_DATA[selected_idx]["speed_bonus"]
    
    level_speed_increase = (current_level - 1) * 2.5
    
    score = 0
    base_speed = 16 + car_bonus + level_speed_increase
    current_speed = base_speed
    nitro = 100
    game_over = False
    game_paused = False

    if player:
        player.position = (0, 0, -8)

    for car in traffic_list:
        car.position = (
            random.choice(LANES),
            0,
            random.randint(40, 180)
        )
        car.color = random.choice(TRAFFIC_COLORS)

    for obs in obstacle_list:
        obs.position = (
            random.choice(LANES),
            0.6,
            random.randint(50, 180)
        )

    for coin in coin_list:
        coin.position = (
            random.choice(LANES),
            1.1,
            random.randint(30, 150)
        )

def trigger_level_complete():
    global level_complete, game_paused
    if level_complete or game_over:
        return

    level_complete = True
    game_paused = False

    reward = 30 + current_level * 20
    save_data["coins"] += reward

    if current_level >= save_data.get("max_level", 1):
        save_data["max_level"] = current_level + 1

    if score > save_data["best_score"]:
        save_data["best_score"] = score

    save_game()

    hud_ui.enabled = False
    level_complete_ui.enabled = True

    next_theme = get_level_theme(current_level + 1)
    next_target = get_level_target(current_level + 1)

    level_complete_info.text = (
        f"Level {current_level} Successfully Cleared!\n\n"
        f"Reward Bonus: +{reward} COINS\n"
        f"Next Realm: {next_theme['name']} (Level {current_level + 1})\n"
        f"Target Score: {next_target}  |  +Traffic & Speed!"
    )

def end_game():
    global game_over, game_paused
    if game_over or level_complete:
        return

    game_over = True
    game_paused = False
    reward = score // 2
    save_data["coins"] += reward

    if score > save_data["best_score"]:
        save_data["best_score"] = score

    save_game()

    hud_ui.enabled = False
    game_over_ui.enabled = True
    theme = get_level_theme(current_level)
    game_over_info.text = (
        f"Level {current_level} ({theme['name']})\n"
        f"Score Reached: {score} / {level_target}\n"
        f"Coins Earned: +{reward}  |  Best: {save_data['best_score']}"
    )

# =========================================================
# UPDATE & MOVEMENT FUNCTIONS
# =========================================================
def update_road_and_scenery(dt):
    move_dist = current_speed * dt
    for line in road_lines:
        line.z -= move_dist
        if line.z < -30:
            line.z += 260

    for prop in scenery_props:
        prop.z -= move_dist
        if prop.z < -40:
            prop.z += 250

def move_player(dt):
    if not game_started or game_over or game_paused or level_complete or not player:
        return

    turn_speed = 9.0 * dt
    target_x = player.x

    if ursina.held_keys["a"] or ursina.held_keys["left arrow"]:
        target_x -= turn_speed
    if ursina.held_keys["d"] or ursina.held_keys["right arrow"]:
        target_x += turn_speed

    player.x = ursina.clamp(target_x, -5.3, 5.3)

def move_traffic(dt):
    global score
    traffic_speed = (current_speed - 4) + (current_level - 1) * 0.8
    for car in traffic_list:
        car.z -= traffic_speed * dt
        if car.z < -30:
            car.z = random.randint(90, 180)
            car.x = random.choice(LANES)
            car.color = random.choice(TRAFFIC_COLORS)
            score += 1

            if score >= level_target:
                trigger_level_complete()
                return

def move_obstacles(dt):
    for obs in obstacle_list:
        obs.z -= current_speed * dt
        if obs.z < -30:
            obs.z = random.randint(80, 170)
            obs.x = random.choice(LANES)

def move_coins(dt):
    for coin in coin_list:
        coin.z -= current_speed * dt
        coin.rotation_y += 200 * dt
        if coin.z < -30:
            coin.z = random.randint(50, 160)
            coin.x = random.choice(LANES)

def check_collisions():
    if not player or game_over or game_paused or level_complete:
        return

    px, py, pz = player.x, player.y, player.z

    for car in traffic_list:
        if abs(px - car.x) < 1.4 and abs(pz - car.z) < 2.3:
            end_game()
            return

    for obs in obstacle_list:
        if abs(px - obs.x) < 1.4 and abs(pz - obs.z) < 2.0:
            end_game()
            return

    for coin in coin_list:
        if abs(px - coin.x) < 1.3 and abs(pz - coin.z) < 1.8:
            save_data["coins"] += 1
            coin.z = random.randint(70, 170)
            coin.x = random.choice(LANES)
            save_game()

def update_camera(dt):
    if not player:
        return

    target_pos = player.position + ursina.Vec3(0, 5.5, -12)
    ursina.camera.position = ursina.lerp(
        ursina.camera.position,
        target_pos,
        dt * 6
    )
    ursina.camera.look_at(player.position + ursina.Vec3(0, 0, 12))

# =========================================================
# KEYBOARD INPUT HANDLER
# =========================================================
def input(key):
    global game_paused

    if level_complete and key in ("space", "enter"):
        next_level()
        return

    if key == "s":
        if shop_open:
            close_shop()
        else:
            open_shop()
        return

    if key in ("p", "escape"):
        if shop_open:
            close_shop()
        elif game_started and not game_over and not level_complete:
            toggle_pause()
        return

    if key == "r" and (game_over or game_paused or level_complete):
        start_game(current_level)
        return

    if key == "m" and (game_over or game_paused or level_complete):
        return_to_menu()
        return

# =========================================================
# MAIN ENGINE UPDATE LOOP
# =========================================================
def update():
    global current_speed, nitro, is_nitro_active

    if shop_open:
        if shop_preview_car:
            shop_preview_car.rotation_y += ursina.time.dt * 45
        return

    if not game_started or game_over or game_paused or level_complete:
        return

    dt = ursina.time.dt

    # Nitro Boost Logic
    if ursina.held_keys["space"] and nitro > 0:
        is_nitro_active = True
        current_speed = base_speed + 15
        nitro -= 35 * dt
        if hasattr(player, "nitro_glow") and player.nitro_glow:
            player.nitro_glow.enabled = True
    else:
        is_nitro_active = False
        current_speed = base_speed
        nitro = min(100, nitro + 12 * dt)
        if hasattr(player, "nitro_glow") and player.nitro_glow:
            player.nitro_glow.enabled = False

    move_player(dt)
    update_road_and_scenery(dt)
    move_traffic(dt)
    move_obstacles(dt)
    move_coins(dt)
    check_collisions()
    update_camera(dt)

    theme = get_level_theme(current_level)

    # Update HUD Displays
    level_hud_text.text = f"LEVEL {current_level}"
    theme_hud_text.text = f"THEME: {theme['name'].upper()}"
    score_text.text = f"Score: {score} / {level_target}"
    coins_text.text = f"Coins: {save_data['coins']}"
    speed_text.text = f"Speed: {int(current_speed * 5)} km/h"
    nitro_text.text = f"Nitro: {int(nitro)}%"
    
    if current_level == 1:
        diff_text.text = "Difficulty: Normal"
        diff_text.color = ursina.color.lime
    elif current_level == 2:
        diff_text.text = "Difficulty: Hard"
        diff_text.color = ursina.color.yellow
    elif current_level >= 3:
        diff_text.text = f"Difficulty: EXTREME (Lvl {current_level})"
        diff_text.color = ursina.color.red

    if nitro < 20:
        nitro_text.color = ursina.color.red
    elif is_nitro_active:
        nitro_text.color = ursina.color.cyan
    else:
        nitro_text.color = ursina.color.lime

# =========================================================
# RUN APPLICATION
# =========================================================
if __name__ == "__main__":
    app.run()