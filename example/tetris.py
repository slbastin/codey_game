from game import game_base
from game import sprite_create
from game import *
import codey 
import time
import random

score = 0
game = game_base()
game.game_start()

a_s = '10101010000000000000000000000000'
b_s = '10380000000000000000000000000000'
c_s = '30300000000000000000000000000000'
d_s = '10180800000000000000000000000000'
e_s = '30101000000000000000000000000000'
f_s = '08181000000000000000000000000000'
sprite_num = 6
sprites = [a_s, b_s, c_s, d_s, e_s, f_s]
current_script = 0
def line_remove_process():
    global score
    screen = game.get_screen()
    i = 0
    while i < 16:
        if screen[i] & 0xff == 0xff:
            score += 1
            del game.back_ground[i]
            game.back_ground.insert(0, 0x00)
            codey.say("start")
        i += 1
    time.sleep(0.2)

down_speed = 10
codey.set_variable('cmd', 0)
def on_button_callback2():
    global down_speed, current_script
    time.sleep(0.5)
    while True:
        if codey.get_variable('cmd') == 1:
            current_script.up()
            codey.set_variable('cmd', 0)          
        elif codey.get_variable('cmd') == 2:
            current_script.down()
            codey.set_variable('cmd', 0)
        elif codey.get_variable('cmd') == 3:
            current_script.rotate()
            codey.set_variable('cmd', 0)
        elif codey.get_variable('cmd') == 4:
            down_speed = 2
            codey.set_variable('cmd', 0)

        temp = current_script.meet_border_check()
        if temp == UP_MEET:
            current_script.down()
            while current_script.meet_border_check() == UP_MEET:
                current_script.down()
        elif temp == DOWN_MEET:
            current_script.up()
            while current_script.meet_border_check() == DOWN_MEET:
                current_script.up()
        time.sleep(0.05)
         
codey.on_button('C', on_button_callback2)

def on_button_callback3():
    global current_script, down_speed, score
    while True:
        index = random.randint(0, sprite_num - 1)
        current_script = sprite_create(sprites[index])
        game.add_sprite(current_script)
        if game.background_collision_check(current_script):
            game.game_over()
            time.sleep(0.2)
            codey.show(score)
            codey.say("wrong")
            break
        count = 1
        down_speed = 10
        while True:
            if count % down_speed == 0:
                current_script.right()
            
            if current_script.meet_border_check() == RIGHT_MEET:
                current_script.left()
                codey.say("score")
                break

            if game.background_collision_check(current_script):
                current_script.left()
                codey.say("score")
                break
 
            time.sleep(0.025)
            count += 1
        time.sleep(0.1)
        game.set_background(game.get_screen())
        current_script.hide()
        time.sleep(0.1)
        line_remove_process()
        game.del_sprite(current_script)

codey.on_button('C', on_button_callback3)
