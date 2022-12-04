import sprites as s
import pygame as p
from settings import *
import random
import os
import pygame.freetype


def meteor_spawn():
    meteor_img = p.image.load("res/PNG/Meteors/" + random.choice(list_meteors))
    meteor = s.Asteroid((random.randint(200, 700), -100), meteor_img)
    meteors_group.add(meteor)


def draw():
    win.blit(bg_img, (0, 0))
    meteors_group.draw(win)
    lasers_group.draw(win)
    ship.draw(win)
    hp_font.render_to(win, (85, 23), str(ship.hp), fgcolor=(255, 255, 255))
    hp_font.render_to(win, (SCREEN_WIDTH - 180, 23), str(ship.score).zfill(5), fgcolor=(255, 255, 255))
    p.mouse.set_visible(False)
    win.blit(hp_img, (20, 20))
    win.blit(x_img, (60, 28))


def draw_menu():
    win.fill('VIOLET')
    win.blit(game_over_surf, game_over_rect)
    button.draw(win)
    button_exit.draw(win)
    win.blit(hp_img, (20, 20))
    hp_font.render_to(win, (85, 23), str(ship.hp), fgcolor=(255, 255, 255))
    hp_font.render_to(win, (SCREEN_WIDTH - 180, 23), str(ship.score).zfill(5), fgcolor=(255, 255, 255))
    win.blit(x_img, (60, 28))


def update():
    global game_state
    ship.move()
    meteors_group.update()
    lasers_group.update()
    if p.sprite.spritecollide(ship, meteors_group, True):
        ship.get_damage(1)
        hit_ship_sound.play()

    for laser in lasers_group:
        if p.sprite.spritecollide(laser, meteors_group, True):
            laser.kill()
            hit_meteor_sound.play()
            ship.score += 1
    if ship.hp == 0:
        game_state = 'Menu'


def stop_game():
    p.mouse.set_visible(True)
    meteors_group.empty()
    lasers_group.empty()


def make_lasers():
    lasers_group.add(s.Laser(ship.rect.center, laser_img))
    fire_laser_sound.play()


list_ships = os.listdir("res/PNG/Ships")
list_meteors = os.listdir("res/PNG/Meteors")
p.init()
ship_png = p.image.load("res/PNG/Ships/" + random.choice(list_ships))  # Подгрузка изображения
bg_img = p.image.load("res/Backgrounds/blue.png")
bg_img = p.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
laser_img = p.image.load("res/PNG/Lasers/laserRed01.png")
ship_images = [p.image.load(f'res/PNG/Damage/playerShip1_damage{i}.png') for i in range(1, 4)]
ship_images.insert(0, p.image.load('res/PNG/Ships/playerShip1_orange.png'))
fire_laser_sound = p.mixer.Sound('res/Bonus/sfx_laser1.ogg')
hit_meteor_sound = p.mixer.Sound('res/Bonus/meteor_hit.wav')
hit_ship_sound = p.mixer.Sound('res/Bonus/hit.wav')
game_over_sound = p.mixer.Sound('res/Bonus/sfx_lose.ogg')
new_game_sound = p.mixer.Sound('res/Bonus/sfx_twoTone.ogg')
bg_music = p.mixer.Sound('res/Bonus/space_ambiance.wav')
hp_font = p.freetype.Font("res/Bonus/kenvector_future.ttf", 42)
button_font = p.freetype.Font("res/Bonus/kenvector_future.ttf", 52)
hp_img = p.image.load('res/PNG/UI/playerLife1_orange.png')
x_img = p.image.load('res/PNG/UI/numeralX.png')

win = p.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
p.display.set_caption('Asteroids')
clock = p.time.Clock()
meteors_group = p.sprite.Group()
lasers_group = p.sprite.Group()

ship = s.Ship((SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50), ship_images)
button = s.Button((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), 'restart', button_font)
button_exit = s.Button((SCREEN_WIDTH/2, 400), 'exit', button_font)
game_over_surf, game_over_rect = button_font.render('game over')
game_over_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)

SPAWN_METEOR = p.USEREVENT
p.time.set_timer(SPAWN_METEOR, 300)
bg_music.play(-1)
play = 1
game_state = 'MAIN GAME'
while play:
    for event in p.event.get():
        if event.type == p.QUIT:
            play = 0
        if game_state == 'MAIN GAME':
            if event.type == SPAWN_METEOR:
                meteor_spawn()
            if event.type == p.MOUSEBUTTONDOWN:
                if len(lasers_group) == 0:
                    make_lasers()

        else:
            if (event.type == p.MOUSEBUTTONDOWN and button.rect.collidepoint(event.pos)):
                game_state = 'MAIN GAME'
                ship.rebuild()
            if (event.type == p.MOUSEBUTTONDOWN and button_exit.rect.collidepoint(event.pos)):
                play = 0

    if game_state == 'MAIN GAME':
        draw()
        update()
    else:
        draw_menu()
        stop_game()

    clock.tick(FPS)
    p.display.update()
