from microbit import *
from random import randint

hole = randint(0, 4)
bird = 2
x = 4
life = 3
tick = 0
#t=70

while True:
    if button_a.is_pressed() and bird < 4: 
        bird += 1
    if button_b.is_pressed() and bird > 0:
        bird -= 1

    display.clear()
    display.set_pixel(0, bird, 9)

    for y in range(5):
        if y != hole:  
            display.set_pixel(x, y, 4)
    
    if tick % 5 == 0:
        x -= 1
        #sleep(100)

    if x < 0:
        x = 4
        hole = randint(0, 4)
        display.clear
    
    if hole != bird and x == 0:
        life -= 1
        sleep(500)
        display.scroll("LIVES LEFT:", 60)
        display.scroll(str(life), 100)
        x = 4
        hole = randint(0, 4)
        sleep(500)
    
    if life <= 0:
        display.clear
        display.scroll("GAME OVER!", 100)
        sleep(200000)
        #sys.exit()
        break
    tick += 1
    sleep(70)
    #t -= 1
    #sleep(t)
