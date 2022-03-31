import pygame
import tkinter as tk
import os
import json
from Vector import Vector2
from Player import Player, load_images
from Tiles import Brick
from rectCollision import handleCollision
import time

root = tk.Tk()
resolution = [root.winfo_screenwidth(), root.winfo_screenheight()]
screen = pygame.display.set_mode(resolution)
path = os.path.dirname(__file__)


def constructMap(level_data, brick_texture, flag_texture, idle_texture, gravity):
    bricks = []
    enemies = []
    finish_points = []
    scale = resolution[1] / 15
    with open(level_data, 'r', encoding='utf-8') as f:
        json_dict = json.load(f)
        for i in json_dict["Bricks"]:
            new_Brick = Brick(screen, [i[0] * scale, i[1] * scale, scale, scale], brick_texture)
            bricks.append(new_Brick)
        for i in json_dict["Finish"]:
            finishPoint = Brick(screen, [i[0] * scale, i[1] * scale, scale, scale], flag_texture)
            finish_points.append(finishPoint)
        spawn = json_dict["Start"]
        player = Player(screen, [spawn[0][0] * scale - scale / 2, spawn[0][1] * scale - scale / 2,
                                 scale * 1.5, scale * 1.5], gravity, idle_texture, "Textures/Player/Walk_Cycle")
    return bricks, enemies, player, finish_points


def handle_collisions(event_list, player, bricks, enemies, end_points, screen_size):
    if player.x < 0:
        player.changeCoord([-player.x, 0])
    if player.x + player.w > screen_size[0]:
        depth = player.x - screen_size[0]
        player.changeCoord([-depth, 0])
    if player.y > screen_size[1]:
        event_list["Death"] = True
    player_rect = [player.x, player.y, player.w, player.h]
    player_center = Vector2(player.x + player.w / 2, player.y + player.h / 2)

    for flag in end_points:
        flag_rect = [flag.x, flag.y, flag.w, flag.h]
        collision, correction = handleCollision(player_rect, flag_rect)
        if collision:
            event_list["Win"] = True

    player.onFloor = False
    for brick in bricks:
        brick_rect = [brick.x, brick.y, brick.w, brick.h]
        brick_center = Vector2(brick.x + brick.w / 2, brick.y + brick.h / 2)
        vector = brick_center.sub(player_center)
        if vector.magnitude() <= (player.w + player.h):
            collision, correction = handleCollision(player_rect, brick_rect)
            if collision:
                if correction[1] < 0:
                    player.onFloor = True
                if correction[1] != 0:
                    player.velocity[1] = 0
                player.changeCoord(correction)


def draw_level(bricks, flags, player):
    for flag in flags:
        flag.draw()
    for brick in bricks:
        brick.draw()
    player.draw()


def update_entities(player, enemies, time_elapsed):
    player.move(time_elapsed)


def shift_level(map_velocity, flags, bricks, player):
    for flag in flags:
        flag.changeCoords(map_velocity)
    for brick in bricks:
        brick.changeCoords(map_velocity)
    player.changeCoord(map_velocity)


def determineShift(events, screen_size, player):
    velocity = [0, 0]
    if player.x + player.w / 2 > screen_size[0] / 2:
        events["Screen_follow"] = True
    if events["Screen_follow"]:
        velocity = [screen_size[0] / 2 - (player.x + player.w / 2), 0]
    return velocity


def main():
    fps = 120
    time_elapsed = 1/120

    brick_list, enemy_list, player, finish_points = constructMap("Data/Level_Data/level1.json",
                                                                 "Textures/Brick.png", "Textures/TEST.png",
                                                                 "Textures/Player/idle.png", 240)
    events = {
        "Death": False,
        "Win": False,
        "Screen_follow": False
    }
    running = True
    while running:
        start_time = time.time()
        if events["Death"]:
            running = False
        screen.fill((255, 255, 255))
        draw_level(brick_list, finish_points, player)
        pygame.display.flip()

        update_entities(player, None, time_elapsed)
        handle_collisions(events, player, brick_list, enemy_list, finish_points, resolution)
        map_velocity = determineShift(events, resolution, player)
        shift_level(map_velocity, finish_points, brick_list, player)

        keys = pygame.key.get_pressed()

        if events["Win"]:
            print("YOU WIN!")
            break

        if keys[pygame.K_a]:
            if keys[pygame.K_LSHIFT]:
                player.velocity[0] = -240
            else:
                player.velocity[0] = -150

        if keys[pygame.K_d]:
            if keys[pygame.K_LSHIFT]:
                player.velocity[0] = 240
            else:
                player.velocity[0] = 150

        if keys[pygame.K_w]:
            if player.onFloor:
                if abs(player.velocity[0]) > 240:
                    player.velocity[1] = -100
                else:
                    player.velocity[1] = -300

        if (not keys[pygame.K_a]) and (not keys[pygame.K_d]):
            player.velocity[0] = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        end_time = time.time()
        elapsed_time = end_time - start_time
        fps = 1/elapsed_time
        #if 1/fps - elapsed_time > 0:
        #    time.sleep(1/fps - elapsed_time)

    pygame.quit()


main()
