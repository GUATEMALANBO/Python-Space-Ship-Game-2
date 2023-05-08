import pygame as py
py.font.init()
py.mixer.init()
from pygame import mixer
WIDTH, HEIGHT = 700, 800

WIN = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption("GALACTIC GUN")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (75, 0, 130)
RED = (255, 0 , 0)
BLUE = (0, 0, 255)

BORDER = py.Rect(0, HEIGHT // 2, WIDTH, 10)

BULLET_HIT_SOUND = py.mixer.Sound('Python\Assets\Metal hit Sound Effect.mp3')
BULLET_FIRE_SOUND = py.mixer.Sound('Python\Assets\Blaster shooting.mp3')
HEALTH_FONT = py.font.SysFont('consolas', 30)
WIN_SOUND = py.mixer.Sound('Python\Assets\8 bit victory.mp3')
CONTROL = py.font.SysFont('consolas', 30)

FPS = 60
VEL = 5
VEL2 = 5
BULLET_VEL = 7
MAX_BULLET = 4
PLAYER_WIDTH, PLAYER_HEIGHT = 80, 60

ability_speed_boost = 2
ability_active = False
ability_speed_boost2 = 2
ability_active2 = False

YELLOW_HIT = py.USEREVENT + 1
RED_HIT = py.USEREVENT + 2

RIFLE_IMAGE = py.image.load('Python\Assets\Space ship2-export.png')
RIFLE = py.transform.scale(RIFLE_IMAGE, (PLAYER_WIDTH, PLAYER_HEIGHT))

CHEST_IMAGE = py.image.load('Python\Assets\Space ship1-export.png')
CHEST_COOL = py.transform.rotate(py.transform.scale(CHEST_IMAGE, (PLAYER_WIDTH, PLAYER_HEIGHT)), 180)

BACKGROUND = py.transform.scale(py.image.load('Python\Assets\Background2.png'), (WIDTH, HEIGHT))

WINNER1_TEXT = py.image.load('Python\Assets\PLAYER 2 WINS2.png')
WINNER2_TEXT = py.image.load('Python\Assets\PLAYER 1 WINS2.png')

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(BACKGROUND,(0, 0))
    py.draw.rect(WIN, PURPLE, BORDER)
    
    player_controls = CONTROL.render("CONTROLS: ARROW KEYS, L, K", 1 , WHITE)
    player_controls2 = CONTROL.render("CONTROLS: W, A, S, D, F, G", 1 , WHITE)
    red_health_text = HEALTH_FONT.render("Health:" + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health:" + str(yellow_health), 1, WHITE)
    WIN.blit(player_controls, (WIDTH - 450, 0))
    WIN.blit(player_controls2, (WIDTH - 450, HEIGHT -28))
    WIN.blit(red_health_text, (0, 0))
    WIN.blit(yellow_health_text, (0, HEIGHT - yellow_health_text.get_height() ))
    
    WIN.blit(RIFLE, (yellow.x , yellow.y))
    WIN.blit(CHEST_COOL, (red.x , red.y ))
    
    for bullet in red_bullets:
        py.draw.rect(WIN, RED, bullet)
    
    for bullet in yellow_bullets:
        py.draw.rect(WIN, BLUE, bullet)
    
    py.display.update()
    
def yellow_keys_movement(keys_pressed, yellow):
    global VEL2
    if keys_pressed[py.K_a] and yellow.x - VEL2 > 0:  # Left
        yellow.x -= VEL2
    if keys_pressed[py.K_d] and yellow.x + yellow.width + VEL2 < WIDTH:  # Right
        yellow.x += VEL2
    if keys_pressed[py.K_w] and yellow.y - yellow.height - VEL2 > BORDER.y - 50:  # Up
        yellow.y -= VEL2
    if keys_pressed[py.K_s] and yellow.y + yellow.height + VEL2 < HEIGHT:  # Down
        yellow.y += VEL2
    if keys_pressed[py.K_g]:
        ability_active2 = True
    else: 
        ability_active2 = False
    if ability_active2: 
        VEL2 = 7 + ability_speed_boost2
    else:
        VEL2 = 5
    
def red_keys_movement(keys_pressed, red):
    global VEL
    if keys_pressed[py.K_LEFT] and red.x - VEL > 0:  # Left
        red.x -= VEL
    if keys_pressed[py.K_RIGHT] and red.x + red.width + VEL < WIDTH:  # Right
        red.x += VEL
    if keys_pressed[py.K_UP] and red.y - VEL >= 0:  # Up
        red.y -= VEL
    if keys_pressed[py.K_DOWN] and red.y + red.height + VEL < BORDER.y + BORDER.height:  # Down
        red.y += VEL
    if keys_pressed[py.K_k]:
        ability_activate = True
    else:
        ability_activate = False
    if ability_activate:
        VEL = 7 + ability_speed_boost
    else:
        VEL = 5
        

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.y -= BULLET_VEL
        if red.colliderect(bullet):
            py.event.post(py.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.y < 0:
            yellow_bullets.remove(bullet)
    
    for bullet in red_bullets:
        bullet.y += BULLET_VEL
        if yellow.colliderect(bullet):
            py.event.post(py.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.y > HEIGHT:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = text
    WIN.blit(draw_text,(WIDTH/2 - draw_text.get_width() + 325 , HEIGHT/2 - draw_text.get_height()/2))
    py.display.update()
    py.time.delay(5000)

def main():
    red = py.Rect(220, 100, PLAYER_WIDTH, PLAYER_HEIGHT)
    yellow = py.Rect(220, 500, PLAYER_WIDTH, PLAYER_HEIGHT)
    
    red_bullets = []
    yellow_bullets = []
    
    red_health = 10
    yellow_health = 10
    
    clock = py.time.Clock()
    run = True

    mixer.music.load('Python\Assets\Winter theme.mp3')
    mixer.music.play(-10)

    while run:
        clock.tick(FPS)
        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
                py.quit()
                
            if event.type == py.KEYDOWN:
                if event.key == py.K_f and len(yellow_bullets) < MAX_BULLET:
                    bullet = py.Rect(
                        yellow.x + yellow.width // 2 - 5, yellow.y + yellow.height - 80, 10, 20
                    )
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                    
                if event.key == py.K_l and len(red_bullets) < MAX_BULLET:
                    bullet = py.Rect(
                        red.x + red.width // 2 - 5 , red.y - red.height + 110, 10, 20
                    )
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                    
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
        winner_text = ''
        if winner_text == '':
            if red_health <=0:
                WIN_SOUND.play()
                draw_winner(WINNER1_TEXT)
                break
            
            if yellow_health <=0:
                WIN_SOUND.play()
                draw_winner(WINNER2_TEXT)
                break
        
        keys_pressed = py.key.get_pressed()  
        yellow_keys_movement(keys_pressed, yellow)
        red_keys_movement(keys_pressed, red)
        
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)        
                
    main()
    
if __name__ == "__main__":
    main()