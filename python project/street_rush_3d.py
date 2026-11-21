from ursina import *
import random
import json
import os
import math
import time as pytime

# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------
def rgb255(r, g, b):     return color.rgb(r/255, g/255, b/255)
def rgba255(r, g, b, a): return color.rgba(r/255, g/255, b/255, a/255)

# =========================================================
# WINDOWi
# =========================================================
app = Ursina()
window.title              = "Street Rush 3D"
window.borderless         = False
window.color              = rgb255(70, 160, 240)
window.show_ursina_splash = False

# =========================================================
# SAVE SYSTEM
# =========================================================
SAVE_FILE    = "racing_save.json"
default_save = {"coins":0,"best_score":0,"selected_car":0,"unlocked_cars":[0],"max_level":1}
save_data    = default_save.copy()

def load_game():
    global save_data
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE) as f: old = json.load(f)
            save_data = default_save.copy(); save_data.update(old)
            if "unlocked_cars" not in save_data: save_data["unlocked_cars"] = [0]
            if save_data.get("selected_car",0) not in save_data["unlocked_cars"]: save_data["selected_car"]=0
            if "max_level" not in save_data: save_data["max_level"]=1
        except: save_data = default_save.copy()

def save_game():
    try:
        with open(SAVE_FILE,"w") as f: json.dump(save_data,f,indent=4)
    except Exception as e: print("Save error:",e)

load_game()

# =========================================================
# CARS
# =========================================================
CARS_DATA = [
    {"name":"Red Racer",   "color":rgb255(230, 30, 30),"price":  0,"speed_bonus":0,"accent":rgb255( 20, 20, 20)},
    {"name":"Blue Storm",  "color":rgb255(  0,140,255),"price": 50,"speed_bonus":2,"accent":rgb255(240,240,240)},
    {"name":"Golden GT",   "color":rgb255(255,190,  0),"price":100,"speed_bonus":4,"accent":rgb255(240,100,  0)},
    {"name":"Green Beast", "color":rgb255( 40,210, 60),"price":200,"speed_bonus":6,"accent":rgb255( 20, 20, 20)},
    {"name":"Purple X",    "color":rgb255(160, 40,230),"price":350,"speed_bonus":9,"accent":rgb255(  0,230,255)},
]

OPPONENT_DATA = [
    {"name":"Silver Bullet","color":rgb255(200,200,210),"accent":rgb255( 80, 80,100)},
    {"name":"Flame King",   "color":rgb255(255, 80,  0),"accent":rgb255(255,200,  0)},
    {"name":"Ice Wolf",     "color":rgb255(  0,200,255),"accent":rgb255(255,255,255)},
    {"name":"Neon Ghost",   "color":rgb255(180,  0,255),"accent":rgb255(  0,255,200)},
    {"name":"Lava Demon",   "color":rgb255(220, 20, 20),"accent":rgb255(255,120,  0)},
]

# =========================================================
# THEMES
# =========================================================
LEVEL_THEMES = [
    {"name":"City Highway",   "sky":rgb255(70,160,240), "ground":rgb255(34,139,34),  "road":rgb255(45,45,50),  "rail":rgb255(220,220,220),"stripe":rgb255(220,20,20), "line":rgb255(255,215,0),  "trunk":rgb255(120,70,30), "foliage":rgb255(40,180,60), "prop":"tree"},
    {"name":"Desert Canyon",  "sky":rgb255(245,130,45), "ground":rgb255(210,140,60), "road":rgb255(75,45,35),  "rail":rgb255(190,90,30),  "stripe":rgb255(255,180,0), "line":rgb255(255,255,255),"trunk":rgb255(40,160,60), "foliage":rgb255(255,210,40),"prop":"cactus"},
    {"name":"Arctic Glacier", "sky":rgb255(120,195,255),"ground":rgb255(200,230,255),"road":rgb255(35,65,105), "rail":rgb255(0,220,255),  "stripe":rgb255(0,140,255), "line":rgb255(0,230,255),  "trunk":rgb255(160,220,255),"foliage":rgb255(255,255,255),"prop":"ice_pine"},
    {"name":"Neon Cyber Space","sky":rgb255(20,8,45),   "ground":rgb255(55,15,90),   "road":rgb255(20,20,32),  "rail":rgb255(255,0,180),  "stripe":rgb255(0,240,255), "line":rgb255(255,0,220),  "trunk":rgb255(0,240,255), "foliage":rgb255(255,0,180), "prop":"neon_beacon"},
    {"name":"Volcanic Inferno","sky":rgb255(200,35,20), "ground":rgb255(50,18,18),   "road":rgb255(32,24,24),  "rail":rgb255(255,120,0),  "stripe":rgb255(255,200,0), "line":rgb255(240,30,30),  "trunk":rgb255(80,30,20),  "foliage":rgb255(255,110,0), "prop":"volcano_spire"},
]

def get_level_theme(lvl): return LEVEL_THEMES[(lvl-1) % len(LEVEL_THEMES)]

# =========================================================
# CAMERA VIEWS
# =========================================================
CAM_VIEWS = [
    ("Behind",   (0,  7,-18), 18),
    ("Hood",     (0,1.8, 1.5), 5),
    ("Top-Down", (0, 22, -4), 70),
    ("Side",     (16, 5,  0), 10),
]
cam_view_idx = 0

def apply_camera_view():
    _, pos, rx = CAM_VIEWS[cam_view_idx]
    camera.position   = pos
    camera.rotation_x = rx
    camera.rotation_y = -90 if cam_view_idx == 3 else 0
    hud_view_text.text = f"View: {CAM_VIEWS[cam_view_idx][0]}  (V)"

# =========================================================
# RACE / GAME STATE
# =========================================================
# Progress = how many units each racer has travelled forward.
# The entire road world scrolls BACKWARD past the stationary player model.
# Finish line is drawn at (player_progress - FINISH_DISTANCE) distance ahead visually.
FINISH_DISTANCE   = 500.0   # units of forward travel

player_progress   = 0.0
opponent_progress = 0.0
opponent_speed    = 0.0
opp_lane_timer    = 0.0     # fixed timer for opponent lane change (not random each frame)
opp_lane_target   = 0       # index into LANES
opp_lane_change_interval = 2.0  # seconds between lane changes

score           = 0
current_level   = 1
base_speed      = 15.0
current_speed   = 15.0
nitro           = 100.0
game_over       = False
game_started    = False
game_paused     = False
level_complete  = False
race_lost       = False
shop_open       = False
level_sel_open  = False
is_nitro_active = False
target_lane_idx = 2
LANES = [-4.5, -2.25, 0.0, 2.25, 4.5]

# =========================================================
# 3D WORLD  (static backdrop — scrolled in update)
# =========================================================
T0 = LEVEL_THEMES[0]

sky_ent      = Entity(model="sphere",scale=1000,double_sided=True,color=T0["sky"])
ground_ent   = Entity(model="cube",scale=(300,0.1,300),position=(0,-0.1,50),color=T0["ground"])
road_ent     = Entity(model="cube",scale=(14,0.2,300),position=(0,0.05,50),color=T0["road"])
left_rail    = Entity(model="cube",scale=(0.4,0.5,300),position=(-7.1,0.3,50),color=T0["rail"])
right_rail   = Entity(model="cube",scale=(0.4,0.5,300),position=(7.1,0.3,50),color=T0["rail"])
left_stripe  = Entity(model="cube",scale=(0.6,0.25,300),position=(-6.6,0.16,50),color=T0["stripe"])
right_stripe = Entity(model="cube",scale=(0.6,0.25,300),position=(6.6,0.16,50),color=T0["stripe"])

road_lines = []
for _z in range(-60,200,12):
    for _x in (-2.25,2.25):
        road_lines.append(Entity(model="cube",scale=(0.25,0.06,4.5),
                                position=(_x,0.19,_z),color=T0["line"]))

scenery_props = []

camera.position   = (0,7,-18)
camera.rotation_x = 18

AmbientLight(color=color.rgba(1,1,1,0.7))
DirectionalLight(color=color.white,direction=(1,-2,1))

# =========================================================
# FINISH LINE
# =========================================================
finish_line_root = None
FINISH_WORLD_Z   = 0.0   # updated every frame; player sits at z=0, finish ahead at this z

def build_finish_line():
    global finish_line_root
    if finish_line_root:
        destroy(finish_line_root)
    finish_line_root = Entity()

    cols = 9
    sq_h = 1.0
    for c in range(cols):
        for r in range(2):
            xp  = -6.75 + c*(14/cols) + (14/cols)/2
            yp  = 0.22 + r*sq_h
            clr = color.white if (c+r)%2==0 else color.black
            Entity(parent=finish_line_root, model="cube",
                scale=(14/cols-0.05, sq_h-0.05, 0.2),
                position=(xp,yp,0), color=clr)

    Entity(parent=finish_line_root,model="cube",
        scale=(0.4,5.0,0.4),position=(-7.3,2.5,0),color=rgb255(220,20,20))
    Entity(parent=finish_line_root,model="cube",
        scale=(0.4,5.0,0.4),position=( 7.3,2.5,0),color=rgb255(220,20,20))
    Entity(parent=finish_line_root,model="cube",
        scale=(15.5,0.5,0.4),position=(0,5.0,0),color=rgb255(220,20,20))
    Text(parent=finish_line_root, text="FINISH",
        origin=(0,0), position=(0,5.7,0), scale=8, color=color.yellow)

    # Start well ahead of the player (player sits at z=0, road scrolls backward)
    finish_line_root.z = FINISH_DISTANCE
    return finish_line_root

# =========================================================
# APPLY THEME
# =========================================================
def apply_level_theme(th):
    window.color=th["sky"]; sky_ent.color=th["sky"]; ground_ent.color=th["ground"]
    road_ent.color=th["road"]; left_rail.color=th["rail"]; right_rail.color=th["rail"]
    left_stripe.color=th["stripe"]; right_stripe.color=th["stripe"]
    for ln in road_lines: ln.color=th["line"]
    for p in scenery_props: destroy(p)
    scenery_props.clear()
    pt=th["prop"]
    for zp in range(-50,200,25):
        for side in (-11,11):
            if pt=="tree":
                trunk=Entity(model="cube",scale=(0.6,3.5,0.6),position=(side,1.75,zp),color=th["trunk"])
                Entity(parent=trunk,model="sphere",scale=(3.5,3.5,3.5),position=(0,0.8,0),color=th["foliage"])
            elif pt=="cactus":
                trunk=Entity(model="cube",scale=(0.7,4.0,0.7),position=(side,2.0,zp),color=th["trunk"])
                Entity(parent=trunk,model="cube",scale=(2.0,0.5,0.5),position=(0,0.2,0),color=th["trunk"])
                Entity(parent=trunk,model="cube",scale=(0.5,1.2,0.5),position=( 0.8,0.6,0),color=th["trunk"])
                Entity(parent=trunk,model="cube",scale=(0.5,1.2,0.5),position=(-0.8,0.6,0),color=th["trunk"])
                Entity(parent=trunk,model="sphere",scale=(1.2,1.2,1.2),position=(0,0.7,0),color=th["foliage"])
            elif pt=="ice_pine":
                trunk=Entity(model="cube",scale=(0.5,2.0,0.5),position=(side,1.0,zp),color=th["trunk"])
                Entity(parent=trunk,model="cube",scale=(3.0,1.2,3.0),position=(0,0.9,0),color=th["foliage"])
                Entity(parent=trunk,model="cube",scale=(2.2,1.2,2.2),position=(0,1.9,0),color=th["foliage"])
                Entity(parent=trunk,model="cube",scale=(1.2,1.0,1.2),position=(0,2.8,0),color=th["foliage"])
            elif pt=="neon_beacon":
                trunk=Entity(model="cube",scale=(0.4,5.0,0.4),position=(side,2.5,zp),color=th["trunk"])
                Entity(parent=trunk,model="cube",scale=(1.6,1.6,1.6),position=(0,0.6,0),color=th["foliage"])
            elif pt=="volcano_spire":
                trunk=Entity(model="cube",scale=(2.5,1.5,2.5),position=(side,0.75,zp),color=th["trunk"])
                Entity(parent=trunk,model="cube",scale=(0.7,1.5,0.7),position=(0,1.0,0),color=th["trunk"])
                Entity(parent=trunk,model="cube",scale=(0.4,1.0,0.4),position=(0,2.0,0),color=th["trunk"])
                Entity(parent=trunk,model="sphere",scale=(1.0,1.0,1.0),position=(0,2.8,0),color=th["foliage"])
            scenery_props.append(trunk)

apply_level_theme(T0)

# =========================================================
# CAR BUILDER
# =========================================================
def build_car(car_color, accent=None, is_player=False):
    if accent is None: accent=rgb255(20,20,20)
    root=Entity()
    Entity(parent=root,model="cube",scale=(1.6,0.55,3.2),position=(0,0.55,0),color=car_color)
    Entity(parent=root,model="cube",scale=(1.1,0.45,1.6),position=(0,0.95,-0.1),color=accent)
    Entity(parent=root,model="cube",scale=(1.0,0.35,0.4),position=(0,0.96,0.6),rotation_x=25,color=rgb255(120,200,245))
    Entity(parent=root,model="cube",scale=(1.0,0.35,0.4),position=(0,0.96,-0.75),rotation_x=-25,color=rgb255(80,140,180))
    for lx in (-0.55,0.55):
        Entity(parent=root,model="cube",scale=(0.3,0.15,0.12),position=(lx,0.56, 1.62),color=rgb255(255,255,200))
        Entity(parent=root,model="cube",scale=(0.3,0.15,0.12),position=(lx,0.56,-1.62),color=rgb255(220,20,20))
    for wx in (-0.85,0.85):
        for wz in (-0.9,0.9):
            wh=Entity(parent=root,model="cube",scale=(0.32,0.45,0.7),position=(wx,0.28,wz),color=rgb255(20,20,20))
            Entity(parent=wh,model="cube",scale=(1.1,0.5,0.5),color=rgb255(160,160,160))
    Entity(parent=root,model="cube",scale=(1.5,0.1,0.4),position=(0,1.15,-1.55),color=accent)
    if is_player:
        root.nitro_glow=Entity(parent=root,model="cube",scale=(0.5,0.4,1.0),
                            position=(0,0.4,-1.9),color=rgb255(0,230,255),enabled=False)
    else:
        root.nitro_glow=None
    return root

# =========================================================
# PLAYER & OPPONENT
# =========================================================
player   = None
opponent = None

def create_player_car():
    global player, target_lane_idx
    if player: destroy(player)
    ci=CARS_DATA[save_data.get("selected_car",0)]
    player=build_car(ci["color"],ci["accent"],is_player=True)
    target_lane_idx=2
    # Player stays fixed in world Z; the road scrolls backward
    player.position=(LANES[2], 0, 0)

def create_opponent_car(lvl):
    global opponent, opp_lane_target, opp_lane_timer
    if opponent: destroy(opponent)
    od=OPPONENT_DATA[(lvl-1)%len(OPPONENT_DATA)]
    opponent=build_car(od["color"],od["accent"],is_player=False)
    # Opponent starts in a different lane, slightly ahead visually
    opp_lane_target = random.choice([i for i in range(len(LANES)) if i!=2])
    opp_lane_timer  = 0.0
    opponent.position=(LANES[opp_lane_target], 0, 4)

    # Red banner label above opponent
    Entity(parent=opponent,model="cube",scale=(2.2,0.4,0.1),position=(0,2.2,0),color=rgb255(200,0,0))
    Text(parent=opponent,text=od["name"],origin=(0,0),position=(0,2.7,0),scale=6,color=color.white)

shop_preview_car=None

def update_shop_preview():
    global shop_preview_car
    if shop_preview_car: destroy(shop_preview_car)
    ci=CARS_DATA[save_data.get("selected_car",0)]
    shop_preview_car=build_car(ci["color"],ci["accent"])
    shop_preview_car.position=(0,1.2,0); shop_preview_car.scale=1.3
    shop_preview_car.enabled=shop_open

# =========================================================
# TRAFFIC / OBSTACLES / COINS
# =========================================================
traffic_list=[];  obstacle_list=[];  coin_list=[]

TRAFFIC_COLORS=[
    rgb255(0,140,255),rgb255(255,120,0),rgb255(255,210,0),
    rgb255(40,210,60),rgb255(160,40,230),rgb255(255,255,255),
    rgb255(255,50,150),rgb255(0,200,180),rgb255(255,80,80),
]

def rebuild_world_entities():
    for e in traffic_list+obstacle_list+coin_list: destroy(e)
    traffic_list.clear(); obstacle_list.clear(); coin_list.clear()

    for _ in range(min(10,4+current_level)):
        tc=build_car(random.choice(TRAFFIC_COLORS),rgb255(30,30,30))
        tc.position=(random.choice(LANES),0,random.randint(20,160))
        traffic_list.append(tc)

    for _ in range(min(8,2+current_level)):
        obs=Entity(model="cube",scale=(2.0,1.4,1.2),
                position=(random.choice(LANES),0.7,random.randint(40,160)),
                color=rgb255(255,100,0))
        Entity(parent=obs,model="cube",scale=(1.01,0.25,1.01),position=(0,0,0),color=rgb255(255,220,0))
        Entity(parent=obs,model="sphere",scale=(0.5,0.5,0.5),position=(0,0.8,0),color=rgb255(255,30,30))
        obstacle_list.append(obs)

    for _ in range(15):
        coin=Entity(model="sphere",scale=(0.8,0.8,0.8),
                    position=(random.choice(LANES),1.2,random.randint(15,140)),
                    color=rgb255(255,200,0))
        Entity(parent=coin,model="cube",scale=(1.4,0.15,1.4),position=(0,0,0),color=rgb255(255,240,80))
        coin_list.append(coin)

rebuild_world_entities()
create_player_car()

# =========================================================
# UI — MAIN MENU
# =========================================================
menu_ui=Entity(parent=camera.ui)
Entity(parent=menu_ui,model="quad",scale=(0.72,0.92),color=rgba255(10,15,30,215))
Text(parent=menu_ui,text="STREET RUSH 3D",origin=(0,0),y=0.38,scale=2.3,color=color.yellow)
Text(parent=menu_ui,text="City · Desert · Ice · Space · Volcano",origin=(0,0),y=0.29,scale=1.05,color=color.white)
menu_info=Text(parent=menu_ui,text="Highest Level: 1  |  Coins: 0  |  Best Score: 0",
            origin=(0,0),y=0.20,scale=1.2,color=color.cyan)
Text(parent=menu_ui,text="Beat the OPPONENT to the FINISH LINE!\nA/D=Lane   W/↑/Space=NITRO   V=View   P=Pause",
    origin=(0,0),y=0.10,scale=0.9,color=rgb255(180,180,180))
start_button  =Button(parent=menu_ui,text="START RACE (latest level)",color=rgb255(0,130,220),scale=(0.36,0.075),y= 0.00)
lvlsel_button =Button(parent=menu_ui,text="SELECT LEVEL",             color=rgb255(0,160,80), scale=(0.36,0.075),y=-0.10)
shop_button   =Button(parent=menu_ui,text="GARAGE / SHOP  (S)",       color=rgb255(210,100,0),scale=(0.36,0.075),y=-0.20)
quit_button   =Button(parent=menu_ui,text="QUIT GAME",                color=rgb255(180,20,20),scale=(0.36,0.075),y=-0.30)

# =========================================================
# UI — LEVEL SELECT
# =========================================================
lvlsel_ui=Entity(parent=camera.ui,enabled=False)
Entity(parent=lvlsel_ui,model="quad",scale=(0.85,0.82),color=rgba255(8,15,28,225))
Text(parent=lvlsel_ui,text="SELECT LEVEL",origin=(0,0),y=0.36,scale=2.1,color=color.gold)
Text(parent=lvlsel_ui,text="Choose any level you have reached",origin=(0,0),y=0.27,scale=1.0,color=rgb255(180,180,180))
lvlsel_back_btn=Button(parent=lvlsel_ui,text="BACK",color=color.gray,scale=(0.20,0.07),y=-0.38)
lvlsel_buttons=[]

def refresh_level_select():
    for b in lvlsel_buttons: destroy(b)
    lvlsel_buttons.clear()
    max_lvl=save_data.get("max_level",1)
    THEME_BTNCOLS=[rgb255(0,110,200),rgb255(190,100,0),rgb255(0,160,220),rgb255(100,0,180),rgb255(180,40,0)]
    for i in range(1,max_lvl+1):
        col=(i-1)%5; row=(i-1)//5
        bx=-0.36+col*0.18; by=0.14-row*0.14
        th=get_level_theme(i); od=OPPONENT_DATA[(i-1)%len(OPPONENT_DATA)]
        label=f"Lv {i}\n{th['name']}\nvs {od['name']}"
        btn=Button(parent=lvlsel_ui,text=label,color=THEME_BTNCOLS[(i-1)%5],scale=(0.16,0.12),position=(bx,by))
        def _h(lvl=i): return lambda: start_new_race(lvl)
        btn.on_click=_h(i); lvlsel_buttons.append(btn)

def open_level_select():
    global level_sel_open
    level_sel_open=True; menu_ui.enabled=False; lvlsel_ui.enabled=True; refresh_level_select()

# =========================================================
# UI — SHOP
# =========================================================
shop_ui=Entity(parent=camera.ui,enabled=False)
Entity(parent=shop_ui,model="quad",scale=(0.96,0.86),color=rgba255(10,15,28,220))
Text(parent=shop_ui,text="CAR GARAGE",origin=(0,0),y=0.39,scale=2.2,color=color.gold)
shop_coins_text=Text(parent=shop_ui,text="Coins: 0",origin=(0,0),y=0.30,scale=1.4,color=color.yellow)
shop_message=Text(parent=shop_ui,text="",origin=(0,0),y=-0.29,scale=1.2,color=color.lime)
back_button=Button(parent=shop_ui,text="BACK TO MENU",color=color.gray,scale=(0.25,0.08),y=-0.39)
shop_car_buttons=[]

def refresh_shop_ui():
    shop_coins_text.text=f"Coins: {save_data.get('coins',0)}"
    for b in shop_car_buttons: destroy(b)
    shop_car_buttons.clear()
    unlocked=save_data.get("unlocked_cars",[0]); selected=save_data.get("selected_car",0)
    for i,cd in enumerate(CARS_DATA):
        bx=-0.36+i*0.18
        if i==selected:     bc,bt=color.green,       f"{cd['name']}\n[EQUIPPED]"
        elif i in unlocked: bc,bt=rgb255(0,120,210),  f"{cd['name']}\n[SELECT]"
        else:               bc,bt=rgb255(160,30,30),  f"{cd['name']}\n${cd['price']}"
        btn=Button(parent=shop_ui,text=bt,color=bc,scale=(0.16,0.13),position=(bx,-0.13))
        def _h(idx=i): return lambda: on_select_car(idx)
        btn.on_click=_h(i); shop_car_buttons.append(btn)
    update_shop_preview()

def on_select_car(car_idx):
    unlocked=save_data.get("unlocked_cars",[0]); ci=CARS_DATA[car_idx]
    if car_idx in unlocked:
        save_data["selected_car"]=car_idx; save_game()
        shop_message.text=f"Selected {ci['name']}!"; shop_message.color=color.lime
    else:
        coins,cost=save_data.get("coins",0),ci["price"]
        if coins>=cost:
            save_data["coins"]=coins-cost; unlocked.append(car_idx)
            save_data["unlocked_cars"]=unlocked; save_data["selected_car"]=car_idx; save_game()
            shop_message.text=f"Unlocked {ci['name']}!"; shop_message.color=color.lime
        else:
            shop_message.text=f"Need {cost-coins} more coins!"; shop_message.color=color.red
    create_player_car(); refresh_shop_ui()

# =========================================================
# UI — HUD
# =========================================================
hud_ui=Entity(parent=camera.ui,enabled=False)

Entity(parent=hud_ui,model="quad",scale=(0.33,0.23),position=(-0.67,0.38),color=rgba255(15,15,20,210))
hud_level_text=Text(parent=hud_ui,text="LEVEL 1",     position=(-0.82,0.46),scale=1.4, color=color.gold)
hud_theme_text=Text(parent=hud_ui,text="THEME: CITY", position=(-0.82,0.41),scale=1.05,color=color.cyan)
hud_coins_text=Text(parent=hud_ui,text="Coins: 0",    position=(-0.82,0.36),scale=1.2, color=color.yellow)
hud_diff_text =Text(parent=hud_ui,text="Normal",      position=(-0.82,0.31),scale=1.0, color=rgb255(180,180,180))

Entity(parent=hud_ui,model="quad",scale=(0.33,0.23),position=(0.67,0.38),color=rgba255(15,15,20,210))
hud_speed_text=Text(parent=hud_ui,text="Speed: 0 km/h",position=(0.53,0.46),scale=1.2,color=color.cyan)
hud_nitro_text=Text(parent=hud_ui,text="Nitro: 100%",  position=(0.53,0.41),scale=1.2,color=color.lime)
hud_dist_text =Text(parent=hud_ui,text="0 / 500m",     position=(0.53,0.36),scale=1.1,color=color.white)

# ── Race progress bar ─────────────────────────────────────────────
Entity(parent=hud_ui,model="quad",scale=(0.62,0.075),position=(0,-0.40),color=rgba255(10,10,10,210))
Entity(parent=hud_ui,model="quad",scale=(0.58,0.038),position=(0,-0.40),color=rgb255(50,50,50))

# Start / Finish labels
Text(parent=hud_ui,text="START",origin=(0,0),position=(-0.32,-0.43),scale=0.75,color=rgb255(180,180,180))
Text(parent=hud_ui,text="FINISH",origin=(0,0),position=( 0.32,-0.43),scale=0.75,color=rgb255(255,220,0))

# Moving markers
hud_player_marker  =Entity(parent=hud_ui,model="quad",scale=(0.022,0.055),
                            position=(-0.29,-0.40),color=color.lime)
hud_opponent_marker=Entity(parent=hud_ui,model="quad",scale=(0.022,0.055),
                            position=(-0.29,-0.40),color=color.red)

hud_race_lead_text=Text(parent=hud_ui,text="",origin=(0,0),
                        position=(0,-0.355),scale=1.15,color=color.yellow)
hud_opp_name=Text(parent=hud_ui,text="vs ???",origin=(0,0),
                position=(0,0.44),scale=1.3,color=color.red)
hud_view_text=Text(parent=hud_ui,text="View: Behind  (V)",origin=(0,0),
                position=(0,-0.47),scale=0.85,color=rgb255(180,180,180))

pause_hud_btn=Button(parent=hud_ui,text="PAUSE (P)",color=rgb255(0,110,190),
                    scale=(0.13,0.055),position=(0.73,0.44))

# =========================================================
# UI — PAUSE
# =========================================================
pause_ui=Entity(parent=camera.ui,enabled=False)
Entity(parent=pause_ui,model="quad",scale=(0.6,0.72),color=rgba255(10,15,28,235))
Text(parent=pause_ui,text="GAME PAUSED",origin=(0,0),y=0.27,scale=2.2,color=color.cyan)
btn_resume    =Button(parent=pause_ui,text="RESUME  (P)",        color=color.green,      scale=(0.36,0.08),y= 0.12)
btn_restart   =Button(parent=pause_ui,text="RESTART LEVEL  (R)", color=rgb255(0,130,210),scale=(0.36,0.08),y= 0.02)
btn_pause_shop=Button(parent=pause_ui,text="GARAGE / SHOP  (S)", color=rgb255(200,100,0),scale=(0.36,0.08),y=-0.08)
btn_main_menu =Button(parent=pause_ui,text="MAIN MENU  (M)",     color=color.gray,       scale=(0.36,0.08),y=-0.18)

# =========================================================
# UI — CRASH
# =========================================================
crash_ui=Entity(parent=camera.ui,enabled=False)
Entity(parent=crash_ui,model="quad",scale=(0.65,0.65),color=rgba255(25,5,5,235))
Text(parent=crash_ui,text="CAR CRASHED!",origin=(0,0),y=0.23,scale=2.3,color=color.red)
crash_info     =Text(parent=crash_ui,text="",origin=(0,0),y=0.11,scale=1.3,color=color.white)
btn_crash_retry=Button(parent=crash_ui,text="RETRY  (R)",         color=color.green,      scale=(0.35,0.08),y=-0.04)
btn_crash_shop =Button(parent=crash_ui,text="GARAGE / SHOP  (S)", color=rgb255(200,100,0),scale=(0.35,0.08),y=-0.14)
btn_crash_menu =Button(parent=crash_ui,text="MAIN MENU  (M)",     color=color.gray,       scale=(0.35,0.08),y=-0.24)

# =========================================================
# UI — RACE LOST
# =========================================================
lost_ui=Entity(parent=camera.ui,enabled=False)
Entity(parent=lost_ui,model="quad",scale=(0.65,0.65),color=rgba255(25,5,5,235))
Text(parent=lost_ui,text="RACE LOST!",origin=(0,0),y=0.25,scale=2.3,color=rgb255(255,80,0))
lost_info     =Text(parent=lost_ui,text="",origin=(0,0),y=0.12,scale=1.15,color=color.white)
btn_lost_retry=Button(parent=lost_ui,text="RETRY  (R)",         color=color.green,      scale=(0.35,0.08),y=-0.04)
btn_lost_shop =Button(parent=lost_ui,text="GARAGE / SHOP  (S)", color=rgb255(200,100,0),scale=(0.35,0.08),y=-0.14)
btn_lost_menu =Button(parent=lost_ui,text="MAIN MENU  (M)",     color=color.gray,       scale=(0.35,0.08),y=-0.24)

# =========================================================
# UI — LEVEL WIN
# =========================================================
level_win_ui=Entity(parent=camera.ui,enabled=False)
Entity(parent=level_win_ui,model="quad",scale=(0.70,0.70),color=rgba255(5,28,15,235))
Text(parent=level_win_ui,text="YOU WIN!",origin=(0,0),y=0.27,scale=2.5,color=color.gold)
level_win_info=Text(parent=level_win_ui,text="",origin=(0,0),y=0.13,scale=1.2,color=color.lime)
btn_next_level=Button(parent=level_win_ui,text="NEXT LEVEL",        color=color.green,      scale=(0.36,0.08),y=-0.02)
btn_win_shop  =Button(parent=level_win_ui,text="GARAGE / SHOP  (S)",color=rgb255(200,100,0),scale=(0.36,0.08),y=-0.12)
btn_win_menu  =Button(parent=level_win_ui,text="MAIN MENU  (M)",    color=color.gray,       scale=(0.36,0.08),y=-0.22)

# =========================================================
# STATE TRANSITIONS
# =========================================================
def show_main_menu():
    global game_started,game_paused,game_over,level_complete,race_lost,shop_open,level_sel_open
    game_started=game_paused=game_over=level_complete=race_lost=shop_open=level_sel_open=False
    menu_ui.enabled=True
    for ui in (shop_ui,hud_ui,pause_ui,crash_ui,level_win_ui,lost_ui,lvlsel_ui): ui.enabled=False
    ml=save_data.get("max_level",1); tc=save_data.get("coins",0); bs=save_data.get("best_score",0)
    menu_info.text=f"Highest Level: {ml}  |  Coins: {tc}  |  Best Score: {bs}"
    if shop_preview_car: shop_preview_car.enabled=False

def open_shop_menu():
    global shop_open
    shop_open=True
    for ui in (menu_ui,pause_ui,crash_ui,level_win_ui,lost_ui,hud_ui,lvlsel_ui): ui.enabled=False
    shop_ui.enabled=True; refresh_shop_ui()

def start_new_race(lvl=1):
    global score,current_level,base_speed,current_speed,nitro
    global game_over,game_started,game_paused,level_complete,race_lost
    global shop_open,level_sel_open,target_lane_idx,cam_view_idx
    global player_progress,opponent_progress,opponent_speed
    global opp_lane_timer,opp_lane_target,opp_lane_change_interval

    current_level=lvl; score=0; nitro=100.0; target_lane_idx=2; cam_view_idx=0
    player_progress=0.0; opponent_progress=0.0
    opp_lane_timer=0.0; opp_lane_change_interval=2.0
    opp_lane_target=random.choice([i for i in range(len(LANES)) if i!=2])

    si=save_data.get("selected_car",0)
    base_speed   = 15.0 + (lvl-1)*2.0 + CARS_DATA[si]["speed_bonus"]
    current_speed= base_speed

    # Opponent speed: starts clearly slower, converges toward player speed by level 5+
    opponent_speed = base_speed * (0.80 + min(lvl-1, 8) * 0.025)

    game_started=True; game_paused=game_over=level_complete=race_lost=shop_open=level_sel_open=False

    th=get_level_theme(lvl); apply_level_theme(th)
    rebuild_world_entities(); create_player_car(); create_opponent_car(lvl); build_finish_line()
    apply_camera_view()

    for ui in (menu_ui,shop_ui,pause_ui,crash_ui,level_win_ui,lost_ui,lvlsel_ui): ui.enabled=False
    hud_ui.enabled=True
    if shop_preview_car: shop_preview_car.enabled=False

    od=OPPONENT_DATA[(lvl-1)%len(OPPONENT_DATA)]
    diff="Normal" if lvl<=2 else ("Hard" if lvl<=4 else "Extreme")
    hud_level_text.text=f"LEVEL {lvl}"
    hud_theme_text.text=f"THEME: {th['name'].upper()}"
    hud_coins_text.text=f"Coins: {save_data.get('coins',0)}"
    hud_diff_text.text =f"Difficulty: {diff}"
    hud_opp_name.text  =f"vs {od['name']}"
    hud_race_lead_text.text=""

def toggle_pause():
    global game_paused
    if not game_started or game_over or level_complete or race_lost: return
    game_paused=not game_paused; pause_ui.enabled=game_paused; hud_ui.enabled=not game_paused

def trigger_crash():
    global game_over
    game_over=True
    crash_info.text=f"Score: {score}\nCoins: {save_data.get('coins',0)}"
    crash_ui.enabled=True

def trigger_race_lost():
    global race_lost
    race_lost=True
    od=OPPONENT_DATA[(current_level-1)%len(OPPONENT_DATA)]
    lost_info.text=(f"{od['name']} reached the finish first!\n"
                    f"Your progress: {int(player_progress)}m / {int(FINISH_DISTANCE)}m\n"
                    f"Tip: Use NITRO (W/↑/Space) to speed ahead!")
    lost_ui.enabled=True

def trigger_level_complete():
    global level_complete
    level_complete=True
    coins_earned=score+5
    save_data["coins"]=save_data.get("coins",0)+coins_earned
    nl=current_level+1
    if nl>save_data.get("max_level",1): save_data["max_level"]=nl
    if score>save_data.get("best_score",0): save_data["best_score"]=score
    save_game()
    od=OPPONENT_DATA[(current_level-1)%len(OPPONENT_DATA)]
    level_win_info.text=(f"You beat {od['name']}!\n"
                         f"Coins earned: +{coins_earned}   Total: {save_data['coins']}\n"
                         f"Next: {get_level_theme(nl)['name']}")
    level_win_ui.enabled=True

# =========================================================
# BUTTON BINDINGS
# =========================================================
start_button.on_click   =lambda: start_new_race(save_data.get("max_level",1))
lvlsel_button.on_click  =open_level_select
shop_button.on_click    =open_shop_menu
quit_button.on_click    =application.quit
back_button.on_click    =show_main_menu
lvlsel_back_btn.on_click=show_main_menu

pause_hud_btn.on_click =toggle_pause
btn_resume.on_click    =toggle_pause
btn_restart.on_click   =lambda: start_new_race(current_level)
btn_pause_shop.on_click=open_shop_menu
btn_main_menu.on_click =show_main_menu

btn_crash_retry.on_click=lambda: start_new_race(current_level)
btn_crash_shop.on_click =open_shop_menu
btn_crash_menu.on_click =show_main_menu

btn_lost_retry.on_click =lambda: start_new_race(current_level)
btn_lost_shop.on_click  =open_shop_menu
btn_lost_menu.on_click  =show_main_menu

btn_next_level.on_click =lambda: start_new_race(current_level+1)
btn_win_shop.on_click   =open_shop_menu
btn_win_menu.on_click   =show_main_menu

# =========================================================
# INPUT
# =========================================================
def input(key):
    global target_lane_idx, cam_view_idx

    if key in ("p","P"): toggle_pause()
    if key in ("s","S"):
        if not game_started or game_paused or game_over or level_complete or race_lost:
            open_shop_menu()
    if key in ("r","R"):
        if game_over or game_paused or race_lost: start_new_race(current_level)
    if key in ("m","M"):
        if game_over or game_paused or level_complete or race_lost: show_main_menu()
    if key in ("v","V"):
        if game_started and not game_paused and not game_over and not level_complete and not race_lost:
            cam_view_idx=(cam_view_idx+1)%len(CAM_VIEWS); apply_camera_view()
    if game_started and not game_paused and not game_over and not level_complete and not race_lost and player:
        if key in ("a","left arrow"):
            if target_lane_idx>0: target_lane_idx-=1
        elif key in ("d","right arrow"):
            if target_lane_idx<len(LANES)-1: target_lane_idx+=1

# =========================================================
# UPDATE LOOP
# =========================================================
def update():
    global score,nitro,current_speed,is_nitro_active
    global player_progress,opponent_progress
    global opp_lane_timer,opp_lane_target,opp_lane_change_interval

    if shop_open and shop_preview_car and shop_preview_car.enabled:
        shop_preview_car.rotation_y+=time.dt*50; return

    if not game_started or game_paused or game_over or level_complete or race_lost or not player:
        return

    dt = time.dt

    # ── Nitro ──────────────────────────────────────────────────────
    nitro_on = held_keys["w"] or held_keys["up arrow"] or held_keys["space"]
    if nitro_on and nitro > 0:
        is_nitro_active=True
        current_speed  = base_speed * 1.65
        nitro          = max(0.0, nitro - dt*28)
        if player.nitro_glow: player.nitro_glow.enabled=True
    else:
        is_nitro_active=False
        current_speed  = base_speed
        nitro          = min(100.0, nitro + dt*12)
        if player.nitro_glow: player.nitro_glow.enabled=False

    # ── Player progress counter ────────────────────────────────────
    player_progress += current_speed * dt

    # ── Opponent progress + lane AI ───────────────────────────────
    if opponent:
        # Tiny sine speed wobble using pytime (NOT Ursina's time module)
        t_now = pytime.time()
        opp_wobble = opponent_speed * (1.0 + 0.06 * math.sin(t_now * 1.8))
        opponent_progress += opp_wobble * dt

        # Lane change on fixed interval (not random every frame)
        opp_lane_timer += dt
        if opp_lane_timer >= opp_lane_change_interval:
            opp_lane_timer = 0.0
            opp_lane_change_interval = 1.5 + random.random() * 2.0   # 1.5–3.5 s
            choices = [i for i in range(len(LANES)) if i != opp_lane_target]
            opp_lane_target = random.choice(choices)

        # Smooth X movement
        opponent.x = lerp(opponent.x, LANES[opp_lane_target], dt*5)

        # Z position = relative distance ahead/behind player on screen
        # Positive z_diff means opponent is ahead of player
        z_diff = (opponent_progress - player_progress)
        # Clamp display so opponent stays visible (never more than 60 units away)
        z_diff_clamped = max(-40.0, min(60.0, z_diff))
        opponent.z = z_diff_clamped

    # ── Player X lerp (player stays at z=0, world scrolls) ────────
    player.x = lerp(player.x, LANES[target_lane_idx], dt*12)

    # ── Camera follow ──────────────────────────────────────────────
    _, cam_off, cam_rx = CAM_VIEWS[cam_view_idx]
    if cam_view_idx == 1:        # Hood
        camera.position   = Vec3(player.x + cam_off[0], cam_off[1], cam_off[2])
        camera.rotation_x = cam_rx; camera.rotation_y = 0
    elif cam_view_idx == 2:      # Top-down
        camera.position   = Vec3(player.x, cam_off[1], cam_off[2])
        camera.rotation_x = cam_rx
    elif cam_view_idx == 3:      # Side
        camera.position   = Vec3(cam_off[0], cam_off[1], 0)
        camera.rotation_x = cam_rx; camera.rotation_y = -90
    else:                        # Behind
        camera.position   = Vec3(player.x*0.3, cam_off[1], cam_off[2])
        camera.rotation_x = cam_rx

    # ── Finish line: scrolls toward player as progress increases ───
    if finish_line_root:
        finish_line_root.z = FINISH_DISTANCE - player_progress

    # ── Road markings scroll ───────────────────────────────────────
    for ln in road_lines:
        ln.z -= current_speed * dt
        if ln.z < -20: ln.z += 240

    # ── Scenery scroll ─────────────────────────────────────────────
    for p in scenery_props:
        p.z -= current_speed * dt
        if p.z < -20: p.z += 250

    # ── Traffic ────────────────────────────────────────────────────
    for tc in traffic_list:
        tc.z -= current_speed * 0.38 * dt
        if tc.z < -15:
            tc.z = random.randint(80,160); tc.x = random.choice(LANES)
            score += 1
            if score > save_data.get("best_score",0):
                save_data["best_score"]=score; save_game()
        if abs(player.x - tc.x) < 1.3 and abs(player.z - tc.z) < 2.6:
            trigger_crash(); return

    # ── Obstacles ──────────────────────────────────────────────────
    for obs in obstacle_list:
        obs.z -= current_speed * dt
        if obs.z < -15:
            obs.z = random.randint(80,160); obs.x = random.choice(LANES)
        if abs(player.x - obs.x) < 1.5 and abs(player.z - obs.z) < 1.8:
            trigger_crash(); return

    # ── Coins ──────────────────────────────────────────────────────
    for coin in coin_list:
        coin.rotation_y += dt * 200
        coin.z -= current_speed * dt
        if coin.z < -15:
            coin.z = random.randint(80,160); coin.x = random.choice(LANES)
        if abs(player.x - coin.x) < 1.3 and abs(player.z - coin.z) < 1.8:
            save_data["coins"] = save_data.get("coins",0) + 1; save_game()
            coin.z = random.randint(100,180); coin.x = random.choice(LANES)

    # ── Race finish checks ─────────────────────────────────────────
    if opponent_progress >= FINISH_DISTANCE:
        trigger_race_lost(); return
    if player_progress >= FINISH_DISTANCE:
        trigger_level_complete(); return

    # ── HUD ────────────────────────────────────────────────────────
    hud_speed_text.text = f"Speed: {int(current_speed*6)} km/h"
    hud_nitro_text.text = f"Nitro: {int(nitro)}%"
    hud_nitro_text.color= rgb255(0,220,255) if is_nitro_active else color.lime
    hud_coins_text.text = f"Coins: {save_data.get('coins',0)}"
    hud_dist_text.text  = f"{int(player_progress)} / {int(FINISH_DISTANCE)}m"

    # Race progress bar: markers slide from x=-0.29 (start) to x=+0.29 (finish)
    bar_half = 0.29
    px = -bar_half + (player_progress   / FINISH_DISTANCE) * bar_half * 2
    ox = -bar_half + (opponent_progress / FINISH_DISTANCE) * bar_half * 2
    px = max(-bar_half, min(bar_half, px))
    ox = max(-bar_half, min(bar_half, ox))
    hud_player_marker.x   = px
    hud_opponent_marker.x = ox

    diff_m = player_progress - opponent_progress
    if diff_m > 5:
        hud_race_lead_text.text  = f"AHEAD  +{int(diff_m)}m"
        hud_race_lead_text.color = color.lime
    elif diff_m < -5:
        hud_race_lead_text.text  = f"BEHIND  {int(-diff_m)}m"
        hud_race_lead_text.color = color.red
    else:
        hud_race_lead_text.text  = "NECK & NECK!"
        hud_race_lead_text.color = color.yellow

# =========================================================
# LAUNCH
# =========================================================
show_main_menu()

if __name__ == "__main__":
    app.run()
