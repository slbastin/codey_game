from game import game_base
from game import sprite_create
from game import *
import codey 
import time
import random

DIR_NONE = 0
DIR_LEFT = 1
DIR_RIGHT = 2

score = 0
game = game_base()

plane_s = '000000000000c060c000000000000000'
plane_s1 = '000000000000c0e0c000000000000000'
plane_s2 = '00000000000080408000000000000000'

bullet_s =  "000000000000001c0000000000000000"

plane_id = 0
music_id = 0

bullet_run_count = 0
bullet_run_flag = False

plane = None
bullet = None

music_name = "shot"

def background_control():
    global score
    temp = game.get_background()
    
    if score < 50:
        a = random.randint(0, 15)
    elif score < 100:
        a = random.randint(0, 7)
        b = random.randint(8, 15)
    else:
        a = random.randint(0, 5)
        b = random.randint(6, 11)
        c = random.randint(7, 15)

    for i in range(16):
        temp[i] <<= 1
        temp[i] &= 0xff
        if score < 50:
            if i == a:
                temp[i] |= 0x01
        elif score < 100:
            if i == a or i == b:
                temp[i] |= 0x01
        else:
            if i == a or i == b or i == c:
                temp[i] |= 0x01            

    game.set_background(temp)

def barrier_delete():
    global score, music_id
    i = bullet.get_position()[0]
    game.set_background_with_column(0x00, i + 7)


def bullet_move_control():
    global bullet_run_flag, bullet_run_count, score, music_name, music_id
    if codey.is_button('C'):
        bullet_run_flag = True
    move_step = 5

    if bullet_run_flag:
        if bullet_run_count == 0:
            codey.say(music_name)
            bullet.set_position([plane.get_position()[0], plane.get_position()[1] + 2]) 
            bullet.show()
            bullet_run_count += 1
            if game.background_collision_check(bullet):
                score += 1
                barrier_delete()
        elif bullet_run_count < move_step:
            bullet.up()
            bullet_run_count += 1
            if game.background_collision_check(bullet):
                score += 1
                barrier_delete()
        else:
            bullet.home()
            bullet.hide()
            bullet_run_count = 0
            bullet_run_flag = False

def plane_move_control():
    global plane
    if plane == None:
        return
    if codey.is_button('A'):
        if plane.meet_border_check() & LEFT_MEET:
             plane.right()
        plane.left()
    elif codey.is_button('B'):
        if plane.meet_border_check() & RIGHT_MEET:
             plane.left()
        plane.right()

game_status = 0
def main():
    global game_status, score, plane_id, plane, music_name, bullet, music_id
    count = 0

    while True:
        if game_status == 0:
            if plane_id == 0:
                codey.face(plane_s)
            elif plane_id == 1:
                codey.face(plane_s1)
            else:
                codey.face(plane_s2)

            if codey.is_button("C"):
                codey.say("start")
                game_status = 1
                score = 0
                if plane_id == 0:
                    plane = sprite_create(plane_s)
                elif plane_id == 1:
                    plane = sprite_create(plane_s1)
                else:
                    plane = sprite_create(plane_s2)

                bullet = sprite_create(bullet_s)
                game.add_sprite(plane)
                bullet.hide()
                game.add_sprite(bullet)

                game.game_start()
                time.sleep(1)
            elif codey.is_button("A"):
                plane_id += 1
                if plane_id > 2:
                    plane_id = 0
                while codey.is_button("A"):
                    pass
            elif codey.is_button("B"):
                music_id += 1
                if music_id > 2:
                    music_id = 0

                if music_id == 0:
                    music_name = "shot"
                elif music_id == 1:
                    music_name = "laser"
                elif music_id == 2:
                    music_name = "score"
                codey.say(music_name)
                while codey.is_button("B"):
                    pass

        elif game_status == 1:
            if count % 3 == 0:
                plane_move_control()
            
            bullet_move_control()

            if count % (codey.dail() // 6) == 0:
                background_control()
            if game.background_collision_check(plane):
                codey.say('wrong')
                game_status = 2
                game.set_background("00000000000000000000000000000000")
                game.sprite_list_clean()

                palne = None
                bullet = None
                game.game_over()
            time.sleep(0.02)
        else:
            codey.show(score)
            if codey.is_button("C"):
                game_status = 0
            time.sleep(0.1)
        count += 1

main()
